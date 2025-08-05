# Download a Hugging Face Model Snapshot using Python

This Python script downloads a snapshot of a Hugging Face model repository using the `huggingface_hub` library.

## 📦 Requirements

- Python 3.7+
- `huggingface_hub` package

Install the dependency:

```bash
pip install huggingface_hub
```

Import environment variables in the "Set me up"

```
export HF_HUB_ETAG_TIMEOUT=86400
export HF_HUB_DOWNLOAD_TIMEOUT=86400
export HF_ENDPOINT=https://acme.jfrog.io/artifactory/api/huggingfaceml/alex-huggingface-remote

export HF_TOKEN=your-artifactory-token
```

📁 Output
The model will be downloaded and cached locally under the ~/.cache/huggingface directory.

✅ Notes
Replace openai-community/gpt2 with any other model name you wish to download.

The snapshot_download() function fetches all necessary files at a specific revision (e.g., "main").

