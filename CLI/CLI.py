import math
import random
import re
import sqlite3
import json
import os
import datetime
import urllib.request
import sys
import subprocess
import threading
import time

PENGETAHUAN_URL = "https://github.com/mifada2543/FikaAI/blob/main/update/pengetahuan.json"  # Ganti dengan URL JSON online

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("riwayat_fika.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pertanyaan TEXT,
            jawaban TEXT,
            waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS pengetahuan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pertanyaan TEXT,
            jawaban TEXT
        )
    """)
    conn.commit()
    conn.close()

def simpan_riwayat(pertanyaan, jawaban):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("INSERT INTO riwayat (pertanyaan, jawaban) VALUES (?, ?)", (pertanyaan, jawaban))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal menyimpan riwayat:", e)

def simpan_pengetahuan(pertanyaan, jawaban):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS pengetahuan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pertanyaan TEXT,
                jawaban TEXT
            )
        """)
        c.execute("INSERT INTO pengetahuan (pertanyaan, jawaban) VALUES (?, ?)", (pertanyaan.lower(), jawaban))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal menyimpan pengetahuan:", e)

def tampilkan_riwayat(limit=10):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("SELECT waktu, pertanyaan, jawaban FROM riwayat ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        if not rows:
            print("Belum ada riwayat.")
            return
        print("\n--- Riwayat Tanya Jawab Terakhir ---")
        for waktu, tanya, jawab in rows[::-1]:
            print(f"[{waktu}]")
            print(f"Tanya: {tanya}")
            print(f"Jawab: {jawab}\n")
    except Exception as e:
        print("Gagal menampilkan riwayat:", e)

def cari_pengetahuan(pertanyaan):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("""
            SELECT jawaban FROM pengetahuan WHERE pertanyaan=?
        """, (pertanyaan.lower(),))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception:
        pass
    return None

# --- Utility & Fitur Lain ---
def input_angka(prompt, allow_negative=False):
    while True:
        try:
            val = float(input(prompt))
            if not allow_negative and val < 0:
                print("Angka tidak boleh negatif.")
                continue
            return val
        except ValueError:
            print("Input tidak valid, coba lagi.")

def tampilkan_cuaca():
    kondisi = ["cerah", "berawan", "hujan ringan", "hujan deras", "berkabut"]
    suhu = random.randint(25, 35)
    return f"Hari ini cuacanya {random.choice(kondisi)} dengan suhu sekitar {suhu}°C."

def tampilkan_fakta():
    fakta = [
        "SoC Dimensity 9300 punya performa lebih tinggi dari Snapdragon 8 Gen 2.",
        "GPU Adreno dibuat oleh Qualcomm dan digunakan di banyak HP Android.",
        "CPU modern punya beberapa core untuk multitasking.",
        "Smartphone flagship biasanya punya refresh rate 120Hz untuk layar lebih halus.",
        "Baterai lithium-ion lebih awet jika tidak diisi penuh 100% terus-menerus."
    ]
    return "Fakta teknologi hari ini:\n" + random.choice(fakta)

def cek_faktorial(tanya):
    match = re.search(r'(-?\d+)\s*!', tanya)
    if match:
        angka = int(match.group(1))
        if angka < 0:
            return "Faktorial hanya untuk bilangan bulat non-negatif ya."
        try:
            hasil = math.factorial(angka)
            return f"{angka}! = {hasil}"
        except Exception:
            return "Maaf, terjadi kesalahan saat menghitung faktorial."
    return None

def cek_hitung(tanya):
    allowed = "0123456789+-*/(). "
    ekspresi = "".join(c for c in tanya if c in allowed)
    if ekspresi.strip() == "":
        return None
    try:
        hasil = eval(ekspresi)
        return f"Hasil perhitungannya adalah {hasil}"
    except Exception:
        return None

def load_pengetahuan_file():
    path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def cek_keyword(tanya):
    tanya = tanya.lower()
    if "help" in tanya or "bantuan" in tanya:
        return (
            "Berikut beberapa tutorial singkat yang bisa kamu coba:\n"
            "- **Belajar pengetahuan:**\n"
            "    Belajar: ibu kota jepang = tokyo\n"
            "- **Kalkulator:**\n"
            "    Ketik ekspresi matematika, contoh: 2+3*4\n"
            "- **Faktorial:**\n"
            "    Contoh: 5!\n"
            "- **Timer:**\n"
            "    timer 5 menit\n"
            "- **Alarm:**\n"
            "    alarm jam 06:30\n"
            "- **Pengingat:**\n"
            "    ingatkan aku untuk minum air dalam 10 menit\n"
            "- **Geometri:**\n"
            "    Pilih menu Geometri untuk keliling, luas, volume\n"
            "- **Update pengetahuan online:**\n"
            "    Pilih menu 'Update Pengetahuan Online' di menu utama\n"
            "- **Preset Timer/Alarm:**\n"
            "    Gunakan tombol preset di menu Timer/Pengingat/Alarm (GUI)\n"
            "\nKetik pertanyaan atau perintah sesuai contoh di atas!"
        )
    pengetahuan = load_pengetahuan_file()
    for kunci, jawaban in pengetahuan.items():
        if kunci.lower() in tanya:
            return jawaban
    return None

def simpan_pengetahuan_file(pertanyaan, jawaban):
    path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
    data = load_pengetahuan_file()
    data[pertanyaan.lower()] = jawaban
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tampilkan_fakta_menarik():
    path = os.path.join(os.path.dirname(__file__), "fakta_menarik.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            fakta_list = json.load(f)
        if not fakta_list:
            return "Belum ada fakta menarik."
        return "Fakta menarik hari ini:\n" + random.choice(fakta_list)
    except Exception:
        return "Gagal membaca fakta menarik."

def pastikan_file_json():
    for fname, default in [
        ("pengetahuan.json", {}),
        ("fakta_menarik.json", [])
    ]:
        path = os.path.join(os.path.dirname(__file__), fname)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)

def update_pengetahuan_online():
    """Update pengetahuan.json lokal dari PENGETAHUAN_URL (harus RAW link)."""
    try:
        url = PENGETAHUAN_URL.replace(
            "github.com", "raw.githubusercontent.com"
        ).replace("/blob/", "/")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read().decode("utf-8")
        pengetahuan = json.loads(data)
        path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pengetahuan, f, ensure_ascii=False, indent=2)
        print("Pengetahuan berhasil diperbarui dari internet.")
        return True
    except Exception as e:
        print("Gagal update pengetahuan online:", e)
        return False

def tanya_fika():
    print("\n=== Tanya Fika ===")
    print("Ketik 'esc' untuk kembali ke menu utama.")
    saran = [
        "Coba 'help' untuk bantuan.",
        "Coba tanya tentang faktorial misal '5!'",
        "hitung matematika seperti '2+3*4', atau fakta teknologi.",
        "teknologi seputar smartphone, atau soal geometri.",
        "atau tanya tentang apa yang Fika bisa lakukan.",
        "atau tanya tentang 'Fika bisa apa'.",
        "atau tanya tentang 'spek vivo v21 5g'.",       
        "atau tanya tentang presiden Indonesia, ibukota Indonesia, atau gravitasi.",
        "atau tanya tentang fotosintesis, komputer, atau halo.",
        "atau tanya tentang spesifikasi smartphone seperti 'spek vivo v21 5g'.",
        "atau jika ingin kembali ketik 'esc' ya"
    ]
    while True:
        tanya = input("Kamu (Akiro): ").lower()

        if "esc" in tanya:
            print("Fika: Oke, kita kembali ke menu utama ya.")
            break

        # --- Fitur Belajar ---
        if tanya.startswith("belajar:"):
            try:
                bagian = tanya[len("belajar:"):].strip()
                if "=" in bagian:
                    pertanyaan, jawaban = bagian.split("=", 1)
                    pertanyaan = pertanyaan.strip()
                    jawaban = jawaban.strip()
                    pengetahuan = load_pengetahuan_file()
                    if pertanyaan.lower() in pengetahuan:
                        print(f"Fika: Pengetahuan '{pertanyaan}' sudah ada. Gunakan pertanyaan lain atau edit manual di file.")
                        continue
                    simpan_pengetahuan_file(pertanyaan, jawaban)
                    simpan_riwayat(tanya, f"Belajar: {pertanyaan} = {jawaban}")
                    print(f"Fika: Oke, aku sudah belajar bahwa '{pertanyaan}' = '{jawaban}'.")
                else:
                    print("Fika: Format belajar salah. Contoh: Belajar: ibu kota jepang = tokyo")
            except Exception:
                print("Fika: Gagal belajar. Pastikan formatnya benar.")
            continue

        # --- Fitur Timer & Alarm ---
        if tanya.startswith("timer"):
            match = re.search(r"timer\s+(\d+)\s*(detik|menit|jam)?", tanya)
            if match:
                angka = int(match.group(1))
                satuan = match.group(2) or "detik"
                if satuan == "menit":
                    durasi = angka * 60
                elif satuan == "jam":
                    durasi = angka * 3600
                else:
                    durasi = angka
                print(f"Fika: Timer selama {angka} {satuan} dimulai!")
                threading.Thread(target=timer_cli, args=(durasi,)).start()
            else:
                print("Fika: Format timer salah. Contoh: timer 5 menit")
            continue

        if tanya.startswith("alarm"):
            match = re.search(r"alarm\s+jam\s+(\d{1,2}):(\d{2})", tanya)
            if match:
                jam = int(match.group(1))
                menit = int(match.group(2))
                now = datetime.datetime.now()
                target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
                if target < now:
                    target += datetime.timedelta(days=1)
                def set_alarm_cli(target_time):
                    now = datetime.datetime.now()
                    delta = (target_time - now).total_seconds()
                    if delta > 0:
                        print(f"Fika: Alarm akan berbunyi dalam {int(delta)} detik.")
                        threading.Thread(target=timer_cli, args=(delta, "Alarm!")).start()
                    else:
                        print("Fika: Waktu alarm sudah lewat.")
                set_alarm_cli(target)
                print(f"Fika: Alarm disetel untuk jam {jam:02d}:{menit:02d}.")
            else:
                print("Fika: Format alarm salah. Contoh: alarm jam 06:30")
            continue

        if tanya.startswith("ingatkan aku untuk"):
            match = re.search(r"ingatkan aku untuk (.+) dalam (\d+)\s*(detik|menit|jam)?", tanya)
            if match:
                pesan = match.group(1)
                angka = int(match.group(2))
                satuan = match.group(3) or "detik"
                if satuan == "menit":
                    durasi = angka * 60
                elif satuan == "jam":
                    durasi = angka * 3600
                else:
                    durasi = angka
                threading.Thread(target=timer_cli, args=(durasi, f"Pengingat: {pesan}")).start()
                print(f"Fika: Akan mengingatkan '{pesan}' dalam {angka} {satuan}.")
            else:
                print("Fika: Format pengingat salah. Contoh: ingatkan aku untuk minum air dalam 10 menit")
            continue

        for cek_func in (cek_faktorial, cek_hitung, cek_keyword):
            jawaban = cek_func(tanya)
            if jawaban:
                print("Fika:", jawaban)
                simpan_riwayat(tanya, jawaban)
                break
        else:
            print("Fika: Maaf, aku belum mengerti pertanyaanmu.")
            print(f" {random.choice(saran)} ")

def kalkulator():
    operasi = {
        "1": ("Penjumlahan", lambda a, b: a + b),
        "2": ("Pengurangan", lambda a, b: a - b),
        "3": ("Perkalian", lambda a, b: a * b),
        "4": ("Pembagian", lambda a, b: a / b if b != 0 else "Pembagian dengan nol tidak diperbolehkan."),
        "6": ("Pangkat", lambda a, b: a ** b)
    }
    while True:
        print("\n=== Kalkulator ===")
        print("1. Penjumlahan (+)")
        print("2. Pengurangan (-)")
        print("3. Perkalian (*)")
        print("4. Pembagian (/)")
        print("5. Akar Kuadrat")
        print("6. Pangkat")
        print("7. Kembali ke menu utama")

        pilih = input("Pilih operasi (1-7): ")

        if pilih == "7":
            break

        if pilih in operasi:
            a = input_angka("Masukkan angka pertama: ")
            b = input_angka("Masukkan angka kedua: ")
            hasil = operasi[pilih][1](a, b)
            print(f"Hasil: {hasil}")
        elif pilih == "5":
            a = input_angka("Masukkan angka: ")
            if a < 0:
                print("Tidak bisa menghitung akar kuadrat dari angka negatif.")
            else:
                print(f"Hasil akar kuadrat dari {a} adalah {math.sqrt(a)}")
        else:
            print("Pilihan tidak valid.")

def keliling_persegi():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Keliling Persegi = {4 * sisi}")

def keliling_persegi_panjang():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    print(f"Keliling Persegi Panjang = {2 * (p + l)}")

def keliling_lingkaran():
    r = input_angka("Jari-jari: ")
    print(f"Keliling Lingkaran = {2 * math.pi * r:.2f}")

def keliling_segitiga():
    a = input_angka("Sisi a: ")
    b = input_angka("Sisi b: ")
    c = input_angka("Sisi c: ")
    print(f"Keliling Segitiga = {a + b + c}")

def luas_persegi():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Luas Persegi = {sisi * sisi}")

def luas_persegi_panjang():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    print(f"Luas Persegi Panjang = {p * l}")

def luas_lingkaran():
    r = input_angka("Jari-jari: ")
    print(f"Luas Lingkaran = {math.pi * r * r:.2f}")

def luas_segitiga():
    a = input_angka("Alas: ")
    t = input_angka("Tinggi: ")
    print(f"Luas Segitiga = {0.5 * a * t}")

def volume_kubus():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Volume Kubus = {sisi ** 3}")

def volume_balok():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Balok = {p * l * t}")

def volume_tabung():
    r = input_angka("Jari-jari: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Tabung = {math.pi * r**2 * t:.2f}")

def volume_kerucut():
    r = input_angka("Jari-jari: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Kerucut = {(1/3) * math.pi * r**2 * t:.2f}")

keliling_map = {
    "a": keliling_persegi,
    "b": keliling_persegi_panjang,
    "c": keliling_lingkaran,
    "d": keliling_segitiga
}
luas_map = {
    "a": luas_persegi,
    "b": luas_persegi_panjang,
    "c": luas_lingkaran,
    "d": luas_segitiga
}
volume_map = {
    "a": volume_kubus,
    "b": volume_balok,
    "c": volume_tabung,
    "d": volume_kerucut
}

def geometri():
    while True:
        print("\n=== Geometri ===")
        print("1. Keliling Bangun Datar")
        print("2. Luas Bangun Datar")
        print("3. Volume Bangun Ruang")
        print("4. Kembali ke menu utama")

        pilih = input("Pilih menu (1-4): ")

        if pilih == "4":
            break

        if pilih in ["1", "2", "3"]:
            if pilih == "1":
                print("\nPilih bangun datar:")
                print("a. Persegi")
                print("b. Persegi Panjang")
                print("c. Lingkaran")
                print("d. Segitiga")
                bangun = input("Pilih (a-d): ").lower()
                func = keliling_map.get(bangun)
            elif pilih == "2":
                print("\nPilih bangun datar:")
                print("a. Persegi")
                print("b. Persegi Panjang")
                print("c. Lingkaran")
                print("d. Segitiga")
                bangun = input("Pilih (a-d): ").lower()
                func = luas_map.get(bangun)
            elif pilih == "3":
                print("\nPilih bangun ruang:")
                print("a. Kubus")
                print("b. Balok")
                print("c. Tabung")
                print("d. Kerucut")
                bangun = input("Pilih (a-d): ").lower()
                func = volume_map.get(bangun)
            if func:
                func()
            else:
                print("Pilihan tidak valid.")
        else:
            print("Pilihan tidak valid.")

def editor_teks_cli():
    """Editor teks sederhana berbasis CLI dengan fitur find dan replace."""
    print("\n=== Editor Teks CLI ===")
    print("Ketik path file untuk membuka atau buat file baru.")
    print("Ketik 'kembali' untuk kembali ke menu utama.")
    while True:
        file_path = input("Path file: ").strip()
        if file_path.lower() == "kembali":
            break
        buffer = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    buffer = f.readlines()
                print("--- Isi file ---")
                for idx, line in enumerate(buffer, 1):
                    print(f"{idx:03d}: {line.rstrip()}")
            except Exception as e:
                print(f"Gagal membaca file: {e}")
                continue
        else:
            print("File baru akan dibuat.")

        while True:
            print("\nPerintah: [tambah baris] | find [teks] | replace [teks_lama] [teks_baru] | simpan | batal")
            baris = input("> ")
            if baris.lower() == "simpan":
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines([l if l.endswith('\n') else l+'\n' for l in buffer])
                    print("File berhasil disimpan.")
                except Exception as e:
                    print(f"Gagal menyimpan file: {e}")
                break
            elif baris.lower() == "batal":
                print("Edit dibatalkan.")
                break
            elif baris.lower().startswith("find "):
                cari = baris[5:]
                found = False
                for idx, line in enumerate(buffer, 1):
                    if cari in line:
                        print(f"{idx:03d}: {line.rstrip()}")
                        found = True
                if not found:
                    print("Teks tidak ditemukan.")
            elif baris.lower().startswith("replace "):
                try:
                    _, lama, baru = baris.split(" ", 2)
                    count = 0
                    for i in range(len(buffer)):
                        if lama in buffer[i]:
                            buffer[i] = buffer[i].replace(lama, baru)
                            count += 1
                    print(f"Diganti {count} baris.")
                except Exception:
                    print("Format: replace [teks_lama] [teks_baru]")
            else:
                buffer.append(baris)
        break

def timer_cli(durasi, pesan="Timer selesai!"):
    time.sleep(durasi)
    print(f"\n{pesan}")

def menu_utama():
    while True:
        print("\n=== Menu Utama ===")
        print("1. Tanya Fika")
        print("2. Kalkulator")
        print("3. Geometri")
        print("4. Cuaca Hari Ini")
        print("5. Fakta Teknologi")
        print("6. Fakta Menarik")
        print("7. Lihat Riwayat Tanya Jawab")
        print("8. Pemutar Musik")
        print("9. Keluar")
        print("10. Update Pengetahuan Online")
        print("11. Editor Teks")

        pilih = input("Pilih menu (1-11): ").strip()

        if pilih == "11":
            editor_teks_cli()
        elif pilih == "1":
            tanya_fika()
        elif pilih == "2":
            kalkulator()
        elif pilih == "3":
            geometri()
        elif pilih == "4":
            print(tampilkan_cuaca())
        elif pilih == "5":
            print(tampilkan_fakta())
        elif pilih == "6":
            print(tampilkan_fakta_menarik())
        elif pilih == "7":
            tampilkan_riwayat()
        elif pilih == "8":
            play_music_file()
        elif pilih == "9":
            print("Sampai jumpa, Akiro!")
            break
        elif pilih == "10":
            update_pengetahuan_online()
        else:
            print("Pilihan tidak valid.")

def play_music_file():
    print("\n=== Pemutar Musik Sederhana ===")
    print("Masukkan path file musik (mp3/wav) atau ketik 'kembali' untuk kembali ke menu.")
    while True:
        file_path = input("Path file musik: ").strip()
        if file_path.lower() == "kembali":
            break
        if not os.path.isfile(file_path):
            print("File tidak ditemukan. Coba lagi.")
            continue
        try:
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
            print(f"Memutar musik: {os.path.basename(file_path)}. Tutup aplikasi pemutar untuk memilih lagu lain.")
            break
        except Exception as e:
            print(f"Gagal memutar musik: {e}")

if __name__ == "__main__":
    pastikan_file_json()
    init_db()
    menu_utama()