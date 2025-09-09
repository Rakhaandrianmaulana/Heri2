import os
import sys
import random
import string
import platform
import shutil
import json
import time

# --- Modul Eksternal (Pastikan sudah diinstal) ---
try:
    import psutil
    import requests
    from pyshorteners import Shortener
    import qrcode
    from pytube import YouTube
    from gtts import gTTS
    from playsound import playsound
    from pyfiglet import Figlet
    from tqdm import tqdm
    from colorama import init, Fore, Style
except ImportError as e:
    print(f"Error: Modul '{e.name}' belum terinstal.")
    print("Silakan jalankan perintah ini di terminal Anda:")
    print("pip install psutil requests pyshorteners \"qrcode[pil]\" pytube gTTS playsound==1.2.2 pyfiglet tqdm colorama")
    sys.exit()

# --- Inisialisasi Colorama ---
init(autoreset=True)

# --- Fungsi Utilitas ---
def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Mencetak header untuk setiap tool."""
    print(Fore.GREEN + Style.BRIGHT + f"\n{'='*10} [ {title} ] {'='*10}")

def print_info(key, value):
    """Mencetak baris info dengan format rapi."""
    print(f"{Fore.CYAN}{key:<20}: {Style.BRIGHT}{Fore.WHITE}{value}")

# --- Definisi Fitur-fitur Tools ---

def system_info_tool():
    """Fitur 1: Menampilkan informasi sistem."""
    print_header("System Information")
    try:
        uname = platform.uname()
        print_info("Sistem Operasi", f"{uname.system} {uname.release}")
        print_info("Nama Node", uname.node)
        print_info("Versi", uname.version)
        print_info("Mesin", uname.machine)
        print_info("Prosesor", uname.processor)
        
        # Info CPU
        print_info("Physical Cores", psutil.cpu_count(logical=False))
        print_info("Total Cores", psutil.cpu_count(logical=True))
        print_info("Penggunaan CPU", f"{psutil.cpu_percent()}%")

        # Info RAM
        svmem = psutil.virtual_memory()
        print_info("Total RAM", f"{svmem.total / (1024**3):.2f} GB")
        print_info("RAM Tersedia", f"{svmem.available / (1024**3):.2f} GB")
        print_info("Penggunaan RAM", f"{svmem.percent}%")

    except Exception as e:
        print(Fore.RED + f"Gagal mendapatkan info sistem: {e}")

def weather_tool():
    """Fitur 2: Menampilkan prakiraan cuaca."""
    print_header("Prakiraan Cuaca Real-time")
    city = input(f"{Fore.YELLOW}Masukkan nama kota (contoh: Jakarta): {Style.RESET_ALL}")
    if not city:
        print(Fore.RED + "Nama kota tidak boleh kosong.")
        return
    try:
        # Menggunakan API gratis dari wttr.in (tidak butuh API Key)
        response = requests.get(f'https://wttr.in/{city}?format=j1')
        response.raise_for_status() # Cek jika ada error HTTP
        weather_data = response.json()
        
        current = weather_data['current_condition'][0]
        area = weather_data['nearest_area'][0]

        print_info("Lokasi", f"{area['areaName'][0]['value']}, {area['country'][0]['value']}")
        print_info("Suhu", f"{current['temp_C']}°C (Terasa seperti {current['FeelsLikeC']}°C)")
        print_info("Kondisi", current['weatherDesc'][0]['value'])
        print_info("Kelembapan", f"{current['humidity']}%")
        print_info("Angin", f"{current['windspeedKmph']} km/h")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengambil data cuaca. Periksa koneksi internet atau nama kota. Error: {e}")
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}")

def url_shortener_tool():
    """Fitur 3: Memperpendek URL."""
    print_header("URL Shortener (TinyURL)")
    long_url = input(f"{Fore.YELLOW}Masukkan URL yang ingin dipersingkat: {Style.RESET_ALL}")
    if not long_url:
        print(Fore.RED + "URL tidak boleh kosong.")
        return
    try:
        s = Shortener()
        short_url = s.tinyurl.short(long_url)
        print(Fore.GREEN + Style.BRIGHT + f"\nURL Pendek Anda: {short_url}")
    except Exception as e:
        print(Fore.RED + f"Gagal memperpendek URL. Pastikan URL valid. Error: {e}")

def password_generator_tool():
    """Fitur 4: Membuat password acak yang kuat."""
    print_header("Strong Password Generator")
    try:
        length = int(input(f"{Fore.YELLOW}Masukkan panjang password (min 8): {Style.RESET_ALL}"))
        if length < 8:
            print(Fore.RED + "Panjang minimal adalah 8.")
            return
            
        use_symbols = input(f"{Fore.YELLOW}Gunakan simbol? (y/n): {Style.RESET_ALL}").lower() == 'y'
        use_numbers = input(f"{Fore.YELLOW}Gunakan angka? (y/n): {Style.RESET_ALL}").lower() == 'y'

        chars = string.ascii_letters
        if use_symbols:
            chars += string.punctuation
        if use_numbers:
            chars += string.digits
            
        password = ''.join(random.choice(chars) for _ in range(length))
        print(Fore.GREEN + Style.BRIGHT + f"\nPassword baru Anda: {password}")
    except ValueError:
        print(Fore.RED + "Input panjang harus berupa angka.")
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan: {e}")
        
def qr_code_tool():
    """Fitur 5: Membuat QR Code dari teks atau URL."""
    print_header("Generate QR Code")
    data = input(f"{Fore.YELLOW}Masukkan teks atau URL: {Style.RESET_ALL}")
    filename = input(f"{Fore.YELLOW}Nama file output (contoh: my_qr.png): {Style.RESET_ALL}")

    if not data or not filename:
        print(Fore.RED + "Data dan nama file tidak boleh kosong.")
        return
    if not filename.endswith('.png'):
        filename += '.png'
        
    try:
        img = qrcode.make(data)
        img.save(filename)
        print(Fore.GREEN + Style.BRIGHT + f"\n[+] Sukses! QR Code disimpan sebagai '{filename}'")
        print(Fore.YELLOW + f"Lokasi file: {os.path.abspath(filename)}")
    except Exception as e:
        print(Fore.RED + f"Gagal membuat QR Code: {e}")

def file_organizer_tool():
    """Fitur 6: Merapikan file ke dalam subfolder."""
    print_header("Automatic File Organizer")
    path = input(f"{Fore.YELLOW}Masukkan path folder yang ingin dirapikan (contoh: C:\\Users\\Lana\\Desktop): {Style.RESET_ALL}")
    if not os.path.isdir(path):
        print(Fore.RED + "Path tidak valid atau bukan sebuah folder.")
        return

    EXTENSIONS = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi"],
        "Music": [".mp3", ".wav", ".aac"],
        "Archives": [".zip", ".rar", ".7z", ".tar"],
        "Programs": [".exe", ".msi"]
    }
    
    confirm = input(f"{Fore.RED + Style.BRIGHT}PERINGATAN! Ini akan memindahkan file di '{path}'. Anda yakin? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        print(Fore.YELLOW + "Operasi dibatalkan.")
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            moved = False
            for folder, exts in EXTENSIONS.items():
                if file_ext in exts:
                    dest_folder = os.path.join(path, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, dest_folder)
                    print(f"Memindahkan '{filename}' -> {folder}")
                    moved = True
                    break
    print(Fore.GREEN + Style.BRIGHT + "\nProses merapikan selesai!")

def youtube_downloader_tool():
    """Fitur 7: Mengunduh video dari YouTube."""
    print_header("YouTube Video Downloader")
    url = input(f"{Fore.YELLOW}Masukkan URL video YouTube: {Style.RESET_ALL}")
    if not url:
        print(Fore.RED + "URL tidak boleh kosong.")
        return
    
    try:
        yt = YouTube(url)
        print(f"\n{Fore.CYAN}Judul: {yt.title}")
        print(f"{Fore.CYAN}Durasi: {yt.length // 60} menit {yt.length % 60} detik")
        
        stream = yt.streams.get_highest_resolution()
        print(f"{Fore.YELLOW}Mengunduh dalam resolusi: {stream.resolution}...")

        # Progress bar
        with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc=yt.title, ascii=True) as pbar:
            def progress_function(chunk, file_handle, bytes_remaining):
                pbar.update(len(chunk))
            yt.register_on_progress_callback(progress_function)
            stream.download()

        print(Fore.GREEN + Style.BRIGHT + f"\n[+] Video '{yt.title}' berhasil diunduh!")
        print(Fore.YELLOW + f"Lokasi file: {os.path.abspath(yt.title + '.mp4')}")

    except Exception as e:
        print(Fore.RED + f"Gagal mengunduh video. Error: {e}")

def text_to_speech_tool():
    """Fitur 8: Mengubah teks menjadi suara."""
    print_header("Text to Speech (TTS)")
    text = input(f"{Fore.YELLOW}Masukkan teks yang ingin diubah menjadi suara: {Style.RESET_ALL}")
    lang = input(f"{Fore.YELLOW}Masukkan kode bahasa (contoh: id untuk Indonesia, en untuk English): {Style.RESET_ALL}")
    
    if not text or not lang:
        print(Fore.RED + "Teks dan bahasa tidak boleh kosong.")
        return

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = "output_tts.mp3"
        tts.save(filename)
        print(Fore.GREEN + f"\n[+] Audio disimpan sebagai '{filename}'. Memainkan suara...")
        playsound(filename)
        os.remove(filename) # Hapus file setelah dimainkan
    except Exception as e:
        print(Fore.RED + f"Gagal memproses TTS. Error: {e}")

def ip_info_tool():
    """Fitur 9: Menampilkan info geolokasi dari IP."""
    print_header("IP Geolocation Lookup")
    ip_address = input(f"{Fore.YELLOW}Masukkan alamat IP (kosongkan untuk IP Anda sendiri): {Style.RESET_ALL}")
    
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'success':
            print_info("Alamat IP", data.get('query'))
            print_info("Negara", data.get('country'))
            print_info("Kota", data.get('city'))
            print_info("Wilayah", data.get('regionName'))
            print_info("Zona Waktu", data.get('timezone'))
            print_info("ISP", data.get('isp'))
            print_info("Organisasi", data.get('org'))
        else:
            print(Fore.RED + "Gagal mendapatkan informasi untuk IP tersebut.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal terhubung. Periksa koneksi internet. Error: {e}")

def show_tqto():
    """Menampilkan bagian terima kasih."""
    print(Fore.MAGENTA + "\n" + "~"*30)
    print(Fore.WHITE + Style.BRIGHT + "       Special Thanks To")
    print(Fore.MAGENTA + "~"*30)
    print(Fore.CYAN + "  - Dev: Lana")
    print(Fore.YELLOW + "  - Thanks to God")
    print(Fore.GREEN + "  - My Parents & You!")
    print(Fore.MAGENTA + "~"*30 + "\n")

# --- Fungsi Utama dan Menu ---

def show_menu():
    """Menampilkan menu utama."""
    f = Figlet(font='standard')
    ascii_art = f.renderText('Lana Ultimate')
    print(Fore.CYAN + Style.BRIGHT + ascii_art)
    
    print(Fore.YELLOW + "="*60)
    print(Fore.YELLOW + "             Selamat Datang di Lana Ultimate Tools v4.0")
    print(Fore.YELLOW + "="*60)
    
    # Daftar fitur dalam dua kolom
    features = {
        "1. Info Sistem": "/sysinfo",
        "2. Cuaca": "/weather",
        "3. Shorten URL": "/shorten",
        "4. Gen Password": "/passgen",
        "5. Gen QR Code": "/qrcode",
        "6. Rapikan File": "/organize",
        "7. Unduh YouTube": "/ytdownload",
        "8. Text to Speech": "/tts",
        "9. Info IP": "/ipinfo",
        "10. Thanks To": "/tqto"
    }
    
    items = list(features.items())
    half = len(items) // 2
    
    for i in range(half):
        # Kolom kiri
        left_key = items[i][0]
        left_val = items[i][1]
        
        # Kolom kanan
        right_key = items[i+half][0]
        right_val = items[i+half][1]
        
        print(f"  {Fore.WHITE}{left_key:<18} -> {Fore.GREEN}{left_val:<15} |  {Fore.WHITE}{right_key:<15} -> {Fore.GREEN}{right_val}")
    
    print(Fore.YELLOW + "-"*60)
    print(f"  {Fore.WHITE}{'Menu' :<18} -> {Fore.GREEN}{'/menu' :<15} |  {Fore.WHITE}{'Keluar' :<15} -> {Fore.GREEN}{'/exit'}")
    print(Fore.YELLOW + "="*60 + "\n")

def main():
    """Loop utama program."""
    command_map = {
        "/menu": show_menu,
        "/sysinfo": system_info_tool,
        "/weather": weather_tool,
        "/shorten": url_shortener_tool,
        "/passgen": password_generator_tool,
        "/qrcode": qr_code_tool,
        "/organize": file_organizer_tool,
        "/ytdownload": youtube_downloader_tool,
        "/tts": text_to_speech_tool,
        "/ipinfo": ip_info_tool,
        "/tqto": show_tqto,
    }
    clear_screen()
    show_menu()
    
    while True:
        try:
            prompt = Fore.CYAN + Style.BRIGHT + "lana-ultimate>" + Style.RESET_ALL + " "
            command = input(prompt).strip().lower()

            if command == '/exit':
                print(Fore.CYAN + "Terima kasih telah menggunakan tools ini. Sampai jumpa!")
                sys.exit()
            
            action = command_map.get(command)
            if action:
                action()
            else:
                if command:
                    print(Fore.RED + f"Perintah '{command}' tidak dikenali. Ketik /menu untuk bantuan.")
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n\nProgram dihentikan. Sampai jumpa!")
            sys.exit()
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"\nTerjadi kesalahan yang tidak terduga: {e}\n")


if __name__ == "__main__":
    main()
