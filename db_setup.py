import os
from app import app, db
from models import Admin, Settings, User, SocialMedia
from werkzeug.security import generate_password_hash
import sqlite3

def setup_db():
    with app.app_context():
        # Tabloları sil ve yeniden oluştur
        db.drop_all()
        db.create_all()
        
        # Default admin kullanıcısını ekle
        admin = Admin()
        admin.username = os.environ.get("ADMIN_USER", "admin")
        admin.email = "admin@kilinchukuk.com"
        admin.password_hash = generate_password_hash(os.environ.get("ADMIN_PASS", "MS"))
        db.session.add(admin)
        
        # Varsayılan site ayarlarını ekle
        settings = Settings()
        settings.site_name = "Kılınç Hukuk"
        settings.site_description = "Kılınç Hukuk & Danışmanlık"
        settings.site_keywords = "hukuk, avukat, danışmanlık, dava, hukuki yardım"
        settings.site_author = "Kılınç Hukuk"
        settings.site_footer = "© Kılınç Hukuk & Danışmanlık. Tüm hakları saklıdır."
        settings.homepage_title = "Kılınç Hukuk & Danışmanlık"
        settings.homepage_subtitle = "Hukuki Destek"
        settings.homepage_content = "Profesyonel hukuk danışmanlığı hizmetleri sunuyoruz."
        settings.about_title = "Hakkımızda"
        settings.about_content = "Kılınç Hukuk & Danışmanlık olarak profesyonel hizmet veriyoruz."
        db.session.add(settings)
        
        # Varsayılan kullanıcı profilini ekle
        user = User()
        user.full_name = "Av. Nail Furkan Kılınç"
        user.description = "Avukat ve Hukuk Danışmanı"
        user.profession = "Avukat"
        user.email = "info@kilinchukuk.com"
        user.phone = "+90 555 123 4567"
        db.session.add(user)
        
        # Varsayılan sosyal medya bilgilerini ekle
        social = SocialMedia()
        social.facebook = "https://facebook.com/kilinchukuk"
        social.instagram = "https://instagram.com/kilinchukuk"
        social.twitter = "https://twitter.com/kilinchukuk"
        db.session.add(social)
        
        # Değişiklikleri kaydet
        db.session.commit()
        print("Veritabanı başarıyla kuruldu ve varsayılan veriler eklendi.")

    conn = sqlite3.connect('instance/portfolio.db')
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE iletisim ADD COLUMN ip_address VARCHAR(45);")
        print('ip_address sütunu eklendi.')
    except Exception as e:
        print('Zaten var veya hata:', e)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_db()