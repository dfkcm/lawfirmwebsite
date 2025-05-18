import os
import secrets
import uuid
from PIL import Image
from flask import current_app, request, session
from werkzeug.utils import secure_filename
import random
import string
from datetime import datetime, date, timedelta
from user_agents import parse
from app import db
from models import VisitorLog, DailyAnalytics

def save_image(file, folder='uploads'):
    """Save an image to the specified folder and return the filename"""
    if not file:
        return None
    
    # Create a secure filename
    filename = secure_filename(file.filename)
    # Generate a unique filename to avoid overwriting
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(filename)
    new_filename = random_hex + file_extension
    
    # Create the upload path if it doesn't exist
    upload_path = os.path.join(current_app.root_path, 'static', folder)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
    # Save the file
    file_path = os.path.join(upload_path, new_filename)
    
    # Resize and save image
    image = Image.open(file)
    # Set a max size for the image if needed
    image.thumbnail((1200, 1200))
    image.save(file_path)
    
    return new_filename

def generate_captcha_code(length=6):
    """Generate a random captcha code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def delete_image(filename, folder='uploads'):
    """Delete an image from the specified folder"""
    if not filename:
        return False
    
    file_path = os.path.join(current_app.root_path, 'static', folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def cleanup_old_records():
    """30 günden eski ziyaretçi kayıtlarını ve 7 günden eski analitik kayıtlarını temizle"""
    try:
        # 30 günden eski ziyaretçi kayıtlarını sil
        thirty_days_ago = datetime.now() - timedelta(days=30)
        old_logs = VisitorLog.query.filter(VisitorLog.visit_time < thirty_days_ago).delete()
        
        # 7 günden eski analitik kayıtlarını sil
        seven_days_ago = date.today() - timedelta(days=7)
        old_analytics = DailyAnalytics.query.filter(DailyAnalytics.date < seven_days_ago).delete()
        
        db.session.commit()
        print(f"Temizlenen kayıtlar - Ziyaretçi: {old_logs}, Analitik: {old_analytics}")
    except Exception as e:
        print(f"Kayıt temizleme hatası: {str(e)}")
        db.session.rollback()

def track_visitor():
    """Ziyaretçi bilgilerini kaydet ve günlük istatistikleri güncelle"""
    try:
        # Eski kayıtları temizle (her 100 ziyarette bir)
        if VisitorLog.query.count() % 100 == 0:
            cleanup_old_records()

        # Session ID oluştur veya mevcut olanı al
        if 'visitor_session_id' not in session:
            session['visitor_session_id'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

        # User agent bilgilerini parse et
        ua_string = request.user_agent.string
        user_agent = parse(ua_string)

        # Ziyaretçi logu oluştur
        visitor_log = VisitorLog(
            ip_address=request.headers.get('X-Forwarded-For', request.remote_addr),
            user_agent=ua_string,
            page_visited=request.path,
            referrer=request.referrer,
            browser=f"{user_agent.browser.family} {user_agent.browser.version_string}",
            platform=user_agent.os.family,
            is_mobile=user_agent.is_mobile,
            session_id=session['visitor_session_id']
        )
        
        db.session.add(visitor_log)

        # Günlük istatistikleri güncelle
        today = date.today()
        analytics = DailyAnalytics.query.filter_by(date=today).first()
        
        if not analytics:
            analytics = DailyAnalytics(date=today)
            db.session.add(analytics)
        
        # Toplam ziyaret sayısını artır
        analytics.total_visits += 1
        
        # Sayfa bazlı istatistikleri güncelle
        if request.path == '/':
            analytics.home_page_visits += 1
        elif request.path == '/hakkimizda':
            analytics.about_page_visits += 1
        elif request.path == '/iletisim':
            analytics.contact_page_visits += 1
        elif request.path.startswith('/makaleler'):
            analytics.articles_page_visits += 1
        elif request.path == '/uzmanlik-alanlari':
            analytics.practice_areas_visits += 1

        # Mobil/Desktop istatistiklerini güncelle
        if user_agent.is_mobile:
            analytics.mobile_visits += 1
        else:
            analytics.desktop_visits += 1

        # Benzersiz ziyaretçi sayısını güncelle
        unique_visitors = VisitorLog.query.filter(
            VisitorLog.visit_time >= today,
            VisitorLog.ip_address == visitor_log.ip_address
        ).count()
        
        if unique_visitors == 1:  # Bu IP'nin bugün ilk ziyareti
            analytics.unique_visitors += 1

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ziyaretçi takip hatası: {str(e)}")
        import traceback
        print(f"Hata stack trace: {traceback.format_exc()}")