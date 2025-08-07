## 🔁 Model Otomatis Diunduh dari Google Drive

Model `lymphoma_model.h5` tidak disimpan di repo GitHub karena ukurannya besar (>100MB).  
Saat aplikasi dibuild di Vercel, file model akan otomatis diunduh dari Google Drive melalui script `download_model.py`.

🔗 [Link model](https://drive.google.com/file/d/1AL8MzQPdFW6aMxKZyR9l6lCxVfXx9RS9/view?usp=sharing)

Pastikan kamu sudah meng-install `gdown`:
```bash
pip install gdown
python download_model.py
