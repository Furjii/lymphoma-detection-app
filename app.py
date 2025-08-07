from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Halo, Vercel!</h1><p>Jika Anda melihat ini, artinya konfigurasi dasar sudah berhasil.</p>"

# Route ini untuk membantu debugging
@app.route('/<path:path>')
def all_routes(path):
    return f"<h1>Halaman '{path}' tidak ditemukan, tapi routing dasar dari app.py berhasil!</h1>"