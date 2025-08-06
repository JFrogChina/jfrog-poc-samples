import os
from huggingface_hub import snapshot_download

# Read token from environment variable
RT_token = os.getenv("SOLENG_IO_TOKEN")
if not RT_token:
    raise ValueError("Please set the SOLENG_IO_TOKEN environment variable.")

# Model name
model_name = "shibing624/text2vec-base-chinese"  # Replace with the model you want to download

# Download the model snapshot
snapshot_download(
    repo_id=model_name,
    revision="main",
    token=RT_token,
    repo_type="model"
)
