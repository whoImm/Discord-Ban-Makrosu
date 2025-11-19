makro_adi = "Otoban Saniye - 0.3sn Beklemeli"

def komut_calistir(kullanici_id):

    komut = [
        "/ban",
        "tab",
        kullanici_id,
        "enter"
    ]
    
    bekleme_sureleri = [0.3, 0.3, 0.3, 0.3]
    
    return komut, bekleme_sureleri