#!/usr/bin/env python3
"""
📱 HSD Core Labs - Toplu SMS Gönderici
Netgsm API ile SMS gönderir
"""

import urllib.request
import urllib.parse
import ssl

# ==========================================
# ⚙️ NETGSM API AYARLARI
# ==========================================
NETGSM_USERNAME = "8503047798"
NETGSM_PASSWORD = "874.3C4"
NETGSM_SENDER = "HSDCORELABS"
NETGSM_URL = "https://api.netgsm.com.tr/sms/send/get"

# ==========================================
# 📄 PDF LİNKİ
# ==========================================
PDF_LINK = "https://drive.google.com/drive/folders/1iDBSTrXz0H32oSynDUEdMtSiQ0ZZojse?usp=sharing"

# ==========================================
# 📞 TELEFON NUMARALARI (buraya ekle)
# ==========================================
PHONE_NUMBERS = [
    "05434486660",
    # Diğer numaraları buraya ekle:
    # "05321234567",
    # "05551234567",
]

# ==========================================
# ✉️ MESAJ İÇERİĞİ
# ==========================================
MESSAGE = f"""Merhaba,

Belgeleriniz hazır! Aşağıdaki linkten erişebilirsiniz:

📄 {PDF_LINK}

İçerik:
- Analiz.pdf
- Terapi Planı.pdf
- Transkripsiyon.pdf
- Vaka Formülasyonu.pdf

Saygılarımızla,
HSD Core Labs"""

# ==========================================
# 🚀 SMS GÖNDER
# ==========================================
def send_sms(phone, message):
    """Tek bir SMS gönderir"""
    params = {
        'usercode': NETGSM_USERNAME,
        'password': NETGSM_PASSWORD,
        'gsmno': phone,
        'message': message,
        'msgheader': NETGSM_SENDER
    }
    
    url = f"{NETGSM_URL}?{urllib.parse.urlencode(params)}"
    
    # SSL sertifika doğrulamasını atla (gerekirse)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        response = urllib.request.urlopen(url, context=context)
        result = response.read().decode('utf-8')
        return result
    except Exception as e:
        return f"HATA: {str(e)}"

def parse_result(result):
    """Netgsm yanıtını parse et"""
    if result.startswith("00"):
        return True, "Başarılı"
    elif result.startswith("01"):
        return False, "Geçersiz kullanıcı adı/şifre"
    elif result.startswith("20"):
        return False, "Mesaj metni boş"
    elif result.startswith("30"):
        return False, "Geçersiz numara"
    elif result.startswith("40"):
        return False, "Başlık hatalı"
    elif result.startswith("70"):
        return False, "Parametre hatası"
    else:
        return False, f"Bilinmeyen hata: {result}"

def main():
    print("=" * 50)
    print("📱 HSD CORE LABS - TOPLU SMS GÖNDERİCİ")
    print("=" * 50)
    print()
    print(f"📄 Gönderilecek link: {PDF_LINK[:50]}...")
    print(f"📞 Toplam numara: {len(PHONE_NUMBERS)}")
    print(f"✉️ Mesaj uzunluğu: {len(MESSAGE)} karakter")
    print()
    
    # Onay iste
    confirm = input("🚀 Göndermek için ENTER'a bas (iptal için 'q'): ")
    if confirm.lower() == 'q':
        print("❌ İptal edildi.")
        return
    
    print()
    print("📤 Gönderiliyor...")
    print("-" * 50)
    
    success = 0
    failed = 0
    
    for i, phone in enumerate(PHONE_NUMBERS, 1):
        # Numarayı temizle
        clean_phone = ''.join(filter(str.isdigit, phone))
        if not clean_phone.startswith('0'):
            clean_phone = '0' + clean_phone
        
        print(f"[{i}/{len(PHONE_NUMBERS)}] {clean_phone}... ", end="")
        
        result = send_sms(clean_phone, MESSAGE)
        is_success, message = parse_result(result)
        
        if is_success:
            print(f"✅ {message}")
            success += 1
        else:
            print(f"❌ {message}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"📊 SONUÇ: {success} başarılı, {failed} başarısız")
    print("=" * 50)

if __name__ == "__main__":
    main()

