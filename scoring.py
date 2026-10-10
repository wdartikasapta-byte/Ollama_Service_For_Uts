"""Prompt akademik dan komunikasi streaming dengan Ollama."""

import json
from collections.abc import Iterator

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def buat_prompt(soal: str) -> str:
    """Susun prompt agar Mistral memahami berbagai jenis pertanyaan."""
    return f"""
Kamu adalah StudyMate AI, asisten akademik yang membantu mahasiswa menjawab
berbagai jenis soal dari berbagai bidang ilmu.

Instruksi:
1. Pahami jenis soal dan apa yang diminta pengguna.
2. Jawab berbagai jenis soal, termasuk matematika, pemrograman, sains,
   teknologi, bahasa, dan mata kuliah lainnya.
3. Untuk soal hitungan, tampilkan langkah penyelesaian dan hasilnya.
4. Untuk soal teori, berikan penjelasan yang jelas dan terstruktur.
5. Untuk soal pilihan ganda, tentukan pilihan paling tepat dan jelaskan alasannya.
6. Untuk soal pemrograman, berikan kode yang sesuai jika diperlukan.
7. Untuk soal bahasa, ikuti bahasa yang diminta dalam soal.
8. Jika ada beberapa soal, jawab satu per satu sesuai nomor.
9. Jangan mengarang informasi jika tidak mengetahui jawabannya.
10. Gunakan bahasa yang mudah dipahami mahasiswa.

SOAL PENGGUNA:
{soal}

JAWABAN:
""".strip()


def cek_ollama(timeout: float = 2.0) -> bool:
    """Periksa apakah layanan Ollama dapat dijangkau."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=timeout)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def jawab_dengan_streaming(prompt: str) -> Iterator[str]:
    """Kirim prompt ke Ollama dan hasilkan jawaban sedikit demi sedikit."""
    with requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True,
            "options": {"num_predict": 300},
        },
        stream=True,
        timeout=(10, 600),
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            token = data.get("response", "")
            if token:
                yield token
            if data.get("done", False):
                break
