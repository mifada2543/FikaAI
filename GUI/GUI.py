import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, scrolledtext
import json
import os
import datetime
import threading
import time
import random
import pygame

# Inisialisasi pygame mixer hanya sekali!
try:
    pygame.mixer.init()
except Exception as e:
    print("Peringatan: Gagal inisialisasi audio:", e)

# --- Utility & Data ---
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

def pastikan_file_json():
    for fname, default in [
        ("pengetahuan.json", {}),
        ("fakta_menarik.json", []),
        ("preset_fika.json", {})
    ]:
        if not os.path.exists(fname):
            save_json(fname, default)

def baca_preset():
    return load_json("preset_fika.json", {})

def simpan_preset(nama, tipe, data):
    preset = baca_preset()
    preset[nama] = {"tipe": tipe, "data": data}
    save_json("preset_fika.json", preset)

def load_pengetahuan_file():
    return load_json("pengetahuan.json", {})

def tampilkan_fakta_menarik():
    fakta_list = load_json("fakta_menarik.json", [])
    if not fakta_list:
        return "Belum ada fakta menarik."
    return "Fakta menarik hari ini:\n" + random.choice(fakta_list)

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

# --- Musik ---
playlist = []
playlist_index = [0]
current_music_file = [None]

def tambah_ke_playlist(file_paths):
    for path in file_paths:
        if path and os.path.isfile(path):
            playlist.append(path)

def putar_lagu_playlist(index):
    if 0 <= index < len(playlist):
        try:
            pygame.mixer.music.load(playlist[index])
            pygame.mixer.music.play()
            current_music_file[0] = playlist[index]
            return True
        except Exception:
            return False
    return False

def lagu_selanjutnya():
    if playlist:
        playlist_index[0] = (playlist_index[0] + 1) % len(playlist)
        putar_lagu_playlist(playlist_index[0])

def lagu_sebelumnya():
    if playlist:
        playlist_index[0] = (playlist_index[0] - 1) % len(playlist)
        putar_lagu_playlist(playlist_index[0])

# --- GUI ---
def main():
    pastikan_file_json()
    root = tk.Tk()
    root.title("Fika Chatbot")
    root.configure(bg="#e3f2fd")

    # --- Tema ---
    theme_mode = ["light"]
    def set_theme(mode="light"):
        if mode == "dark":
            root.configure(bg="#23272e")
            chat_area.configure(bg="#23272e", fg="#f8f8f2", insertbackground="#f8f8f2")
            countdown_label.configure(bg="#23272e", fg="#ffb86c")
            frame.configure(bg="#23272e")
            entry.configure(bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2")
            fitur_frame.configure(bg="#23272e")
            preset_frame.configure(bg="#23272e")
            music_frame.configure(bg="#23272e")
            status_lbl.configure(bg="#23272e", fg="#ffb86c")
        else:
            root.configure(bg="#e3f2fd")
            chat_area.configure(bg="#f5f5f5", fg="#222", insertbackground="#222")
            countdown_label.configure(bg="#e3f2fd", fg="#d32f2f")
            frame.configure(bg="#e3f2fd")
            entry.configure(bg="white", fg="#222", insertbackground="#222")
            fitur_frame.configure(bg="#e3f2fd")
            preset_frame.configure(bg="#e3f2fd")
            music_frame.configure(bg="#e3f2fd")
            status_lbl.configure(bg="#e3f2fd", fg="#333")

    def toggle_theme():
        theme_mode[0] = "dark" if theme_mode[0] == "light" else "light"
        set_theme(theme_mode[0])

    # --- Countdown ---
    countdown_var = tk.StringVar(value="")
    countdown_label = tk.Label(root, textvariable=countdown_var, font=("Segoe UI", 12, "bold"), fg="#d32f2f", bg="#e3f2fd")
    countdown_label.pack()

    # --- Chat Area ---
    chat_area = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled', wrap=tk.WORD, font=("Consolas", 11), bg="#f5f5f5")
    chat_area.pack(padx=10, pady=10)

    # --- Input ---
    frame = tk.Frame(root, bg="#e3f2fd")
    frame.pack(padx=10, pady=(0,10), fill='x')
    entry = tk.Entry(frame, width=45, font=("Segoe UI", 11))
    entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0,5))
    entry.focus()

    # --- Timer/Alarm/Pengingat State ---
    timer_active = [False]
    pengingat_active = [False]
    alarm_active = [False]

    def update_countdown(sisa):
        if sisa > 0:
            jam = sisa // 3600
            menit = (sisa % 3600) // 60
            detik = sisa % 60
            countdown_var.set(f"Sisa waktu: {jam:02d}:{menit:02d}:{detik:02d}")
        else:
            countdown_var.set("")

    # --- Timer, Alarm, Pengingat ---
    def set_timer_gui(durasi, pesan="Timer selesai!", repeat=False):
        if timer_active[0]:
            messagebox.showwarning("Timer", "Sudah ada timer aktif!")
            return
        timer_active[0] = True
        def timer_thread():
            sisa = durasi
            while sisa > 0:
                update_countdown(sisa)
                time.sleep(1)
                sisa -= 1
            update_countdown(0)
            messagebox.showinfo("Timer/Pengingat", pesan)
            timer_active[0] = False
            if repeat:
                set_timer_gui(durasi, pesan, repeat=True)
        threading.Thread(target=timer_thread, daemon=True).start()

    def set_pengingat_gui(durasi, pesan="Pengingat!", repeat=False):
        if pengingat_active[0]:
            messagebox.showwarning("Pengingat", "Sudah ada pengingat aktif!")
            return
        pengingat_active[0] = True
        def pengingat_thread():
            sisa = durasi
            while sisa > 0:
                update_countdown(sisa)
                time.sleep(1)
                sisa -= 1
            update_countdown(0)
            messagebox.showinfo("Pengingat", pesan)
            pengingat_active[0] = False
            if repeat:
                set_pengingat_gui(durasi, pesan, repeat=True)
        threading.Thread(target=pengingat_thread, daemon=True).start()

    def set_alarm_gui(target_time, pesan="Alarm!", repeat=False):
        if alarm_active[0]:
            messagebox.showwarning("Alarm", "Sudah ada alarm aktif!")
            return
        alarm_active[0] = True
        def alarm_thread():
            while True:
                now = datetime.datetime.now()
                sisa = int((target_time - now).total_seconds())
                if sisa > 0:
                    update_countdown(sisa)
                    time.sleep(1)
                else:
                    break
            update_countdown(0)
            messagebox.showinfo("Alarm", pesan)
            alarm_active[0] = False
            if repeat:
                next_time = target_time + datetime.timedelta(days=1)
                set_alarm_gui(next_time, pesan, repeat=True)
        threading.Thread(target=alarm_thread, daemon=True).start()

    # --- Logic Tanya Fika ---
    def lagu_sedang_diputar():
        if current_music_file[0]:
            return f"Lagu yang sedang diputar: {os.path.basename(current_music_file[0])}"
        else:
            return "Tidak ada lagu yang sedang diputar."

    def tanya_fika_logic(tanya):
        tanya = tanya.lower()
        if tanya.startswith("belajar:"):
            try:
                bagian = tanya[len("belajar:"):].strip()
                if "=" in bagian:
                    pertanyaan, jawaban = bagian.split("=", 1)
                    pertanyaan = pertanyaan.strip()
                    jawaban = jawaban.strip()
                    pengetahuan = load_pengetahuan_file()
                    if pertanyaan.lower() in pengetahuan:
                        return f"Pengetahuan '{pertanyaan}' sudah ada. Gunakan pertanyaan lain atau edit manual di file."
                    pengetahuan[pertanyaan.lower()] = jawaban
                    save_json("pengetahuan.json", pengetahuan)
                    return f"Oke, aku sudah belajar bahwa '{pertanyaan}' = '{jawaban}'."
                else:
                    return "Format belajar salah. Contoh: Belajar: ibu kota jepang = tokyo"
            except Exception:
                return "Gagal belajar. Pastikan formatnya benar."

        # Saran untuk user (letakkan sebelum def tanya_fika_logic)
        saran_gui = [
            "Coba 'help' untuk bantuan.",
            "Coba tanya tentang faktorial misal '5!'",
            "Hitung matematika seperti '2+3*4', atau fakta teknologi.",
            "Tanya teknologi seputar smartphone, atau soal geometri.",
            "Tanya apa yang Fika bisa lakukan.",
            "Tanya 'Fika bisa apa'.",
            "Tanya 'spek vivo v21 5g'.",
            "Tanya presiden Indonesia, ibukota Indonesia, atau gravitasi.",
            "Tanya tentang fotosintesis, komputer, atau halo.",
            "Tanya spesifikasi smartphone seperti 'spek vivo v21 5g'.",
            "Atau jika ingin keluar, tutup aplikasi ini."
        ]

        # Deteksi pertanyaan tentang lagu/musik yang sedang diputar
        if any(k in tanya for k in [
            "lagu apa yang sedang diputar",
            "musik apa yang sedang diputar",
            "apa yang sedang diputar",
            "judul lagu yang diputar",
            "lagu sekarang",
            "lagu apa ini"
        ]):
            return lagu_sedang_diputar()

        if tanya.startswith("timer"):
            import re
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
                set_timer_gui(durasi)
                return f"Timer selama {angka} {satuan} dimulai!"
            else:
                return "Format timer salah. Contoh: timer 5 menit"
        if tanya.startswith("alarm"):
            import re
            match = re.search(r"alarm\s+jam\s+(\d{1,2}):(\d{2})", tanya)
            if match:
                jam = int(match.group(1))
                menit = int(match.group(2))
                now = datetime.datetime.now()
                target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
                if target < now:
                    target += datetime.timedelta(days=1)
                set_alarm_gui(target)
                return f"Alarm disetel untuk jam {jam:02d}:{menit:02d}."
            else:
                return "Format alarm salah. Contoh: alarm jam 06:30"
        if tanya.startswith("ingatkan aku untuk"):
            import re
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
                set_pengingat_gui(durasi, f"Pengingat: {pesan}")
                return f"Akan mengingatkan '{pesan}' dalam {angka} {satuan}."
            else:
                return "Format pengingat salah. Contoh: ingatkan aku untuk minum air dalam 10 menit"
        pengetahuan = load_pengetahuan_file()
        for kunci, jawaban in pengetahuan.items():
            if kunci.lower() in tanya:
                return jawaban
        return (
            "Maaf, aku belum mengerti pertanyaanmu.\n"
            + random.choice(saran_gui)
        )

    # --- Kirim Pesan ---
    def kirim():
        user_input = entry.get().strip()
        if not user_input:
            return
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Kamu: {user_input}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)
        entry.delete(0, tk.END)
        jawaban = tanya_fika_logic(user_input)
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika: {jawaban}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    send_btn = tk.Button(frame, text="Kirim", command=kirim, bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold"))
    send_btn.pack(side=tk.LEFT)

    # --- Fitur Lain ---
    def tampilkan_fakta_gui():
        fakta = tampilkan_fakta_menarik()
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika (Fakta Menarik): {fakta}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    def tampilkan_cuaca_gui():
        cuaca = tampilkan_cuaca()
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika (Cuaca): {cuaca}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    def tampilkan_fakta_tek_gui():
        fakta = tampilkan_fakta()
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika (Fakta Teknologi): {fakta}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    # --- Editor Teks GUI ---
    def buka_editor_teks_gui():
        win = tk.Toplevel(root)
        win.title("Editor Teks")
        win.geometry("600x400")
        text_area = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 11), bg="#f5f5f5")
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        def load_file():
            file_path = filedialog.askopenfilename(
                title="Buka File",
                filetypes=[("Teks", "*.txt"), ("Semua File", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text_area.delete(1.0, tk.END)
                        text_area.insert(tk.END, f.read())
                    win.title(f"Editor Teks - {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal membuka file: {e}")
        def save_file():
            file_path = filedialog.asksaveasfilename(
                title="Simpan File",
                defaultextension=".txt",
                filetypes=[("Teks", "*.txt"), ("Semua File", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(text_area.get(1.0, tk.END))
                    win.title(f"Editor Teks - {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Gagal menyimpan file: {e}")
        def find_text():
            cari = simpledialog.askstring("Find", "Cari teks:")
            if cari:
                text_area.tag_remove('found', '1.0', tk.END)
                idx = '1.0'
                found = False
                while True:
                    idx = text_area.search(cari, idx, nocase=1, stopindex=tk.END)
                    if not idx:
                        break
                    lastidx = f"{idx}+{len(cari)}c"
                    text_area.tag_add('found', idx, lastidx)
                    idx = lastidx
                    found = True
                text_area.tag_config('found', background='yellow')
                if not found:
                    messagebox.showinfo("Find", "Teks tidak ditemukan.")
        def replace_text():
            cari = simpledialog.askstring("Find", "Cari teks:")
            if not cari:
                return
            ganti = simpledialog.askstring("Replace", "Ganti dengan:")
            if ganti is None:
                return
            content = text_area.get("1.0", tk.END)
            baru = content.replace(cari, ganti)
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", baru)
            messagebox.showinfo("Replace", f"Semua '{cari}' diganti dengan '{ganti}'.")
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Buka File", command=load_file, bg="#1976d2", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Simpan File", command=save_file, bg="#388e3c", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Find", command=find_text, bg="#ffb300", fg="black").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Find & Replace", command=replace_text, bg="#ff7043", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Tutup", command=win.destroy, bg="#d32f2f", fg="white").pack(side=tk.LEFT, padx=5)

    # --- Preset Timer/Alarm ---
    def pilih_preset_timer():
        preset = baca_preset()
        items = [k for k, v in preset.items() if v["tipe"] == "timer"]
        if not items:
            messagebox.showinfo("Preset Timer", "Belum ada preset timer.")
            return
        pilih = simpledialog.askstring("Preset Timer", "Nama preset:\n" + "\n".join(items))
        if pilih and pilih in preset:
            data = preset[pilih]["data"]
            angka = data["angka"]
            satuan = data["satuan"]
            if satuan == "menit":
                durasi = angka * 60
            elif satuan == "jam":
                durasi = angka * 3600
            else:
                durasi = angka
            set_timer_gui(durasi)
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Timer preset '{pilih}' selama {angka} {satuan} dimulai!\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
    def pilih_preset_alarm():
        preset = baca_preset()
        items = [k for k, v in preset.items() if v["tipe"] == "alarm"]
        if not items:
            messagebox.showinfo("Preset Alarm", "Belum ada preset alarm.")
            return
        pilih = simpledialog.askstring("Preset Alarm", "Nama preset:\n" + "\n".join(items))
        if pilih and pilih in preset:
            data = preset[pilih]["data"]
            jam = data["jam"]
            menit = data["menit"]
            now = datetime.datetime.now()
            target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
            if target < now:
                target += datetime.timedelta(days=1)
            set_alarm_gui(target)
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Alarm preset '{pilih}' disetel untuk jam {jam:02d}:{menit:02d}.\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

    # --- Tombol-tombol utama ---
    # --- Dialog Timer ---
    def buka_timer():
        durasi = simpledialog.askinteger("Timer", "Masukkan durasi timer (dalam detik):", minvalue=1)
        if durasi:
            set_timer_gui(durasi)
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Timer selama {durasi} detik dimulai!\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

    fitur_frame = tk.Frame(root, bg="#e3f2fd")
    fitur_frame.pack(pady=(0,10))

    def buka_pengingat():
        durasi = simpledialog.askinteger("Pengingat", "Masukkan durasi pengingat (dalam detik):", minvalue=1)
        if durasi:
            pesan = simpledialog.askstring("Pengingat", "Pesan pengingat:", initialvalue="Pengingat!")
            if not pesan:
                pesan = "Pengingat!"
            set_pengingat_gui(durasi, pesan)
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Pengingat '{pesan}' dalam {durasi} detik dimulai!\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

    def buka_alarm():
        jam = simpledialog.askinteger("Alarm", "Jam alarm (0-23):", minvalue=0, maxvalue=23)
        if jam is not None:
            menit = simpledialog.askinteger("Alarm", "Menit alarm (0-59):", minvalue=0, maxvalue=59)
            if menit is not None:
                pesan = simpledialog.askstring("Alarm", "Pesan alarm:", initialvalue="Alarm!")
                if not pesan:
                    pesan = "Alarm!"
                now = datetime.datetime.now()
                target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
                if target < now:
                    target += datetime.timedelta(days=1)
                set_alarm_gui(target, pesan)
                chat_area.config(state='normal')
                chat_area.insert(tk.END, f"Fika: Alarm '{pesan}' disetel untuk jam {jam:02d}:{menit:02d}.\n")
                chat_area.config(state='disabled')
                chat_area.see(tk.END)

    tk.Button(fitur_frame, text="⏲️ Timer", command=lambda: buka_timer(), bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="🔔 Pengingat", command=lambda: buka_pengingat(), bg="#388e3c", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="⏰ Alarm", command=lambda: buka_alarm(), bg="#fbc02d", fg="black", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="📝 Editor Teks", command=buka_editor_teks_gui, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="🌦️ Cuaca", command=tampilkan_cuaca_gui, bg="#039be5", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="💡 Fakta Teknologi", command=tampilkan_fakta_tek_gui, bg="#43a047", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(fitur_frame, text="🎲 Fakta Menarik", command=tampilkan_fakta_gui, bg="#8e24aa", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

    preset_frame = tk.Frame(root, bg="#e3f2fd")
    preset_frame.pack(pady=(0,10))
    tk.Button(preset_frame, text="⏲️ Pilih Preset Timer", command=pilih_preset_timer, bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(preset_frame, text="⏰ Pilih Preset Alarm", command=pilih_preset_alarm, bg="#fbc02d", fg="black", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

    # --- Pemutar Musik Native ---
    music_status = tk.StringVar(value="Tidak ada musik yang diputar.")

    def pilih_dan_tambah_playlist():
        file_paths = filedialog.askopenfilenames(
            title="Pilih file musik (bisa lebih dari satu)",
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"), ("Semua File", "*.*")]
        )
        tambah_ke_playlist(file_paths)
        if playlist:
            music_status.set(f"Playlist: {len(playlist)} lagu. Klik ▶️ untuk mulai.")
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: {len(file_paths)} lagu ditambahkan ke playlist.\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

    def putar_playlist():
        if not playlist:
            music_status.set("Playlist kosong.")
            return
        if putar_lagu_playlist(playlist_index[0]):
            music_status.set(f"Memutar: {os.path.basename(playlist[playlist_index[0]])} ({playlist_index[0]+1}/{len(playlist)})")
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Memutar musik: {os.path.basename(playlist[playlist_index[0]])}\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
        else:
            music_status.set("Gagal memutar lagu.")

    def pause_musik():
        pygame.mixer.music.pause()
        music_status.set("Musik dijeda.")

    def lanjut_musik():
        pygame.mixer.music.unpause()
        if playlist:
            music_status.set(f"Memutar: {os.path.basename(playlist[playlist_index[0]])} ({playlist_index[0]+1}/{len(playlist)})")

    def stop_musik():
        pygame.mixer.music.stop()
        music_status.set("Tidak ada musik yang diputar.")
        current_music_file[0] = None

    def next_musik():
        if playlist:
            lagu_selanjutnya()
            putar_playlist()

    def prev_musik():
        if playlist:
            lagu_sebelumnya()
            putar_playlist()

    music_frame = tk.Frame(root, bg="#e3f2fd")
    music_frame.pack(pady=(0,10))

    add_btn = tk.Button(music_frame, text="➕ Tambah Lagu", command=pilih_dan_tambah_playlist, bg="#009688", fg="white", font=("Segoe UI", 10, "bold"))
    add_btn.pack(side=tk.LEFT, padx=2)
    play_btn = tk.Button(music_frame, text="▶️ Mainkan", command=putar_playlist, bg="#43a047", fg="white", font=("Segoe UI", 10, "bold"))
    play_btn.pack(side=tk.LEFT, padx=2)
    pause_btn = tk.Button(music_frame, text="⏸️ Pause", command=pause_musik, bg="#fbc02d", fg="black", font=("Segoe UI", 10, "bold"))
    pause_btn.pack(side=tk.LEFT, padx=2)
    lanjut_btn = tk.Button(music_frame, text="▶️ Lanjut", command=lanjut_musik, bg="#0288d1", fg="white", font=("Segoe UI", 10, "bold"))
    lanjut_btn.pack(side=tk.LEFT, padx=2)
    prev_btn = tk.Button(music_frame, text="⏮️ Prev", command=prev_musik, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold"))
    prev_btn.pack(side=tk.LEFT, padx=2)
    next_btn = tk.Button(music_frame, text="⏭️ Next", command=next_musik, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold"))
    next_btn.pack(side=tk.LEFT, padx=2)
    stop_btn = tk.Button(music_frame, text="⏹️ Stop", command=stop_musik, bg="#d32f2f", fg="white", font=("Segoe UI", 10, "bold"))
    stop_btn.pack(side=tk.LEFT, padx=2)
    status_lbl = tk.Label(music_frame, textvariable=music_status, bg="#e3f2fd", fg="#333", font=("Segoe UI", 10, "italic"))
    status_lbl.pack(side=tk.LEFT, padx=10)

    theme_btn = tk.Button(root, text="🌗 Ganti Tema", command=toggle_theme, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold"))
    theme_btn.pack(pady=(0,10))

    set_theme(theme_mode[0])
    root.bind('<Return>', lambda event: kirim())
    root.mainloop()

if __name__ == "__main__":
    main()