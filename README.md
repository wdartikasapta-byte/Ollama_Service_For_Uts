# Ollama service for uts

## StudyMate AI** — asisten belajar berbasis kecerdasan buatan.

Mahasiswa sering membutuhkan bantuan untuk memahami dan menyelesaikan soal
dari berbagai mata kuliah. Proyek ini menghadirkan StudyMate AI, aplikasi web
sederhana yang menerima soal dan menampilkan jawaban beserta penjelasan dengan
bantuan model bahasa Mistral melalui Ollama.

Pemrosesan model dijalankan melalui layanan Ollama pada komputer lokal, sehingga
pengguna dapat mencoba asisten tanpa menghubungkan aplikasi ke layanan model
berbasis cloud. Aplikasi juga menyimpan soal dan jawaban ke database SQLite agar
riwayat dapat dilihat kembali atau diunduh. StudyMate AI dimaksudkan sebagai
alat bantu belajar; pengguna tetap perlu memeriksa dan memahami jawabannya.

## Struktur Folder

```text
Ollama_Service_For_Uts/
├── .git/                 # Metadata dan riwayat versi Git
├── .venv/                # Lingkungan virtual Python proyek
├── .streamlit/
│   └── config.toml       # Pengaturan tema dan tampilan Streamlit
├── assets/
│   └── style.css         # Gaya visual aplikasi
├── data/
│   └── studymate.db      # Database SQLite untuk menyimpan riwayat
├── __pycache__/          # Cache bytecode Python (dibuat otomatis)
├── app.py                # Antarmuka web dan alur utama aplikasi
├── database.py           # Inisialisasi dan pengelolaan database/riwayat
├── scoring.py            # Pembuatan prompt dan komunikasi streaming dengan Ollama
├── requirements.txt      # Daftar dependensi Python
└── README.md             # Dokumentasi proyek
```

## Cara Menjalankan Aplikasi

### Persiapan

Pastikan Python dan [Ollama](https://ollama.com/download) sudah terpasang.
Aplikasi menggunakan model `mistral` melalui Ollama lokal.

### Instalasi dan menjalankan

Buka PowerShell, lalu clone repositori dan masuk ke folder proyek:

```powershell
git clone https://github.com/wdartikasapta-byte/Ollama_Service_For_Uts.git
cd Ollama_Service_For_Uts

# Buat lingkungan virtual jika belum ada
py -m venv .venv

# Aktifkan lingkungan virtual
.\.venv\Scripts\Activate.ps1

# Instal dependensi proyek
python -m pip install -r requirements.txt

# Unduh model yang digunakan aplikasi (cukup sekali)
ollama pull mistral

# Jalankan aplikasi web
python -m streamlit run app.py
```

Jika PowerShell menolak aktivasi lingkungan virtual, gunakan Python di
lingkungan virtual secara langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull mistral
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Pastikan layanan Ollama berjalan sebelum mengirim soal. Jika Ollama belum aktif,
buka aplikasi Ollama atau jalankan `ollama serve` di jendela terminal lain.
Aplikasi terhubung ke `http://localhost:11434` dan biasanya terbuka di
`http://localhost:8501`. Biarkan terminal Streamlit tetap berjalan selama
aplikasi digunakan; hentikan dengan `Ctrl+C`.
