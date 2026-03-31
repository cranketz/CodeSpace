import random
import heapq
import os

# Graphviz'i hata almadan içe aktarmayı deniyoruz
try:
    import graphviz
    GRAPHVIZ_KURULU = True
except ImportError:
    GRAPHVIZ_KURULU = False

# Hedef durum sabitimiz (0 boşluğu temsil eder)
HEDEF_DURUM = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Ekrana ve dosyaya aynı anda yazdıran yardımcı fonksiyon
def logla(metin, dosya):
    print(metin)
    if dosya:
        dosya.write(metin + "\n")

def masaustu_yolunu_bul():
    """Kullanıcının işletim sistemine göre Masaüstü klasörünün yolunu bulur."""
    kullanici_dizini = os.path.expanduser("~")
    olasi_yollar = [
        os.path.join(kullanici_dizini, "Desktop"),
        os.path.join(kullanici_dizini, "Masaüstü"),
        os.path.join(kullanici_dizini, "OneDrive", "Desktop"),
        os.path.join(kullanici_dizini, "OneDrive", "Masaüstü")
    ]
    for yol in olasi_yollar:
        if os.path.exists(yol):
            return yol
    return kullanici_dizini

def cozulebilir_mi(durum):
    inversion_sayisi = 0
    durum_kopyasi = [x for x in durum if x != 0] 
    for i in range(len(durum_kopyasi)):
        for j in range(i + 1, len(durum_kopyasi)):
            if durum_kopyasi[i] > durum_kopyasi[j]:
                inversion_sayisi += 1
    return inversion_sayisi % 2 == 0

def rastgele_cozulebilir_durum_olustur():
    while True:
        baslangic = list(HEDEF_DURUM)
        random.shuffle(baslangic)
        if cozulebilir_mi(baslangic):
            return tuple(baslangic)

def ayarlari_belirle():
    print("-" * 50)
    print("8-TAŞ (8-PUZZLE) YAPAY ZEKA ÇÖZÜCÜ")
    print("-" * 50)
    print("1. Varsayılan (Rastgele Çözülebilir Başlangıç)")
    print("2. Kendi başlangıç konumumu girmek istiyorum")
    
    secim = input("\nSeçiminiz (1/2): ").strip()
    
    if secim == '1':
        return rastgele_cozulebilir_durum_olustur()
        
    elif secim == '2':
        print("\nLütfen 0'dan 8'e kadar olan 9 rakamı aralarında boşluk bırakarak girin.")
        print("Örnek (0 boşluğu temsil eder): 1 2 3 4 0 5 6 7 8")
        
        while True:
            kullanici_girisi = input("\nBaşlangıç konumu: ").strip().split()
            if len(kullanici_girisi) != 9:
                print("[HATA] Lütfen tam olarak 9 adet rakam girin!")
                continue
            try:
                baslangic_konumu = tuple(int(x) for x in kullanici_girisi)
                if set(baslangic_konumu) != set(range(9)):
                    print("[HATA] Rakamları (0-8) birer kez kullanın!")
                    continue
                if not cozulebilir_mi(baslangic_konumu):
                    print("[UYARI] Girdiğiniz bu dizilim matematiksel olarak ÇÖZÜLEMEZ!")
                    if input("Yine de denemek istiyor musunuz? (e/h): ").strip().lower() != 'e':
                        continue
                return baslangic_konumu
            except ValueError:
                print("[HATA] Lütfen sadece rakam girin!")
    else:
        print("\n[UYARI] Geçersiz seçim! Varsayılan ayarlarla başlatılıyor...")
        return rastgele_cozulebilir_durum_olustur()

def manhattan_mesafesi(durum):
    mesafe = 0
    for i in range(9):
        deger = durum[i]
        if deger != 0:
            hedef_index = HEDEF_DURUM.index(deger)
            mevcut_satir, mevcut_sutun = divmod(i, 3)
            hedef_satir, hedef_sutun = divmod(hedef_index, 3)
            mesafe += abs(mevcut_satir - hedef_satir) + abs(mevcut_sutun - hedef_sutun)
    return mesafe

def komsulari_bul(durum):
    komsular = []
    bosluk_index = durum.index(0)
    satir, sutun = divmod(bosluk_index, 3)
    
    hareketler = {
        'Yukarı': (satir - 1, sutun),
        'Aşağı': (satir + 1, sutun),
        'Sola': (satir, sutun - 1),
        'Sağa': (satir, sutun + 1)
    }
    
    for yon, (yeni_satir, yeni_sutun) in hareketler.items():
        if 0 <= yeni_satir < 3 and 0 <= yeni_sutun < 3:
            yeni_index = yeni_satir * 3 + yeni_sutun
            yeni_durum = list(durum)
            yeni_durum[bosluk_index], yeni_durum[yeni_index] = yeni_durum[yeni_index], yeni_durum[bosluk_index]
            komsular.append((yon, tuple(yeni_durum)))
            
    return komsular

def a_yildiz_coz(baslangic):
    sayac = 0 
    kuyruk = []
    heapq.heappush(kuyruk, (manhattan_mesafesi(baslangic), sayac, 0, baslangic, []))
    ziyaret_edilenler = set()
    
    while kuyruk:
        f, _, g, mevcut_durum, yol = heapq.heappop(kuyruk)
        
        if mevcut_durum == HEDEF_DURUM:
            return yol + [(None, mevcut_durum)]
            
        if mevcut_durum in ziyaret_edilenler:
            continue
            
        ziyaret_edilenler.add(mevcut_durum)
        
        for yon, komsu_durum in komsulari_bul(mevcut_durum):
            if komsu_durum not in ziyaret_edilenler:
                sayac += 1
                yeni_g = g + 1
                yeni_f = yeni_g + manhattan_mesafesi(komsu_durum)
                yeni_yol = yol + [(yon, mevcut_durum)]
                heapq.heappush(kuyruk, (yeni_f, sayac, yeni_g, komsu_durum, yeni_yol))
                
    return None

def matris_olustur(durum):
    """Durumu 3x3 formatında string olarak döndürür."""
    sonuc = ""
    for i in range(0, 9, 3):
        satir = durum[i:i+3]
        sonuc += "  ".join(str(x) if x != 0 else "_" for x in satir) + "\n"
    return sonuc

# --- YENİ: GRAPHVIZ AĞAÇ ÇİZİM FONKSİYONU ---
def agac_ciz(ilk_durum, cozum_yolu, kayit_klasoru):
    if not GRAPHVIZ_KURULU:
        print("\n[UYARI] Graphviz Python kütüphanesi bulunamadı. Ağaç çizimi atlanıyor.")
        return None

    # Eşaralıklı font (Courier New) kullanarak matrislerin hizasını koruyoruz
    dot = graphviz.Digraph(comment='8-Tas Arama Agaci', format='png')
    dot.attr(node='box', fontname='Courier New', fontsize='12')

    def node_id(durum):
        return "".join(str(x) for x in durum)

    # Başlangıç düğümünü ekle (Mavi)
    dot.node(node_id(ilk_durum), matris_olustur(ilk_durum), style='filled', fillcolor='#add8e6')

    onceki_durum = ilk_durum

    for yon, yeni_durum in cozum_yolu:
        if yon is None:
            continue

        olasi_hamleler = komsulari_bul(onceki_durum)
        for olasi_yon, olasi_durum in olasi_hamleler:
            id_onceki = node_id(onceki_durum)
            id_olasi = node_id(olasi_durum)

            # Doğru hamleyi Yeşil, kalın ok ile çiz
            if olasi_durum == yeni_durum:
                dot.node(id_olasi, matris_olustur(olasi_durum), style='filled', fillcolor='#90ee90')
                dot.edge(id_onceki, id_olasi, label=olasi_yon, color='green', penwidth='2.0')
            # Seçilmeyen alternatif dalları Gri, kesik çizgili ok ile çiz
            else:
                dot.node(id_olasi, matris_olustur(olasi_durum), style='filled', fillcolor='#f0f0f0', fontcolor='#808080')
                dot.edge(id_onceki, id_olasi, label=olasi_yon, color='gray', style='dashed')

        onceki_durum = yeni_durum

    # Hedef durumu Altın Sarısı yap
    dot.node(node_id(HEDEF_DURUM), matris_olustur(HEDEF_DURUM), style='filled', fillcolor='#ffd700', penwidth='2.0')

    dosya_ismi = os.path.join(kayit_klasoru, "cozum_agaci")
    try:
        # cleanup=True diyerek arka planda oluşan .gv gereksiz dosyasını otomatik sildiriyoruz
        dot.render(dosya_ismi, view=False, cleanup=True)
        return dosya_ismi + ".png"
    except graphviz.backend.ExecutableNotFound:
        print("\n[HATA] Graphviz kurulu ama sistem PATH ayarlarında bulunamadı!")
        print("Lütfen Graphviz'in ana programını kurduğundan ve Ortam Değişkenlerine eklediğinden emin ol.")
        return None

# --- ANA PROGRAM ---
if __name__ == "__main__":
    ilk_durum = ayarlari_belirle()
    
    masaustu_yolu = masaustu_yolunu_bul()
    txt_dosya_yolu = os.path.join(masaustu_yolu, "cozum_raporu.txt")
    
    print("\n[BİLGİ] Çözüm aranıyor, lütfen bekleyin...\n")
    cozum_yolu = a_yildiz_coz(ilk_durum)
    
    with open(txt_dosya_yolu, "w", encoding="utf-8") as rapor_dosyasi:
        logla("=" * 40, rapor_dosyasi)
        logla("8-TAŞ BULMACASI ÇÖZÜM RAPORU", rapor_dosyasi)
        logla("=" * 40 + "\n", rapor_dosyasi)
        
        logla("--- BAŞLANGIÇ DURUMU ---", rapor_dosyasi)
        logla(matris_olustur(ilk_durum), rapor_dosyasi)
        
        if cozum_yolu:
            logla(f"[BAŞARILI] Çözüm toplam {len(cozum_yolu) - 1} adımda bulundu!\n", rapor_dosyasi)
            
            adim_sayisi = 1
            onceki_durum = ilk_durum
            
            for yon, yeni_durum in cozum_yolu:
                if yon is not None:
                    logla("*" * 40, rapor_dosyasi)
                    logla(f"ADIM {adim_sayisi}:", rapor_dosyasi)
                    logla("DEĞERLENDİRİLEN OLASI HAMLELER VE MATRİSLERİ:", rapor_dosyasi)
                    
                    olasi_hamleler = komsulari_bul(onceki_durum)
                    for olasi_yon, olasi_durum in olasi_hamleler:
                        logla(f"-> Boşluk '{olasi_yon}' yönüne giderse:", rapor_dosyasi)
                        logla(matris_olustur(olasi_durum), rapor_dosyasi)
                        
                    logla("-" * 40, rapor_dosyasi)
                    logla(f"*** SEÇİLEN HAMLE: Boşluk '{yon}' yönüne hareket etti. ***", rapor_dosyasi)
                    logla("Oluşan Yeni Durum Matrisi:", rapor_dosyasi)
                    logla(matris_olustur(yeni_durum), rapor_dosyasi)
                    
                    onceki_durum = yeni_durum
                    adim_sayisi += 1
                    
            logla("*" * 40, rapor_dosyasi)
            logla("\n*** HEDEF DURUMA ULAŞILDI! ***", rapor_dosyasi)
            logla(matris_olustur(HEDEF_DURUM), rapor_dosyasi)
            
            # Kodun raporlama kısmı bitince ağaç çizim fonksiyonunu tetikliyoruz
            agac_yolu = agac_ciz(ilk_durum, cozum_yolu, masaustu_yolu)
            
        else:
            logla("[BAŞARISIZ] Bu dizilim için bir çözüm bulunamadı.", rapor_dosyasi)

    print(f"\n[SİSTEM] Tüm çözüm adımları başarıyla Masaüstüne kaydedildi:")
    print(f"📄 Metin Raporu: {txt_dosya_yolu}")
    if cozum_yolu and GRAPHVIZ_KURULU:
        print(f"🖼️ Görsel Ağaç:  {agac_yolu}")