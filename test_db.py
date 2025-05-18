from app import app, db
from models import VisitorLog, DailyAnalytics
from datetime import datetime, date
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    
    # Tabloların varlığını kontrol et
    print("\nTablo kontrolleri:")
    tables = inspector.get_table_names()
    print(f"Mevcut tablolar: {tables}")
    print(f"VisitorLog tablosu var mı: {'visitor_logs' in tables}")
    print(f"DailyAnalytics tablosu var mı: {'daily_analytics' in tables}")
    
    # Mevcut kayıtları kontrol et
    print("\nMevcut kayıtlar:")
    visitor_count = VisitorLog.query.count()
    analytics_count = DailyAnalytics.query.count()
    print(f"VisitorLog kayıt sayısı: {visitor_count}")
    print(f"DailyAnalytics kayıt sayısı: {analytics_count}")
    
    # Test kaydı oluştur
    print("\nTest kaydı oluşturuluyor...")
    try:
        # Visitor log test kaydı
        test_log = VisitorLog(
            ip_address="127.0.0.1",
            user_agent="Test Browser",
            page_visited="/test",
            browser="Test Browser 1.0",
            platform="Test OS",
            is_mobile=False,
            session_id="test_session"
        )
        db.session.add(test_log)
        
        # Daily analytics test kaydı
        today = date.today()
        test_analytics = DailyAnalytics.query.filter_by(date=today).first()
        if not test_analytics:
            test_analytics = DailyAnalytics(
                date=today,
                total_visits=1,
                unique_visitors=1,
                home_page_visits=1,
                mobile_visits=0,
                desktop_visits=1
            )
            db.session.add(test_analytics)
        
        db.session.commit()
        print("Test kayıtları başarıyla oluşturuldu!")
        
        # Oluşturulan kayıtları kontrol et
        print("\nGüncellenmiş kayıt sayıları:")
        print(f"VisitorLog kayıt sayısı: {VisitorLog.query.count()}")
        print(f"DailyAnalytics kayıt sayısı: {DailyAnalytics.query.count()}")
        
        # Son eklenen kayıtları göster
        print("\nSon eklenen ziyaretçi kaydı:")
        last_visitor = VisitorLog.query.order_by(VisitorLog.visit_time.desc()).first()
        if last_visitor:
            print(f"IP: {last_visitor.ip_address}")
            print(f"Sayfa: {last_visitor.page_visited}")
            print(f"Zaman: {last_visitor.visit_time}")
        
        print("\nBugünün analitik kaydı:")
        today_analytics = DailyAnalytics.query.filter_by(date=today).first()
        if today_analytics:
            print(f"Toplam ziyaret: {today_analytics.total_visits}")
            print(f"Tekil ziyaretçi: {today_analytics.unique_visitors}")
            print(f"Mobil ziyaret: {today_analytics.mobile_visits}")
            print(f"Masaüstü ziyaret: {today_analytics.desktop_visits}")
        
    except Exception as e:
        print(f"\nHATA: {str(e)}")
        import traceback
        print(f"Hata detayı: {traceback.format_exc()}")
        db.session.rollback() 