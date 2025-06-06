import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import random
import string

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure upload path
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except Exception as e:
        logging.error(f"Uploads klasörü oluşturma hatası: {e}")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
}

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

@app.context_processor
def utility_processor():
    return dict(
        get_random_string=lambda n: ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
    )

# Create all tables
with app.app_context():
    try:
        from models import Admin, Settings, User, Service, Expertise, Project, SocialMedia, Contact, Lawyer
        db.create_all()
        
        # Initialize an admin user if none exists
        if not Admin.query.first():
            from werkzeug.security import generate_password_hash
            admin = Admin()
            admin.username = os.environ.get('ADMIN_USER', 'admin')
            admin.email = 'admin@admin.com'
            admin.password_hash = generate_password_hash(os.environ.get('ADMIN_PASS', 'MS'))
            db.session.add(admin)
            db.session.commit()
            logging.info("Created default admin user")
        
        # Initialize settings if none exist
        if not Settings.query.first():
            settings = Settings()
            settings.site_name = 'KILINÇ HUKUK VE DANIŞMANLIK'
            settings.site_description = 'KILINÇ HUKUK VE DANIŞMANLIK - Profesyonel Hukuk Hizmetleri'
            settings.site_keywords = 'hukuk, avukat, danışmanlık, dava, hukuki yardım'
            settings.site_author = 'Av. Nail Furkan Kılınç'
            settings.site_footer = '© 2024 KILINÇ HUKUK VE DANIŞMANLIK. Tüm hakları saklıdır.'
            db.session.add(settings)
            db.session.commit()
            logging.info("Created default settings")
    except Exception as e:
        logging.error(f"Veritabanı başlatma hatası: {e}")

from routes import *
from admin_routes import *

if __name__ == '__main__':
    app.run(debug=True)