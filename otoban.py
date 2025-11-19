import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import importlib.util
import threading
import time
import keyboard
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from PIL import Image, ImageTk
import sys
import tempfile

class OtobanApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Discord Otomatik Ban Makrosu")
        self.root.geometry("650x750")
        self.root.configure(bg='#2b2b2b')

        self.root.attributes('-topmost', False)
        self.arkaplan = '#2b2b2b'
        self.card_arkaplan = '#3c3f41'
        self.yazi_rengi = '#ffffff'
        self.buton_rengi = '#4CAF50'
        self.buton_hover = '#45a049'
        self.buton_durdur = '#f44336'
        self.buton_durdur_hover = '#da190b'
        self.buton_hazirlik = '#FF9800'
        self.buton_hazirlik_hover = '#F57C00'
        self.macrolar = {}
        self.secili_makro = None
        self.calistiriliyor = False
        self.hazirlik_asamasi = False
        self.thread = None
        self.mevcut_sayfa = "ana"
        self.json_dosya = "otoban.json"
        self.sunucular_klasor = "sunucular"
        self.kullanici_id_listesi = self.json_yukle()
        self.macrolari_yukle()
        self.stil_ayarla()
        self.pencere_ikonu_ayarla()
        self.arayuz_olustur()

    def pencere_ikonu_ayarla(self):
        try:
            logo_yolu = os.path.join(self.sunucular_klasor, "logo.png")
            if os.path.exists(logo_yolu):
                print(f"Logo bulundu: {logo_yolu}")
                icon = Image.open(logo_yolu)
                photo = ImageTk.PhotoImage(icon)
                self.root.iconphoto(True, photo)
                self.root._icon = photo
                if os.name == 'nt':
                    self.windows_taskbar_ikonu_ayarla(logo_yolu)
                print("Logo başarıyla yüklendi")
                return True
            else:
                print(f"Logo dosyası bulunamadı: {logo_yolu}")
                logo_yolu = "logo.png"
                if os.path.exists(logo_yolu):
                    icon = Image.open(logo_yolu)
                    photo = ImageTk.PhotoImage(icon)
                    self.root.iconphoto(True, photo)
                    self.root._icon = photo
                    print("Logo mevcut dizinden yüklendi")
                    return True
        except Exception as e:
            print(f"İkon yüklenirken hata: {e}")
        self.varsayilan_ikon_olustur()
        return False
    def windows_taskbar_ikonu_ayarla(self, logo_yolu):
        try:
            import ctypes
            from ctypes import wintypes
            icon = Image.open(logo_yolu)
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
            icon_images = []
            
            for size in icon_sizes:
                resized_icon = icon.resize(size, Image.Resampling.LANCZOS)
                icon_images.append(resized_icon)

            temp_dir = tempfile.gettempdir()
            ico_yolu = os.path.join(temp_dir, "discord_otoban_icon.ico")

            icon_images[0].save(ico_yolu, format='ICO', sizes=[(size[0], size[1]) for size in icon_sizes])
            try:
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                app_id = "DiscordOtoBan.v1.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
                ico_handle = ctypes.windll.user32.LoadImageW(
                    0, ico_yolu, 1, 0, 0, 0x00000010
                )
                if ico_handle:
                    WM_SETICON = 0x0080
                    ICON_SMALL = 0
                    ICON_BIG = 1
                    
                    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, ico_handle)
                    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, ico_handle)
                    
                    print("Taskbar ikonu başarıyla ayarlandı")
                else:
                    print("Taskbar ikonu yüklenemedi")
                    
            except Exception as e:
                print(f"Windows API hatası: {e}")
                
        except Exception as e:
            print(f"Taskbar ikonu ayarlanırken hata: {e}")
    
    def varsayilan_ikon_olustur(self):
        try:
            from PIL import Image, ImageDraw
            icon = Image.new('RGBA', (64, 64), (43, 43, 43, 255))
            draw = ImageDraw.Draw(icon)
            draw.ellipse([10, 10, 54, 54], fill=(76, 175, 80, 255))
            draw.text((24, 18), "B", fill=(255, 255, 255, 255), font_size=24)
            photo = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, photo)
            self.root._icon = photo
            print("Varsayılan ikon oluşturuldu")
        except Exception as e:
            print(f"Varsayılan ikon oluşturulurken hata: {e}")
    def stil_ayarla(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=self.arkaplan, foreground=self.yazi_rengi)
        style.configure('TLabel', background=self.arkaplan, foreground=self.yazi_rengi, font=('Arial', 10))
        style.configure('TButton', background=self.buton_rengi, foreground=self.yazi_rengi, 
                       font=('Arial', 10, 'bold'), borderwidth=0, focuscolor='none')
        style.map('TButton', background=[('active', self.buton_hover)])
        style.configure('TFrame', background=self.arkaplan)
        style.configure('TLabelframe', background=self.arkaplan, foreground=self.yazi_rengi)
        style.configure('TLabelframe.Label', background=self.arkaplan, foreground=self.yazi_rengi)
        style.configure('TEntry', fieldbackground=self.card_arkaplan, foreground=self.yazi_rengi, 
                       insertcolor=self.yazi_rengi)
        style.configure('TCombobox', fieldbackground=self.card_arkaplan, foreground=self.yazi_rengi, 
                       background=self.card_arkaplan)
        style.configure('TSpinbox', fieldbackground=self.card_arkaplan, foreground=self.yazi_rengi)
        style.configure('TScrollbar', background=self.card_arkaplan)
    def json_yukle(self):
        try:
            if os.path.exists(self.json_dosya):
                with open(self.json_dosya, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"JSON yükleme hatası: {e}")
            return []
    def json_kaydet(self):
        try:
            with open(self.json_dosya, 'w', encoding='utf-8') as f:
                json.dump(self.kullanici_id_listesi, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"JSON kaydetme hatası: {e}")
    def macrolari_yukle(self):
        if not os.path.exists(self.sunucular_klasor):
            os.makedirs(self.sunucular_klasor)
        for dosya in os.listdir(self.sunucular_klasor):
            if dosya.endswith('.py'):
                makro_adi = dosya[:-3]
                try:
                    modul_yolu = os.path.join(self.sunucular_klasor, dosya)
                    spec = importlib.util.spec_from_file_location(makro_adi, modul_yolu)
                    modul = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modul)
                    if hasattr(modul, 'makro_adi'):
                        self.macrolar[makro_adi] = {
                            'modul': modul,
                            'adi': modul.makro_adi
                        }
                except Exception as e:
                    print(f"{dosya} yüklenirken hata: {e}")
    def arayuz_olustur(self):
        self.ozel_baslik_cubugu_olustur()
        self.ana_container = ttk.Frame(self.root)
        self.ana_container.pack(fill=tk.BOTH, expand=True)
        
        self.ana_sayfa_olustur()
        self.bilgi_sayfasi_olustur()
        self.sayfa_goster("ana")
    
    def ozel_baslik_cubugu_olustur(self):
        try:
            self.root.overrideredirect(True)
            self.baslik_cubugu = tk.Frame(self.root, bg='#1e1e1e', height=35)
            self.baslik_cubugu.pack(fill=tk.X, side=tk.TOP)
            self.baslik_cubugu.pack_propagate(False)
            baslik_label = tk.Label(self.baslik_cubugu, text="Discord Otomatik Ban Makrosu", 
                                   font=('Arial', 10), 
                                   bg='#1e1e1e', fg='#ffffff')
            baslik_label.pack(side=tk.LEFT, padx=12, pady=8)
            
            kontrol_frame = tk.Frame(self.baslik_cubugu, bg='#1e1e1e')
            kontrol_frame.pack(side=tk.RIGHT)
            
            kucult_buton = tk.Button(kontrol_frame, text="─", 
                                    font=('Arial', 12, 'bold'),
                                    bg='#1e1e1e', fg='#ffffff',
                                    relief='flat', width=3,
                                    command=self.root.iconify, cursor='hand2')
            kucult_buton.pack(side=tk.LEFT)
            
            kapat_buton = tk.Button(kontrol_frame, text="×", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#1e1e1e', fg='#ffffff',
                                   relief='flat', width=3,
                                   command=self.root.quit, cursor='hand2')
            kapat_buton.pack(side=tk.LEFT)
            
            def buton_hover(event, button, hover_color='#333333'):
                button.configure(bg=hover_color)
            
            def buton_leave(event, button):
                button.configure(bg='#1e1e1e')
            
            kucult_buton.bind("<Enter>", lambda e: buton_hover(e, kucult_buton, '#2a2a2a'))
            kucult_buton.bind("<Leave>", lambda e: buton_leave(e, kucult_buton))
            kapat_buton.bind("<Enter>", lambda e: buton_hover(e, kapat_buton, '#e81123'))
            kapat_buton.bind("<Leave>", lambda e: buton_leave(e, kapat_buton))

            def baslik_surukle_basla(event):
                self.baslik_surukle_x = event.x_root
                self.baslik_surukle_y = event.y_root
                self.pencere_konum_x = self.root.winfo_x()
                self.pencere_konum_y = self.root.winfo_y()
            
            def baslik_surukle(event):
                x = self.pencere_konum_x + (event.x_root - self.baslik_surukle_x)
                y = self.pencere_konum_y + (event.y_root - self.baslik_surukle_y)
                self.root.geometry(f"+{x}+{y}")
            
            self.baslik_cubugu.bind("<Button-1>", baslik_surukle_basla)
            self.baslik_cubugu.bind("<B1-Motion>", baslik_surukle)
            baslik_label.bind("<Button-1>", baslik_surukle_basla)
            baslik_label.bind("<B1-Motion>", baslik_surukle)
            
        except Exception as e:
            print(f"Özel başlık çubuğu oluşturulurken hata: {e}")
            self.root.overrideredirect(False)
    
    def ana_sayfa_olustur(self):
        self.ana_sayfa = ttk.Frame(self.ana_container)

        ust_cubuk_frame = ttk.Frame(self.ana_sayfa)
        ust_cubuk_frame.pack(fill=tk.X, padx=20, pady=15)

        self.bilgi_butonu = tk.Button(ust_cubuk_frame, text="?", 
                                     font=('Arial', 14, 'bold'),
                                     bg='#555555', fg='white',
                                     relief='flat', width=3,
                                     command=lambda: self.sayfa_goster("bilgi"), cursor='hand2')
        self.bilgi_butonu.pack(side=tk.LEFT)

        baslik_label = tk.Label(ust_cubuk_frame, text="DISCORD OTO BAN MAKROSU", 
                               font=('Arial', 16, 'bold'), 
                               bg=self.arkaplan, fg=self.yazi_rengi)
        baslik_label.pack(side=tk.LEFT, expand=True)

        bos_alan = ttk.Frame(ust_cubuk_frame, width=35)
        bos_alan.pack(side=tk.RIGHT)

        uyari_frame = ttk.Frame(self.ana_sayfa)
        uyari_frame.pack(fill=tk.X, padx=20, pady=5)
        
        uyari_label = tk.Label(uyari_frame, text="Başlat butonuna bastıktan sonra 3 saniye içinde Discord'un gerekli yerine tıklayın!", 
                              font=('Arial', 10, 'italic'), 
                              bg=self.arkaplan, fg='#FF9800')
        uyari_label.pack()

        icerik_frame = ttk.Frame(self.ana_sayfa)
        icerik_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        sol_frame = ttk.LabelFrame(icerik_frame, text=" MAKRO KONTROLLERİ ", padding="15")
        sol_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        makro_sec_frame = ttk.Frame(sol_frame)
        makro_sec_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(makro_sec_frame, text="Makro Seçin:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        self.makro_combobox = ttk.Combobox(makro_sec_frame, values=list(self.macrolar.keys()), 
                                          font=('Arial', 10), height=15)
        self.makro_combobox.pack(fill=tk.X, pady=5)
        self.makro_combobox.bind('<<ComboboxSelected>>', self.makro_secildi)

        hiz_frame = ttk.Frame(sol_frame)
        hiz_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(hiz_frame, text="Ban Aralığı (saniye):", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        
        hiz_icerik_frame = ttk.Frame(hiz_frame)
        hiz_icerik_frame.pack(fill=tk.X, pady=5)
        
        self.hiz_var = tk.StringVar(value="1")
        hiz_spinbox = ttk.Spinbox(hiz_icerik_frame, from_=0.5, to=10, increment=0.5, 
                                 textvariable=self.hiz_var, width=10, font=('Arial', 10))
        hiz_spinbox.pack(side=tk.LEFT)
        
        ttk.Label(hiz_icerik_frame, text="saniye").pack(side=tk.LEFT, padx=(5, 0))
        buton_frame = ttk.Frame(sol_frame)
        buton_frame.pack(fill=tk.X, pady=20)
        
        self.baslat_buton = tk.Button(buton_frame, text="MAKROYU BAŞLAT", 
                                     font=('Arial', 12, 'bold'),
                                     bg=self.buton_hazirlik, fg='white',
                                     relief='flat', padx=20, pady=10,
                                     command=self.baslat, cursor='hand2')
        self.baslat_buton.pack(fill=tk.X, pady=5)
        
        self.durdur_buton = tk.Button(buton_frame, text="DURDUR", 
                                     font=('Arial', 12, 'bold'),
                                     bg=self.buton_durdur, fg='white',
                                     relief='flat', padx=20, pady=10,
                                     command=self.durdur, state=tk.DISABLED, cursor='hand2')
        self.durdur_buton.pack(fill=tk.X, pady=5)
        
        durum_frame = ttk.Frame(sol_frame)
        durum_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(durum_frame, text="Durum:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.durum_label = ttk.Label(durum_frame, text="Hazır", font=('Arial', 10))
        self.durum_label.pack(anchor=tk.W, pady=(5, 0))
        self.geri_sayim_label = ttk.Label(durum_frame, text="", font=('Arial', 12, 'bold'), foreground='#FF9800')
        self.geri_sayim_label.pack(anchor=tk.W, pady=(5, 0))
        istatistik_frame = ttk.Frame(sol_frame)
        istatistik_frame.pack(fill=tk.X, pady=10)
        ttk.Label(istatistik_frame, text="İstatistikler:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        self.toplam_label = ttk.Label(istatistik_frame, text=f"Toplam ID: {len(self.kullanici_id_listesi)}", 
                                     font=('Arial', 10))
        self.toplam_label.pack(anchor=tk.W, pady=(2, 0))
        self.islenen_label = ttk.Label(istatistik_frame, text="İşlenen: 0", font=('Arial', 10))
        self.islenen_label.pack(anchor=tk.W, pady=(2, 0))
        sag_frame = ttk.LabelFrame(icerik_frame, text=" KULLANICI ID YÖNETİMİ ", padding="15")
        sag_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        id_ekle_frame = ttk.Frame(sag_frame)
        id_ekle_frame.pack(fill=tk.X, pady=10)
        ttk.Label(id_ekle_frame, text="Yeni Kullanıcı ID Ekle:", font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        id_giris_frame = ttk.Frame(id_ekle_frame)
        id_giris_frame.pack(fill=tk.X, pady=8)
        self.id_entry = ttk.Entry(id_giris_frame, font=('Arial', 11))
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.id_entry.bind('<Return>', self.id_ekle)
        ekle_buton = tk.Button(id_giris_frame, text="EKLE", 
                              font=('Arial', 10, 'bold'),
                              bg=self.buton_rengi, fg='white',
                              relief='flat', padx=15,
                              command=self.id_ekle, cursor='hand2')
        ekle_buton.pack(side=tk.RIGHT)
        liste_baslik_frame = ttk.Frame(sag_frame)
        liste_baslik_frame.pack(fill=tk.X, pady=(20, 5))
        ttk.Label(liste_baslik_frame, text="Ban Listesi:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT)
        sil_buton = tk.Button(liste_baslik_frame, text="Seçileni Sil", 
                             font=('Arial', 9, 'bold'),
                             bg=self.buton_durdur, fg='white',
                             relief='flat', padx=10,
                             command=self.id_sil, cursor='hand2')
        sil_buton.pack(side=tk.RIGHT)
        liste_cerceve = ttk.Frame(sag_frame)
        liste_cerceve.pack(fill=tk.BOTH, expand=True, pady=5)
        self.liste_kutusu = tk.Listbox(liste_cerceve, bg=self.card_arkaplan, fg=self.yazi_rengi,
                                      selectbackground=self.buton_rengi, selectforeground='white',
                                      font=('Arial', 10), relief='flat', bd=0)
        scrollbar = ttk.Scrollbar(liste_cerceve, orient=tk.VERTICAL, command=self.liste_kutusu.yview)
        self.liste_kutusu.configure(yscrollcommand=scrollbar.set)
        self.liste_kutusu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.liste_guncelle()
        self.buton_hover_efektleri()
    def bilgi_sayfasi_olustur(self):
        self.bilgi_sayfasi = ttk.Frame(self.ana_container)
        ust_cubuk_frame = ttk.Frame(self.bilgi_sayfasi)
        ust_cubuk_frame.pack(fill=tk.X, padx=20, pady=15)
        geri_buton = tk.Button(ust_cubuk_frame, text="←", 
                              font=('Arial', 14, 'bold'),
                              bg='#555555', fg='white',
                              relief='flat', width=3,
                              command=lambda: self.sayfa_goster("ana"), cursor='hand2')
        geri_buton.pack(side=tk.LEFT)
        baslik_label = tk.Label(ust_cubuk_frame, text="UYGULAMA BİLGİLERİ", 
                               font=('Arial', 16, 'bold'), 
                               bg=self.arkaplan, fg=self.yazi_rengi)
        baslik_label.pack(side=tk.LEFT, expand=True)
        bos_alan = ttk.Frame(ust_cubuk_frame, width=35)
        bos_alan.pack(side=tk.RIGHT)
        bilgi_icerik_frame = ttk.Frame(self.bilgi_sayfasi, padding="20")
        bilgi_icerik_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        bilgiler = [
            ("Uygulama Adı", "Discord Otomatik Ban Makrosu"),
            ("Sürüm", "v1.0"),
            ("Geliştirici", "palyac0"),
            ("Discord", "palyac0"),
            ("GitHub", "whoImm"),
            ("Lisans", "MIT License"),
        ]
        
        for i, (baslik, icerik) in enumerate(bilgiler):
            baslik_label = tk.Label(bilgi_icerik_frame, text=baslik, 
                                   font=('Arial', 12, 'bold'),
                                   bg=self.arkaplan, fg=self.yazi_rengi,
                                   anchor='w')
            baslik_label.grid(row=i, column=0, sticky='ew', pady=10, padx=(0, 20))
            icerik_label = tk.Label(bilgi_icerik_frame, text=icerik,
                                   font=('Arial', 11),
                                   bg=self.arkaplan, fg='#CCCCCC',
                                   anchor='w')
            icerik_label.grid(row=i, column=1, sticky='ew', pady=10)

        aciklama_frame = ttk.Frame(bilgi_icerik_frame)
        aciklama_frame.grid(row=len(bilgiler), column=0, columnspan=2, sticky='ew', pady=20)
        
        aciklama_text = """Bu uygulama Discord sunucularında otomatik ban işlemi yapmak için geliştirilmiştir. 
Kullanmadan önce sunucu'un kurallarını okuduğunuzdan emin olun."""
        
        aciklama_label = tk.Label(aciklama_frame, text=aciklama_text,
                                font=('Arial', 10, 'italic'),
                                bg=self.arkaplan, fg='#FF9800',
                                justify=tk.LEFT, wraplength=500)
        aciklama_label.pack(anchor='w')
    
    def sayfa_goster(self, sayfa_adi):
        if self.mevcut_sayfa == "ana":
            self.ana_sayfa.pack_forget()
        elif self.mevcut_sayfa == "bilgi":
            self.bilgi_sayfasi.pack_forget()
        
        if sayfa_adi == "ana":
            self.ana_sayfa.pack(fill=tk.BOTH, expand=True)
            self.mevcut_sayfa = "ana"
        elif sayfa_adi == "bilgi":
            self.bilgi_sayfasi.pack(fill=tk.BOTH, expand=True)
            self.mevcut_sayfa = "bilgi"
    
    def buton_hover_efektleri(self):
        def on_enter(event):
            if event.widget['state'] == tk.NORMAL:
                if event.widget == self.baslat_buton:
                    event.widget.configure(bg=self.buton_hazirlik_hover)
                elif event.widget == self.durdur_buton:
                    event.widget.configure(bg=self.buton_durdur_hover)
                elif event.widget == self.bilgi_butonu:
                    event.widget.configure(bg='#777777')
        
        def on_leave(event):
            if event.widget['state'] == tk.NORMAL:
                if event.widget == self.baslat_buton:
                    event.widget.configure(bg=self.buton_hazirlik)
                elif event.widget == self.durdur_buton:
                    event.widget.configure(bg=self.buton_durdur)
                elif event.widget == self.bilgi_butonu:
                    event.widget.configure(bg='#555555')
        
        self.baslat_buton.bind("<Enter>", on_enter)
        self.baslat_buton.bind("<Leave>", on_leave)
        self.durdur_buton.bind("<Enter>", on_enter)
        self.durdur_buton.bind("<Leave>", on_leave)
        self.bilgi_butonu.bind("<Enter>", on_enter)
        self.bilgi_butonu.bind("<Leave>", on_leave)
    
    def liste_guncelle(self):
        self.liste_kutusu.delete(0, tk.END)
        for kullanici_id in self.kullanici_id_listesi:
            self.liste_kutusu.insert(tk.END, kullanici_id)
        self.toplam_label.config(text=f"Toplam ID: {len(self.kullanici_id_listesi)}")
    
    def makro_secildi(self, event):
        self.secili_makro = self.makro_combobox.get()
        if self.secili_makro in self.macrolar:
            self.durum_label.config(text=f"Durum: {self.macrolar[self.secili_makro]['adi']} seçildi")
    
    def id_ekle(self, event=None):
        kullanici_id = self.id_entry.get().strip()
        if kullanici_id:
            if kullanici_id not in self.kullanici_id_listesi:
                self.kullanici_id_listesi.append(kullanici_id)
                self.json_kaydet()
                self.liste_guncelle()
                self.id_entry.delete(0, tk.END)
                messagebox.showinfo("Başarılı", "Kullanıcı ID eklendi!")
            else:
                messagebox.showwarning("Uyarı", "Bu ID zaten listede var!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir ID girin!")
    
    def id_sil(self):
        secili = self.liste_kutusu.curselection()
        if secili:
            index = secili[0]
            silinecek_id = self.kullanici_id_listesi[index]
            self.kullanici_id_listesi.pop(index)
            self.json_kaydet()
            self.liste_guncelle()
            messagebox.showinfo("Başarılı", f"{silinecek_id} ID'si silindi!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir ID seçin!")
    
    def baslat(self):
        if not self.secili_makro:
            messagebox.showwarning("Uyarı", "Lütfen önce bir makro seçin!")
            return
        
        if not self.kullanici_id_listesi:
            messagebox.showwarning("Uyarı", "Banlanacak kullanıcı ID'si yok!")
            return
        
        self.hazirlik_asamasi = True
        self.baslat_buton.config(state=tk.DISABLED, bg='#666666')
        self.durum_label.config(text="Durum: Hazırlık modu - Discord'a tıklayın!")
        hazirlik_thread = threading.Thread(target=self.hazirlik_geri_sayim)
        hazirlik_thread.daemon = True
        hazirlik_thread.start()
    
    def hazirlik_geri_sayim(self):
        for i in range(3, 0, -1):
            if not self.hazirlik_asamasi:
                break
                
            self.root.after(0, lambda x=i: self.geri_sayim_label.config(text=f"Kalan: {x} saniye"))
            time.sleep(1)
        
        if self.hazirlik_asamasi:
            self.root.after(0, self.geri_sayim_label.config, {"text": "Makro başlıyor!"})
            time.sleep(0.5)
            self.root.after(0, self.makroyu_baslat)
    
    def makroyu_baslat(self):
        try:
            hiz = float(self.hiz_var.get())
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçersiz hız değeri!")
            return
        
        self.calistiriliyor = True
        self.hazirlik_asamasi = False
        self.durdur_buton.config(state=tk.NORMAL, bg=self.buton_durdur)
        self.durum_label.config(text="Durum: Çalışıyor...")
        self.geri_sayim_label.config(text="")
        self.islenen_label.config(text="İşlenen: 0")
        self.thread = threading.Thread(target=self.makro_calistir, args=(hiz,))
        self.thread.daemon = True
        self.thread.start()
    
    def durdur(self):
        self.calistiriliyor = False
        self.hazirlik_asamasi = False
        self.baslat_buton.config(state=tk.NORMAL, bg=self.buton_hazirlik)
        self.durdur_buton.config(state=tk.DISABLED, bg='#666666')
        self.durum_label.config(text="Durum: Durduruldu")
        self.geri_sayim_label.config(text="")
    
    def makro_calistir(self, hiz):
        keyboard_controller = Controller()
        islenen_sayisi = 0
        
        for kullanici_id in self.kullanici_id_listesi:
            if not self.calistiriliyor:
                break
                
            try:
                makro_modul = self.macrolar[self.secili_makro]['modul']
                sonuc = makro_modul.komut_calistir(kullanici_id)
                
                if isinstance(sonuc, tuple) and len(sonuc) == 2:
                    komut, bekleme_sureleri = sonuc
                else:
                    komut = sonuc
                    bekleme_sureleri = [0.5] * len(komut)
                for i, tus in enumerate(komut):
                    if not self.calistiriliyor:
                        break
                        
                    if tus == "tab":
                        keyboard_controller.press(Key.tab)
                        keyboard_controller.release(Key.tab)
                    elif tus == "enter":
                        keyboard_controller.press(Key.enter)
                        keyboard_controller.release(Key.enter)
                    else:
                        keyboard.write(tus)
                    if i < len(bekleme_sureleri):
                        time.sleep(bekleme_sureleri[i])
                    else:
                        time.sleep(0.5)
                
                islenen_sayisi += 1
                self.root.after(0, lambda: self.islenen_label.config(text=f"İşlenen: {islenen_sayisi}"))
                
                if self.calistiriliyor:
                    time.sleep(hiz)
                
            except Exception as e:
                print(f"Makro çalıştırma hatası: {e}")
        self.root.after(0, self.makro_tamamlandi)
    
    def makro_tamamlandi(self):
        self.calistiriliyor = False
        self.baslat_buton.config(state=tk.NORMAL, bg=self.buton_hazirlik)
        self.durdur_buton.config(state=tk.DISABLED, bg='#666666')
        self.durum_label.config(text="Durum: Tamamlandı")
        self.geri_sayim_label.config(text="")
        messagebox.showinfo("Tamamlandı", "Tüm ban işlemleri tamamlandı!")
    
    def run(self):
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()
