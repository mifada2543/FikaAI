GIT sedang bermasalah😅,silakan download manual

Mesih pemula😅 kalau ada masalah boleh ditanya di Group.md

Saya usahakan menjawab sebisa saya -Mifada2543

![License](https://img.shields.io/github/license/mifada2543/FikaAI)
![Python](https://img.shields.io/badge/Built%20With-Python%203-blue)
![SQLite](https://img.shields.io/badge/Storage-SQLite-lightgrey)
![CLI+GUI](https://img.shields.io/badge/Modes-CLI%20%7C%20GUI-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
Android bisa dengan python + termux hanya versi CLI saja

## 📸 Tampilan GUI Fika

Bisa di cek di Screenshot
![Tampilan GUI Fika](https://github.com/mifada2543/FikaAI/blob/main/Screenshot/17505724575876390207229960351747.jpg)

![Tampilan GUI Fika]Dalam perbaikan

![Tampilan GUI Fika]Dalam perbaikan

🇮🇩 Fika AI — Asisten AI Ringan (Offline + GUI)

Fika adalah asisten AI ringan berbasis Python yang bisa berjalan dalam mode CLI (terminal) maupun GUI (desktop). Cocok untuk edukasi, eksperimen, atau hiburan pribadi.


---

🇬🇧 Fika AI — Lightweight AI Assistant (Offline + GUI)

Fika is a lightweight AI assistant built with Python, supporting CLI (terminal) and GUI (desktop) modes. Ideal for education, experimentation, or casual fun.


---

🎯 🇮🇩 Fitur Utama / 🇬🇧 Key Features

✅ Tanya jawab (AI offline ringan)
✅ Q&A with lightweight offline AI

✅ Kalkulator matematika dasar
✅ Basic math calculator

✅ Perhitungan geometri (keliling, luas, volume)
✅ Geometry calculations (perimeter, area, volume)

✅ Fakta teknologi dan fakta menarik harian
✅ Daily tech & fun facts

✅ Penyimpanan riwayat percakapan (SQLite)
✅ Chat history saved (SQLite)

✅ Pembelajaran pengetahuan baru secara manual
✅ Manual knowledge learning

✅ GUI sederhana dengan pemutar musik (pygame opsional)
✅ Simple GUI with music player (optional pygame)

✅ Mode CLI cepat & ringan
✅ Fast & lightweight CLI mode



---

🧠 Teknologi / Technologies

Python 3.8+

sqlite3 (riwayat & pengetahuan / history & knowledge)

json (data statis / static data)

tkinter (antarmuka GUI / GUI interface)(windows and linux only, Android not recomended)

pygame (opsional untuk musik / optional music player)(windows and linux only, Android not recomended)



---

🔧 🇮🇩 Cara Menjalankan / 🇬🇧 How to Run

📦 Rekomendasi editor: Visual Studio Code
tolong baca requirement.txt/please read requirement.txt
git clone https://github.com/mifada2543/FikaAI/V1.git
cd V1
pip install pygame     # Opsional, untuk GUI music player
python bot.py          # CLI mode
python bot.py --dev    # CLI mode with debug
python bot.py --gui    # GUI mode
python bot.py --gui    # GUI mode with debug

Saat dijalankan, kamu akan diminta memilih antara GUI atau CLI.
When run, you'll be prompted to choose GUI or CLI mode.

📝 Untuk Linux(langkahnya kurang tau), pastikan tkinter sudah terinstal:

sudo apt install python3-tk

📝langkah Untuk Android, Pastikan gunakan versi CLI.
download semua bahannya (CLI.py, pengetahuan.json, dll)
pastikan semua file ada di folder download
lalu copy semua filenya dan buat folder baru bernama "Fika"
Masuk ke termux pastikan sudah pkg update && pkg upgrade
pkg install python
lalu jalankan perintah "cp -r /sdcard/Download/Fika /data/data/com.termux/files/home/"
cd Fika
jalankan "python CLI.py"

---

📂 Struktur Proyek / Project Structure

fika/
├── bot.py                 # Program utama / Main program
├── pengetahuan.json       # Data pengetahuan offline
├── fakta_menarik.json     # Fakta menarik
├── riwayat_fika.db        # Riwayat disimpan otomatis
├── README.md              # Dokumentasi
├── .gitignore             # File yang diabaikan Git


---

💡 Belajar Manual / Manual Learning

Contoh:

belajar: ibu kota jepang = Tokyo


---

👨‍💻 Pengembang / Developer

Dikembangkan oleh Mifada2543 (Akiro) — 2025
Developed by Mifada2543 (Akiro) — 2025

📬 Untuk kolaborasi, hubungi via GitHub.
For collaboration, contact via GitHub.


---

🛡️ Hak cipta proyek ini tetap dimiliki oleh pencipta asli (mifada2543).  
Siapapun boleh menggunakan, memodifikasi(tidak untuk hal negatif dan melanggar norma), dan menyebarkan ulang dengan syarat tetap mencantumkan nama pembuat asli.

📄 Lisensi / License

MIT License
This project is based on Fika by Akiro (https://github.com/Mifada2543/FikaAI), licensed under the MIT License.

---
✨ Tentang Fika

> Fika adalah proyek asisten AI ringan yang lahir dari mimpi seorang pelajar berusia 12 tahun, dan mulai diwujudkan saat ia berusia 15 tahun.

Dikembangkan oleh Akiro (mifada2543), Fika dibuat dengan rasa penasaran besar terhadap dunia AI dan bagaimana sebuah asisten virtual bisa bekerja — tanpa perlu sumber daya besar atau internet.

Dibangun sepenuhnya dengan Python, Fika tumbuh dari proyek iseng menjadi asisten virtual lengkap dengan antarmuka CLI dan GUI, fitur matematika, fakta, alarm, hingga pemutar musik.

Fika adalah simbol bahwa semangat belajar dan ketekunan bisa menghasilkan karya yang luar biasa

> 📝 Fika dibuat karena sang kreator lagi gabut 😁
Tapi siapa sangka, dari kegabutan lahirlah AI offline kayak Fika!

Created because the dev was bored 😁
But who knew boredom could lead to an AI like Fika?
