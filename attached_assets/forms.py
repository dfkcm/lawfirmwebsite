from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, ValidationError, HiddenField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mevcut Şifre', validators=[DataRequired()])
    new_password = PasswordField('Yeni Şifre', validators=[
        DataRequired(),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    confirm_password = PasswordField('Şifreyi Tekrar', validators=[
        DataRequired(),
        EqualTo('new_password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Şifreyi Değiştir')

class ProfileForm(FlaskForm):
    full_name = StringField('Ad Soyad', validators=[DataRequired()])
    profession = StringField('Meslek', validators=[DataRequired()])
    phone = StringField('Telefon', validators=[DataRequired()])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    profile_photo = FileField('Profil Fotoğrafı', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])
    submit = SubmitField('Güncelle')

class ServiceForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

class ExpertiseForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

class ProjectForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    category = SelectField('Hukuk Alanı', validators=[DataRequired()], 
                        choices=[
                            ('anayasa', 'Anayasa Hukuku'),
                            ('ceza', 'Ceza Hukuku'),
                            ('ceza_muhakemesi', 'Ceza Muhakemesi Hukuku'),
                            ('ceza_infaz', 'Ceza İnfaz Hukuku'),
                            ('idare', 'İdare Hukuku'),
                            ('vergi', 'Vergi Hukuku'),
                            ('disiplin', 'Disiplin Hukuku'),
                            ('insan_haklari', 'İnsan Hakları Hukuku'),
                            ('devletler_genel', 'Devletler Genel Hukuku'),
                            ('medeni', 'Medeni Hukuk'),
                            ('kisiler', 'Kişiler Hukuku'),
                            ('aile', 'Aile Hukuku'),
                            ('miras', 'Miras Hukuku'),
                            ('esya', 'Eşya Hukuku'),
                            ('borclar', 'Borçlar Hukuku'),
                            ('ticaret', 'Ticaret Hukuku'),
                            ('ticari_isletme', 'Ticari İşletme Hukuku'),
                            ('sirketler', 'Şirketler Hukuku'),
                            ('kiymetli_evrak', 'Kıymetli Evrak Hukuku'),
                            ('deniz_ticareti', 'Deniz Ticareti Hukuku'),
                            ('sigorta', 'Sigorta Hukuku'),
                            ('is', 'İş Hukuku'),
                            ('toplu_is', 'Toplu İş Hukuku'),
                            ('sosyal_guvenlik', 'Sosyal Güvenlik Hukuku'),
                            ('icra_iflas', 'İcra ve İflas Hukuku'),
                            ('uluslararasi_ozel', 'Uluslararası Özel Hukuk'),
                            ('uluslararasi_kamu', 'Uluslararası Kamu Hukuku'),
                            ('fikri_sinai', 'Fikri ve Sınai Mülkiyet Hukuku'),
                            ('tuketici', 'Tüketici Hukuku'),
                            ('rekabet', 'Rekabet Hukuku'),
                            ('tasima', 'Taşıma Hukuku'),
                            ('spor', 'Spor Hukuku'),
                            ('bilisim', 'Bilişim Hukuku'),
                            ('saglik', 'Sağlık Hukuku'),
                            ('tip', 'Tıp Hukuku'),
                            ('medya_basin', 'Medya ve Basın Hukuku'),
                            ('enerji', 'Enerji Hukuku'),
                            ('cevre', 'Çevre Hukuku'),
                            ('insaat', 'İnşaat Hukuku'),
                            ('ulastirma', 'Ulaştırma Hukuku'),
                            ('hava_uzay', 'Hava ve Uzay Hukuku'),
                            ('tarim', 'Tarım Hukuku'),
                            ('turizm', 'Turizm Hukuku'),
                            ('kulturel_miras', 'Kültürel Miras Hukuku'),
                            ('avrupa_birligi', 'Avrupa Birliği Hukuku'),
                            ('uluslararasi_ticaret', 'Uluslararası Ticaret Hukuku'),
                            ('uluslararasi_ceza', 'Uluslararası Ceza Hukuku'),
                            ('secim', 'Seçim Hukuku'),
                            ('imar', 'İmar Hukuku'),
                            ('noterlik', 'Noterlik Hukuku'),
                            ('avukatlik', 'Avukatlık Hukuku'),
                            ('yargilama', 'Yargılama Hukuku'),
                            ('hukuk_felsefesi', 'Hukuk Felsefesi'),
                            ('hukuk_sosyolojisi', 'Hukuk Sosyolojisi'),
                            ('gayrimenkul', 'Gayrimenkul Hukuku')
                        ])
    image = FileField('Makale Görseli', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])
    submit = SubmitField('Kaydet')

class SocialMediaForm(FlaskForm):
    facebook = StringField('Facebook', validators=[DataRequired(), URL()])
    instagram = StringField('Instagram', validators=[DataRequired(), URL()])
    twitter = StringField('Twitter', validators=[DataRequired(), URL()])
    submit = SubmitField('Güncelle')

class SettingsForm(FlaskForm):
    site_name = StringField('Site Adı', validators=[DataRequired()])
    site_description = TextAreaField('Site Açıklaması', validators=[DataRequired()])
    site_keywords = StringField('Site Anahtar Kelimeleri', validators=[DataRequired()])
    site_author = StringField('Site Yazarı', validators=[DataRequired()])
    site_footer = StringField('Site Footer', validators=[DataRequired()])
    submit = SubmitField('Güncelle')

class HomepageForm(FlaskForm):
    homepage_title = StringField('Ana Başlık', validators=[DataRequired()])
    homepage_subtitle = StringField('Alt Başlık')
    homepage_content = TextAreaField('İçerik', validators=[DataRequired()])
    homepage_image = FileField('Ana Sayfa Görseli', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])
    submit = SubmitField('Güncelle')

class AboutForm(FlaskForm):
    about_title = StringField('Hakkımızda Başlığı', validators=[DataRequired()])
    about_content = TextAreaField('Hakkımızda İçeriği', validators=[DataRequired()])
    about_image = FileField('Görsel', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])
    submit = SubmitField('Güncelle')

class LawyerForm(FlaskForm):
    name = StringField('Ad Soyad', validators=[DataRequired()])
    title = StringField('Ünvan', validators=[DataRequired()])
    bio = TextAreaField('Biyografi', validators=[DataRequired()])
    photo = FileField('Fotoğraf', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])
    order = IntegerField('Sıralama', default=0)
    submit = SubmitField('Kaydet')

class ContactForm(FlaskForm):
    full_name = StringField('Ad Soyad', validators=[DataRequired()])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    subject = StringField('Konu', validators=[DataRequired()])
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    captcha = StringField('Güvenlik Kodu', validators=[DataRequired()])
    csrf_token = HiddenField()
    submit = SubmitField('Gönder')
