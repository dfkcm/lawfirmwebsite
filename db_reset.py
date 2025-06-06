import os
from app import app, db
from models import Admin, Settings, User, SocialMedia
from werkzeug.security import generate_password_hash
import datetime

def init_db():
    """Veritabanını sıfırla ve başlangıç verilerini ekle"""
    with app.app_context():
        # Tabloları sil ve yeniden oluştur
        db.drop_all()
        db.create_all()
        
        # Default admin kullanıcısını ekle
        if Admin.query.count() == 0:
            admin = Admin(
                username=os.environ.get("ADMIN_USER", "admin"),
                email="admin@kilinchukuk.com",
                password_hash=generate_password_hash(os.environ.get("ADMIN_PASS", "MS"))
            )
            db.session.add(admin)
            print("Default admin kullanıcısı oluşturuldu.")
        
        # Varsayılan site ayarlarını ekle
        if Settings.query.count() == 0:
            settings = Settings(
                site_name="Kılınç Hukuk",
                site_description="Kılınç Hukuk & Danışmanlık",
                site_keywords="hukuk, avukat, danışmanlık, dava, hukuki yardım",
                site_author="Kılınç Hukuk",
                site_footer="© Kılınç Hukuk & Danışmanlık. Tüm hakları saklıdır.",
                homepage_title="Kılınç Hukuk & Danışmanlık",
                homepage_subtitle="Hukuki Destek",
                homepage_content="Profesyonel hukuk danışmanlığı hizmetleri sunuyoruz.",
                about_title="Hakkımızda",
                about_content="Kılınç Hukuk & Danışmanlık olarak profesyonel hizmet veriyoruz."
            )
            db.session.add(settings)
            print("Default site ayarları oluşturuldu.")
        
        # Varsayılan kullanıcı profilini ekle
        if User.query.count() == 0:
            user = User(
                full_name="Av. Nail Furkan Kılınç",
                description="Avukat ve Hukuk Danışmanı",
                profession="Avukat",
                email="info@kilinchukuk.com",
                phone="+90 555 123 4567"
            )
            db.session.add(user)
            print("Default kullanıcı profili oluşturuldu.")
        
        # Varsayılan sosyal medya bilgilerini ekle
        if SocialMedia.query.count() == 0:
            social = SocialMedia(
                facebook="https://facebook.com/kilinchukuk",
                instagram="https://instagram.com/kilinchukuk",
                twitter="https://twitter.com/kilinchukuk"
            )
            db.session.add(social)
            print("Default sosyal medya bilgileri oluşturuldu.")
        
        db.session.commit()
        print("Veritabanı başarıyla sıfırlandı ve başlangıç verileri eklendi.")

if __name__ == "__main__":
    init_db()