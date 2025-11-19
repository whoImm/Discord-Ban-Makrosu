import os
import sys
import subprocess
import importlib.util
import tkinter as tk
from tkinter import messagebox

def paket_kontrol(paket_adi):
    try:
        spec = importlib.util.find_spec(paket_adi)
        return spec is not None
    except ImportError:
        return False

def paket_kur(paket_adi):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", paket_adi])
        return True
    except subprocess.CalledProcessError:
        return False

def gerekli_paketleri_kontrol_et():
    gerekli_paketler = [
        "pynput",
        "keyboard", 
        "Pillow"
    ]
    
    eksik_paketler = []
    
    for paket in gerekli_paketler:
        if not paket_kontrol(paket):
            eksik_paketler.append(paket)
    
    return eksik_paketler

def kurulum_yap():
    eksik_paketler = gerekli_paketleri_kontrol_et()
    
    if not eksik_paketler:
        return True

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleWindow()
    except:
        pass
    
    print("Eksik paketler tespit edildi. Kurulum başlatılıyor...")
    print("Kurulacak paketler:", ", ".join(eksik_paketler))
    print("Lütfen bekleyin...")
    
    basarili = []
    basarisiz = []
    
    for paket in eksik_paketler:
        print(f"{paket} kuruluyor...")
        if paket_kur(paket):
            basarili.append(paket)
            print(f"✓ {paket} başarıyla kuruldu")
        else:
            basarisiz.append(paket)
            print(f"✗ {paket} kurulumu başarısız")
    
    if basarisiz:
        print("\nBazı paketler kurulamadı:")
        for paket in basarisiz:
            print(f"  - {paket}")

        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Kurulum Hatası", 
                f"Şu paketler kurulamadı: {', '.join(basarisiz)}\n\n"
                "Lütfen Manuel Kurulum Yapın:\n"
                "1. Komut istemini açın (cmd)\n"
                "2. Şu komutu çalıştırın:\n"
                "pip install pynput keyboard Pillow"
            )
            root.destroy()
        except:
            pass
        
        return False
    
    print("\n✓ Tüm paketler başarıyla kuruldu!")
    return True

def main_programi_baslat():
    try:
        from main import OtobanApp
        app = OtobanApp()
        app.run()
    except Exception as e:
        print(f"Program başlatılırken hata: {e}")
        input("Çıkmak için bir tuşa basın...")

if __name__ == "__main__":
    if kurulum_yap():
        print("Ana program başlatılıyor...")
        main_programi_baslat()
    else:
        print("Kurulum tamamlanamadı. Lütfen manuel kurulum yapın.")
        input("Çıkmak için bir tuşa basın...")