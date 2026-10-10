"""Pengelolaan riwayat StudyMate AI menggunakan database SQLite."""

import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "studymate.db"


def init_database() -> None:
    """Membuat tabel riwayat."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS riwayat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soal TEXT NOT NULL,
                jawaban TEXT NOT NULL,
                waktu TEXT NOT NULL
            )
            """
        )


def simpan_riwayat(soal: str, jawaban: str) -> None:
    """Simpan soal dan jawaban yang berhasil dibuat AI."""
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO riwayat (soal, jawaban, waktu) VALUES (?, ?, ?)",
            (soal.strip(), jawaban.strip(), waktu),
        )


def ambil_riwayat() -> list[dict]:
    """Ambil seluruh riwayat, terbaru berada paling atas."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, soal, jawaban, waktu FROM riwayat ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def hapus_semua_riwayat() -> None:
    """Hapus semua isi tabel riwayat."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM riwayat")
