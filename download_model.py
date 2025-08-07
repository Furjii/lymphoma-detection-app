# download_model.py
import gdown
import os

# Pastikan folder model/ ada
os.makedirs("model", exist_ok=True)

# ID file dari Google Drive
file_id = "1AL8MzQPdFW6aMxKZyR9l6lCxVfXx9RS9"
url = f"https://drive.google.com/uc?id={file_id}"

# File output ke dalam folder model/
output_path = "model/model0.h5"

print(f"Downloading model to: {output_path}")
gdown.download(url, output_path, quiet=False)
