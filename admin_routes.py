import os
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import Admin, Settings, User, Service, Expertise, Project, SocialMedia, Contact, Lawyer, Article, Category
from forms import (AdminLoginForm, SettingsForm, UserForm, ServiceForm, ExpertiseForm, 
                  ProjectForm, SocialMediaForm, LawyerForm, ArticleForm, CategoryForm,
                  ChangePasswordForm, AboutForm)
from utils import save_image, delete_image
import secrets
from datetime import datetime, timedelta

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    settings = Settings.query.first()
    message_count = Contact.query.count()
    project_count = Project.query.count()
    
    latest_messages = Contact.query.order_by(Contact.date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         settings=settings,
                         message_count=message_count,
                         project_count=project_count,
                         latest_messages=latest_messages,
                         now=datetime.now())

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    settings = Settings.query.first()
    user = User.query.first()
    if not user:
        user = User(
            full_name="",
            email="",
            description="",
            profession="",
            phone=""
        )
        db.session.add(user)
        db.session.commit()
    
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        
        # Handle profile photo upload
        if form.profile_photo.data:
            if user.profile_photo:
                delete_image(user.profile_photo)
            filename = save_image(form.profile_photo.data, 'uploads')
            user.profile_photo = filename
        
        db.session.commit()
        flash('Profil bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_profile'))
    
    return render_template('admin/profile.html', settings=settings, form=form, user=user, now=datetime.now())

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    settings = Settings.query.first()
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        admin = Admin.query.get(current_user.id)
        
        if check_password_hash(admin.password_hash, form.current_password.data):
            admin.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Şifreniz başarıyla değiştirildi.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Mevcut şifre hatalı.', 'danger')
    
    return render_template('admin/change_password.html', settings=settings, form=form, now=datetime.now())

@app.route('/admin/services', methods=['GET', 'POST'])
@login_required
def admin_services():
    settings = Settings.query.first()
    services = Service.query.all()
    form = ServiceForm()
    
    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Hizmet başarıyla eklendi.', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/services.html', settings=settings, services=services, form=form, now=datetime.now())

@app.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_service(id):
    settings = Settings.query.first()
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    
    if form.validate_on_submit():
        form.populate_obj(service)
        db.session.commit()
        flash('Hizmet başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/edit_service.html', settings=settings, form=form, service=service, now=datetime.now())

@app.route('/admin/services/delete/<int:id>')
@login_required
def admin_delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Hizmet başarıyla silindi.', 'success')
    return redirect(url_for('admin_services'))

@app.route('/admin/calisma-alanlarimiz', methods=['GET', 'POST'])
@login_required
def admin_calisma_alanlarimiz():
    settings = Settings.query.first()
    calisma_list = Expertise.query.all()
    form = ExpertiseForm()
    if form.validate_on_submit():
        calisma = Expertise(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(calisma)
        db.session.commit()
        flash('Çalışma alanı başarıyla eklendi.', 'success')
        return redirect(url_for('admin_calisma_alanlarimiz'))
    return render_template('admin/calisma_alanlarimiz.html', settings=settings, calisma_list=calisma_list, form=form, now=datetime.now())

@app.route('/admin/calisma-alanlarimiz/delete/<int:id>')
@login_required
def admin_delete_calisma(id):
    calisma = Expertise.query.get_or_404(id)
    db.session.delete(calisma)
    db.session.commit()
    flash('Çalışma alanı başarıyla silindi.', 'success')
    return redirect(url_for('admin_calisma_alanlarimiz'))

@app.route('/admin/projects', methods=['GET', 'POST'])
@login_required
def admin_projects():
    settings = Settings.query.first()
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Her sayfada 10 makale
    
    projects = Project.query.order_by(Project.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data
        )
        
        db.session.add(project)
        db.session.commit()
        flash('Makale başarıyla eklendi.', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/projects.html', 
                         settings=settings, 
                         projects=projects, 
                         form=form, 
                         now=datetime.now())

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_project(id):
    settings = Settings.query.first()
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        # Form içeriğini modele doldur (image hariç)
        project.title = form.title.data
        project.description = form.description.data
        project.category = form.category.data
        
        db.session.commit()
        flash('Makale başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/edit_project.html', settings=settings, form=form, project=project, now=datetime.now())

@app.route('/admin/projects/delete/<int:id>')
@login_required
def admin_delete_project(id):
    project = Project.query.get_or_404(id)
    
    db.session.delete(project)
    db.session.commit()
    flash('Makale başarıyla silindi.', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/social-media', methods=['GET', 'POST'])
@login_required
def admin_social_media():
    settings = Settings.query.first()
    social = SocialMedia.query.first()
    if not social:
        social = SocialMedia(
            facebook="https://facebook.com",
            instagram="https://instagram.com",
            twitter="https://twitter.com"
        )
        db.session.add(social)
        db.session.commit()
    
    form = SocialMediaForm(obj=social)
    
    if form.validate_on_submit():
        form.populate_obj(social)
        db.session.commit()
        flash('Sosyal medya bağlantıları başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_social_media'))
    
    return render_template('admin/social_media.html', settings=settings, form=form, now=datetime.now())

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = Settings.query.first()
    form = SettingsForm(obj=settings)
    
    if form.validate_on_submit():
        form.populate_obj(settings)
        db.session.commit()
        flash('Site ayarları başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', settings=settings, form=form, now=datetime.now())

@app.route('/admin/messages')
@login_required
def admin_messages():
    settings = Settings.query.first()
    messages = Contact.query.order_by(Contact.date.desc()).all()
    return render_template('admin/messages.html',
                         settings=settings,
                         messages=messages,
                         now=datetime.now())

@app.route('/admin/messages/view/<int:id>')
@login_required
def admin_view_message(id):
    settings = Settings.query.first()
    message = Contact.query.get_or_404(id)
    return render_template('admin/view_message.html', settings=settings, message=message, now=datetime.now())

@app.route('/admin/messages/delete/<int:id>')
@login_required
def admin_delete_message(id):
    message = Contact.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Mesaj başarıyla silindi.', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/homepage', methods=['GET', 'POST'])
@login_required
def admin_homepage():
    settings = Settings.query.first()
    form = SettingsForm(obj=settings)
    
    if form.validate_on_submit():
        form.populate_obj(settings)
        
        # Görsel işleme
        if form.logo.data:
            if settings.homepage_image:
                delete_image(settings.homepage_image)
            filename = save_image(form.logo.data, 'uploads')
            settings.homepage_image = filename
        
        db.session.commit()
        flash('Site ayarları başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_homepage'))
    
    return render_template('admin/homepage.html', 
                         settings=settings, 
                         form=form, 
                         now=datetime.now())

@app.route('/admin/about', methods=['GET', 'POST'])
@login_required
def admin_about():
    settings = Settings.query.first()
    form = AboutForm(obj=settings)
    
    if form.validate_on_submit():
        settings.about_title = form.about_title.data
        settings.about_content = form.about_content.data
        
        # Görsel işleme
        if form.about_image.data:
            if settings.about_image:
                delete_image(settings.about_image)
            filename = save_image(form.about_image.data, 'uploads')
            settings.about_image = filename
        
        db.session.commit()
        flash('Hakkımızda içeriği başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_about'))
    
    return render_template('admin/about.html', 
                         settings=settings, 
                         form=form, 
                         now=datetime.now())

@app.route('/admin/lawyers', methods=['GET', 'POST'])
@login_required
def admin_lawyers():
    settings = Settings.query.first()
    lawyers = Lawyer.query.order_by(Lawyer.order).all()
    form = LawyerForm()
    
    if form.validate_on_submit():
        lawyer = Lawyer(
            name=form.name.data,
            title=form.title.data,
            bio=form.bio.data,
            order=form.order.data
        )
        
        # Fotoğraf işleme
        if form.photo.data:
            filename = save_image(form.photo.data, 'uploads')
            lawyer.photo = filename
        
        db.session.add(lawyer)
        db.session.commit()
        flash('Avukat başarıyla eklendi.', 'success')
        return redirect(url_for('admin_lawyers'))
    
    return render_template('admin/lawyers.html', 
                         settings=settings, 
                         lawyers=lawyers, 
                         form=form, 
                         now=datetime.now())

@app.route('/admin/lawyers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_lawyer(id):
    settings = Settings.query.first()
    lawyer = Lawyer.query.get_or_404(id)
    form = LawyerForm(obj=lawyer)
    
    if form.validate_on_submit():
        lawyer.name = form.name.data
        lawyer.title = form.title.data
        lawyer.bio = form.bio.data
        lawyer.order = form.order.data
        
        # Fotoğraf işleme
        if form.photo.data:
            if lawyer.photo:
                delete_image(lawyer.photo)
            filename = save_image(form.photo.data, 'uploads')
            lawyer.photo = filename
        
        db.session.commit()
        flash('Avukat bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_lawyers'))
    
    return render_template('admin/edit_lawyer.html', 
                         settings=settings, 
                         form=form, 
                         lawyer=lawyer, 
                         now=datetime.now())

@app.route('/admin/lawyers/delete/<int:id>')
@login_required
def admin_delete_lawyer(id):
    lawyer = Lawyer.query.get_or_404(id)
    
    # Fotoğraf silme
    if lawyer.photo:
        delete_image(lawyer.photo)
    
    db.session.delete(lawyer)
    db.session.commit()
    flash('Avukat başarıyla silindi.', 'success')
    return redirect(url_for('admin_lawyers'))