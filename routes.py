import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_login import login_required, current_user
from app import app, db
from models import Settings, User, Service, Expertise, Project, SocialMedia, Contact, Lawyer, Article, Category
from forms import ContactForm
from utils import generate_captcha_code
import secrets

# Generate CSRF token for session
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

def get_client_ip():
    # Render ve diğer proxy'ler için header kontrolleri
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For header'ı virgülle ayrılmış IP'leri içerir
        # İlk IP gerçek client IP'sidir
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr

@app.route('/')
def index():
    # Fetch minimal data for the simplified home page
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    user = User.query.first()
    
    return render_template('index.html',
                         settings=settings,
                         social=social,
                         user=user)

@app.route('/hakkimizda')
def hakkimizda():
    # Fetch data for the about page
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    lawyers = Lawyer.query.order_by(Lawyer.order).all()
    
    return render_template('about.html',
                         settings=settings,
                         social=social,
                         lawyers=lawyers)

@app.route('/calisma-alanlarimiz')
def calisma_alanlarimiz():
    # Fetch data for the practice areas page
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    calisma_list = Expertise.query.all()
    
    return render_template('practice_areas.html',
                         settings=settings,
                         social=social,
                         calisma_list=calisma_list)

@app.route('/makaleler')
def makaleler():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    search_query = request.args.get('q', '')
    category = request.args.get('category', '')
    query = Project.query
    if search_query:
        query = query.filter(Project.title.ilike(f'%{search_query}%') | Project.description.ilike(f'%{search_query}%'))
    if category:
        query = query.filter(Project.category == category)
    total_articles = query.count()
    total_pages = (total_articles + per_page - 1) // per_page
    offset = (page - 1) * per_page
    articles = query.order_by(Project.date.desc()).offset(offset).limit(per_page).all()
    categories = db.session.query(Project.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    category_map = {
        'anayasa': 'Anayasa Hukuku',
        'ceza': 'Ceza Hukuku',
        'ceza_muhakemesi': 'Ceza Muhakemesi Hukuku',
        'ceza_infaz': 'Ceza İnfaz Hukuku',
        'idare': 'İdare Hukuku',
        'vergi': 'Vergi Hukuku',
        'disiplin': 'Disiplin Hukuku',
        'insan_haklari': 'İnsan Hakları Hukuku',
        'devletler_genel': 'Devletler Genel Hukuku',
        'medeni': 'Medeni Hukuk',
        'kisiler': 'Kişiler Hukuku',
        'aile': 'Aile Hukuku',
        'miras': 'Miras Hukuku',
        'esya': 'Eşya Hukuku',
        'borclar': 'Borçlar Hukuku',
        'ticaret': 'Ticaret Hukuku',
        'ticari_isletme': 'Ticari İşletme Hukuku',
        'sirketler': 'Şirketler Hukuku',
        'kiymetli_evrak': 'Kıymetli Evrak Hukuku',
        'deniz_ticareti': 'Deniz Ticareti Hukuku',
        'sigorta': 'Sigorta Hukuku',
        'is': 'İş Hukuku',
        'toplu_is': 'Toplu İş Hukuku',
        'sosyal_guvenlik': 'Sosyal Güvenlik Hukuku',
        'icra_iflas': 'İcra ve İflas Hukuku',
        'uluslararasi_ozel': 'Uluslararası Özel Hukuk',
        'uluslararasi_kamu': 'Uluslararası Kamu Hukuku',
        'fikri_sinai': 'Fikri ve Sınai Mülkiyet Hukuku',
        'tuketici': 'Tüketici Hukuku',
        'rekabet': 'Rekabet Hukuku',
        'tasima': 'Taşıma Hukuku',
        'spor': 'Spor Hukuku',
        'bilisim': 'Bilişim Hukuku',
        'saglik': 'Sağlık Hukuku',
        'tip': 'Tıp Hukuku',
        'medya_basin': 'Medya ve Basın Hukuku',
        'enerji': 'Enerji Hukuku',
        'cevre': 'Çevre Hukuku',
        'insaat': 'İnşaat Hukuku',
        'ulastirma': 'Ulaştırma Hukuku',
        'hava_uzay': 'Hava ve Uzay Hukuku',
        'tarim': 'Tarım Hukuku',
        'turizm': 'Turizm Hukuku',
        'kulturel_miras': 'Kültürel Miras Hukuku',
        'avrupa_birligi': 'Avrupa Birliği Hukuku',
        'uluslararasi_ticaret': 'Uluslararası Ticaret Hukuku',
        'uluslararasi_ceza': 'Uluslararası Ceza Hukuku',
        'secim': 'Seçim Hukuku',
        'imar': 'İmar Hukuku',
        'noterlik': 'Noterlik Hukuku',
        'avukatlik': 'Avukatlık Hukuku',
        'yargilama': 'Yargılama Hukuku',
        'hukuk_felsefesi': 'Hukuk Felsefesi',
        'hukuk_sosyolojisi': 'Hukuk Sosyolojisi',
        'gayrimenkul': 'Gayrimenkul Hukuku'
    }
    categories_with_labels = [(cat, category_map.get(cat, cat)) for cat in categories]
    return render_template('articles.html',
                         settings=settings,
                         social=social,
                         articles=articles,
                         categories=categories_with_labels,
                         current_page=page,
                         total_pages=total_pages,
                         category_map=category_map)

@app.route('/makale/<int:id>')
def makale_detay(id):
    # Fetch article details
    settings = Settings.query.first()
    article = Project.query.get_or_404(id)
    social = SocialMedia.query.first()
    
    # Fetch other recent articles for sidebar
    recent_articles = Project.query.filter(Project.id != id).order_by(Project.date.desc()).limit(3).all()
    
    # Get category label
    category_map = {
        'anayasa': 'Anayasa Hukuku',
        'ceza': 'Ceza Hukuku',
        'ceza_muhakemesi': 'Ceza Muhakemesi Hukuku',
        'ceza_infaz': 'Ceza İnfaz Hukuku',
        'idare': 'İdare Hukuku',
        'vergi': 'Vergi Hukuku',
        'disiplin': 'Disiplin Hukuku',
        'insan_haklari': 'İnsan Hakları Hukuku',
        'devletler_genel': 'Devletler Genel Hukuku',
        'medeni': 'Medeni Hukuk',
        'kisiler': 'Kişiler Hukuku',
        'aile': 'Aile Hukuku',
        'miras': 'Miras Hukuku',
        'esya': 'Eşya Hukuku',
        'borclar': 'Borçlar Hukuku',
        'ticaret': 'Ticaret Hukuku',
        'ticari_isletme': 'Ticari İşletme Hukuku',
        'sirketler': 'Şirketler Hukuku',
        'kiymetli_evrak': 'Kıymetli Evrak Hukuku',
        'deniz_ticareti': 'Deniz Ticareti Hukuku',
        'sigorta': 'Sigorta Hukuku',
        'is': 'İş Hukuku',
        'toplu_is': 'Toplu İş Hukuku',
        'sosyal_guvenlik': 'Sosyal Güvenlik Hukuku',
        'icra_iflas': 'İcra ve İflas Hukuku',
        'uluslararasi_ozel': 'Uluslararası Özel Hukuk',
        'uluslararasi_kamu': 'Uluslararası Kamu Hukuku',
        'fikri_sinai': 'Fikri ve Sınai Mülkiyet Hukuku',
        'tuketici': 'Tüketici Hukuku',
        'rekabet': 'Rekabet Hukuku',
        'tasima': 'Taşıma Hukuku',
        'spor': 'Spor Hukuku',
        'bilisim': 'Bilişim Hukuku',
        'saglik': 'Sağlık Hukuku',
        'tip': 'Tıp Hukuku',
        'medya_basin': 'Medya ve Basın Hukuku',
        'enerji': 'Enerji Hukuku',
        'cevre': 'Çevre Hukuku',
        'insaat': 'İnşaat Hukuku',
        'ulastirma': 'Ulaştırma Hukuku',
        'hava_uzay': 'Hava ve Uzay Hukuku',
        'tarim': 'Tarım Hukuku',
        'turizm': 'Turizm Hukuku',
        'kulturel_miras': 'Kültürel Miras Hukuku',
        'avrupa_birligi': 'Avrupa Birliği Hukuku',
        'uluslararasi_ticaret': 'Uluslararası Ticaret Hukuku',
        'uluslararasi_ceza': 'Uluslararası Ceza Hukuku',
        'secim': 'Seçim Hukuku',
        'imar': 'İmar Hukuku',
        'noterlik': 'Noterlik Hukuku',
        'avukatlik': 'Avukatlık Hukuku',
        'yargilama': 'Yargılama Hukuku',
        'hukuk_felsefesi': 'Hukuk Felsefesi',
        'hukuk_sosyolojisi': 'Hukuk Sosyolojisi',
        'gayrimenkul': 'Gayrimenkul Hukuku'
    }
    category_label = category_map.get(article.category, '')
    
    return render_template('article_detail.html',
                        settings=settings,
                        article=article,
                        social=social,
                        recent_articles=recent_articles,
                        category_label=category_label,
                        category_map=category_map)

@app.route('/iletisim', methods=['GET', 'POST'])
def iletisim():
    # Fetch data for the contact page
    settings = Settings.query.first()
    user = User.query.first()
    social = SocialMedia.query.first()
    
    # Generate CSRF token if not exists
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    
    # Generate captcha code
    if 'captcha_code' not in session:
        session['captcha_code'] = generate_captcha_code()
    
    # Initialize contact form
    form = ContactForm()

    # Process contact form submission
    if request.method == 'POST':
        form = ContactForm(request.form)

        # Validate CSRF token
        form_token = request.form.get('csrf_token')
        if not form_token or form_token != session['csrf_token']:
            flash('Güvenlik doğrulaması başarısız oldu.', 'danger')
            session['captcha_code'] = generate_captcha_code()
            return render_template('contact.html',
                                 settings=settings,
                                 user=user,
                                 social=social,
                                 form=form)

        # Validate captcha
        captcha_input = request.form.get('captcha')
        if not captcha_input or captcha_input != session.get('captcha_code'):
            flash('Güvenlik kodu hatalı.', 'danger')
            session['captcha_code'] = generate_captcha_code()
            return render_template('contact.html',
                                 settings=settings,
                                 user=user,
                                 social=social,
                                 form=form)
        
        # Create a new contact message
        new_message = Contact(
            full_name=request.form.get('full_name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message'),
            ip_address=get_client_ip()
        )
        
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Mesajınız başarıyla gönderildi.', 'success')
            
            # Regenerate captcha code
            session['captcha_code'] = generate_captcha_code()
            # Regenerate CSRF token
            session['csrf_token'] = secrets.token_hex(16)
            
            return redirect(url_for('iletisim'))
        except Exception as e:
            db.session.rollback()
            flash(f'Bir hata oluştu: {str(e)}', 'danger')
            return redirect(url_for('iletisim'))
    
    return render_template('contact.html',
                         settings=settings,
                         user=user,
                         social=social,
                         form=form)

@app.route('/captcha')
def captcha():
    """Generate a captcha image and return it"""
    # Generate a new captcha code
    captcha_code = generate_captcha_code()
    session['captcha_code'] = captcha_code
    
    # Create a simple SVG captcha
    svg = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="150" height="50">
        <rect width="100%" height="100%" fill="white"/>
        <text x="30" y="35" font-family="Arial" font-size="24" fill="black">{captcha_code}</text>
        <line x1="10" y1="10" x2="140" y2="40" stroke="gray" stroke-width="1"/>
        <line x1="40" y1="30" x2="110" y2="10" stroke="gray" stroke-width="1"/>
        <line x1="20" y1="40" x2="130" y2="20" stroke="gray" stroke-width="1"/>
    </svg>
    '''
    
    return svg, 200, {'Content-Type': 'image/svg+xml'}

@app.route('/error')
def error():
    message = request.args.get('message', 'Sayfa bulunamadı veya erişim izniniz yok.')
    return render_template('error.html', message=message)

@app.errorhandler(404)
def page_not_found(e):
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    return render_template('error.html', 
                         settings=settings, 
                         social=social, 
                         message='Sayfa bulunamadı.'), 404

@app.errorhandler(403)
def forbidden(e):
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    return render_template('error.html', 
                         settings=settings, 
                         social=social, 
                         message='Bu sayfaya erişim izniniz yok.'), 403

@app.errorhandler(500)
def internal_server_error(e):
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    return render_template('error.html', 
                         settings=settings, 
                         social=social, 
                         message='Sunucu hatası oluştu. Lütfen daha sonra tekrar deneyiniz.'), 500