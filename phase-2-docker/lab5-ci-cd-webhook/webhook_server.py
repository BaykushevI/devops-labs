from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import datetime
import os

app = FastAPI()


class PushPayload(BaseModel):
    ref: str | None = None


BASE_DIR = "/home/ibayk/devops-labs/phase-2-docker/lab5-ci-cd-webhook"
DEPLOY_SCRIPT = os.path.join(BASE_DIR, "deploy_lab4.sh")
WEBHOOK_LOG = os.path.join(BASE_DIR, "webhook_calls.log")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/deploy")
async def deploy(payload: PushPayload):
    """
    Webhook endpoint, called from GitHub:
    - по ref = refs/tags/vX.Y.Z
    - start deploy_lab4.sh
    - return success/failed depending of exit code of script
    """
    ref = payload.ref or ""

    # Логваме payload-а за дебъг
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(WEBHOOK_LOG, "a") as f:
        f.write("\n========== Webhook call ==========\n")
        f.write(f"Time: {datetime.datetime.now().isoformat()}\n")
        f.write(f"ref: {ref}\n")

    # Ако искаш да ограничиш само до тагове – остави този if
    if ref and not ref.startswith("refs/tags/"):
        return {
            "status": "ignored",
            "reason": f"ref '{ref}' is not a tag (refs/tags/*)",
        }

    # Стартираме deploy скрипта
    proc = subprocess.run(
        ["/bin/bash", DEPLOY_SCRIPT],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    # Логваме резултата
    with open(WEBHOOK_LOG, "a") as f:
        f.write(f"Exit code: {proc.returncode}\n")
        f.write("----- STDOUT -----\n")
        f.write(proc.stdout + "\n")
        f.write("----- STDERR -----\n")
        f.write(proc.stderr + "\n")

    if proc.returncode != 0:
        return {
            "status": "failed",
            "exit_code": proc.returncode,
        }

    return {
        "status": "success",
        "exit_code": 0,
    }

