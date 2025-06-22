Fika AI

Fika adalah asisten AI ringan berbasis Python yang bisa dijalankan dalam mode CLI (terminal) maupun GUI (desktop). Proyek ini dirancang untuk edukasi, eksperimen, dan hiburan.

🎯 Fitur Utama

✅ Tanya jawab (offline AI ringan)

✅ Kalkulator matematika dasar

✅ Perhitungan geometri (keliling, luas, volume)

✅ Fakta teknologi dan fakta menarik harian

✅ Penyimpanan riwayat percakapan (SQLite)

✅ Pembelajaran pengetahuan baru secara manual

✅ GUI sederhana berbasis Tkinter (dengan pemutar musik)

✅ Mode terminal CLI cepat & ringan

Recommended memakai VS code

🧠 Teknologi yang Digunakan

Python 3.8+

sqlite3 untuk menyimpan riwayat & pengetahuan

json untuk pengetahuan statis

tkinter untuk antarmuka GUI

**Catatan untuk Linux:**
Pastikan tkinter sudah terinstal:

bash
sudo apt install python3-tk


pygame (opsional, untuk pemutar musik)

🔧 Cara Menjalankan

Clone repository:

git clone https://github.com/mifada2543/FikaAI.git
cd FikaAI

Install dependensi (opsional):

pip install pygame

Jalankan:

python bot.py          # Mode CLI
python bot.py --dev    # Mode CLI dengan debug

Saat dijalankan, kamu akan diminta memilih gui atau langsung menggunakan CLI.

📂 Struktur File

fika/
├── bot.py     # Program utama
├── pengetahuan.json  # Data pengetahuan offline
├── fakta_menarik.json # Fakta-fakta menarik
├── .gitignore  # File yang tidak akan dipush ke GitHub
├── README.md   # Dokumentasi ini

📌 Catatan

Riwayat tersimpan otomatis ke riwayat_fika.db

Semua data JSON bisa diedit secara manual

Fika bisa "belajar" jika kamu ketik:

belajar: ibu kota jepang = Tokyo

🧑‍💻 Developer

Dikembangkan oleh Akiro (2025). Untuk pertanyaan atau kolaborasi, silakan kontak melalui GitHub.

📄 Lisensi

MIT License

> Fika dibuat karena sang kreator [mifada2543](https://github.com/mifada2543) lagi gabut😁  
> Tapi siapa sangka, dari kegabutan lahir AI offline kayak Fika!

📌 Mohon tidak klaim ulang sebagai milik pribadi.
