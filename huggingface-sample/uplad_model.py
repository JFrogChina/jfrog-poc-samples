import os
from huggingface_hub import HfApi

# Load token
TOKEN = os.getenv("SOLENG_IO_TOKEN")
if not TOKEN:
    raise ValueError("Please set SOLENG_IO_TOKEN")

api = HfApi(token=TOKEN)

folder_path = os.path.expanduser("~/.cache/huggingface/hub/models--huggingbob--test")

api.upload_folder(
    folder_path=folder_path,
    repo_id="huggingbob/test",
    revision="main",
    repo_type="model"
)

print("Upload completed")
