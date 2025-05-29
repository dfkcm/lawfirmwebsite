from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, ValidationError, HiddenField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL

class AdminLoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')

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

class UserForm(FlaskForm):
    full_name = StringField('Ad Soyad', validators=[DataRequired()])
    profession = StringField('Meslek', validators=[DataRequired()])
    phone = StringField('Telefon', validators=[DataRequired()])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    profile_photo = FileField('Profil Fotoğrafı', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları (.jpg, .png)')
    ])

class ServiceForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    icon = StringField('İkon', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

class ExpertiseForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    icon = StringField('İkon', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

class ProjectForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[DataRequired()])
    image = FileField('Resim')
    link = StringField('Link', validators=[Optional(), URL()])
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
    submit = SubmitField('Kaydet')

class SocialMediaForm(FlaskForm):
    facebook = StringField('Facebook', validators=[Optional(), URL()])
    twitter = StringField('Twitter', validators=[Optional(), URL()])
    instagram = StringField('Instagram', validators=[Optional(), URL()])
    linkedin = StringField('LinkedIn', validators=[Optional(), URL()])
    youtube = StringField('YouTube', validators=[Optional(), URL()])
    submit = SubmitField('Güncelle')

class SettingsForm(FlaskForm):
    site_name = StringField('Site Adı', validators=[DataRequired()])
    site_title = StringField('Site Başlığı', validators=[DataRequired()])
    site_description = TextAreaField('Site Açıklaması', validators=[DataRequired()])
    contact_email = StringField('İletişim E-posta', validators=[DataRequired(), Email()])
    contact_phone = StringField('İletişim Telefon', validators=[DataRequired()])
    contact_address = TextAreaField('İletişim Adres', validators=[DataRequired()])
    footer_text = TextAreaField('Footer Metni', validators=[DataRequired()])
    logo = FileField('Logo')
    favicon = FileField('Favicon')

class LawyerForm(FlaskForm):
    name = StringField('Ad Soyad', validators=[DataRequired()])
    title = StringField('Ünvan', validators=[DataRequired()])
    bio = TextAreaField('Biyografi', validators=[DataRequired()])
    photo = FileField('Fotoğraf')
    order = IntegerField('Sıralama', default=0)

class AboutForm(FlaskForm):
    about_title = StringField('Hakkımızda Başlığı', validators=[DataRequired()])
    about_content = TextAreaField('Hakkımızda İçeriği', validators=[DataRequired()])
    about_image = FileField('Görsel')

class ArticleForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    category_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    image = FileField('Resim')
    meta_description = TextAreaField('Meta Açıklama', validators=[Optional()])
    meta_keywords = StringField('Meta Anahtar Kelimeler', validators=[Optional()])

class CategoryForm(FlaskForm):
    name = StringField('Kategori Adı', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[Optional()])

class ContactForm(FlaskForm):
    full_name = StringField('Ad Soyad', validators=[DataRequired()])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    subject = StringField('Konu', validators=[DataRequired()])
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    captcha = StringField('Güvenlik Kodu', validators=[DataRequired()])
    csrf_token = HiddenField()
    submit = SubmitField('Gönder')