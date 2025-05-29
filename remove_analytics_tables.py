from app import app, db
import sqlite3

def remove_analytics_tables():
    with app.app_context():
        # SQLite bağlantısı oluştur
        conn = sqlite3.connect('instance/portfolio.db')
        c = conn.cursor()
        
        try:
            # Tabloları sil
            c.execute("DROP TABLE IF EXISTS visitor_logs;")
            c.execute("DROP TABLE IF EXISTS daily_analytics;")
            conn.commit()
            print("Ziyaretçi analitiği tabloları başarıyla silindi.")
        except Exception as e:
            print(f"Hata: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    remove_analytics_tables() 