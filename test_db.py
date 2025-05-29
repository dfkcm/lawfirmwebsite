from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    
    # Tabloların varlığını kontrol et
    print("\nTablo kontrolleri:")
    tables = inspector.get_table_names()
    print(f"Mevcut tablolar: {tables}")

    # Test kaydı oluştur
    print("\nTest kaydı oluşturuluyor...")
    try:
        db.session.commit()
        print("Test kayıtları başarıyla oluşturuldu!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Hata: {str(e)}") 