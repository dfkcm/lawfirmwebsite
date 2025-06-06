# Kılınç Hukuk ve Danışmanlık Web Sitesi

Bu proje, Kılınç Hukuk ve Danışmanlık için Flask tabanlı bir web sitesi ve içerik yönetim sistemidir.

## Kurulum

1. Gerekli paketleri yükleyin:
```
pip install -r requirements.txt
```

2. Veritabanını oluşturun:
```
python db_setup.py
```

3. Uygulamayı çalıştırın:
```
python main.py
```

4. Tarayıcınızda `http://localhost:5000` adresine gidin.

## Admin Paneline Erişim

- URL: `http://localhost:5000/admin`
- Kullanıcı adı: `admin`
- Şifre: `MS`

## Özellikler

- Responsive tasarım
- Admin paneli üzerinden içerik yönetimi
- Hizmetler, makaleler ve uzmanlar için yönetim arayüzü
- İletişim formu ve mesaj yönetimi
- SEO dostu yapı

## Notlar

- `.env` dosyasını kendi veritabanı bağlantı bilgilerinizle güncelleyin
- Yerel geliştirme için SQLite veritabanı, canlı ortam için PostgreSQL önerilir
