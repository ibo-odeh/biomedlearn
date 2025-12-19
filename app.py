from flask import Flask, render_template, g, request, redirect, url_for, session, send_from_directory, flash
import sqlite3
from flask import send_from_directory, make_response
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = 'gizli_anahtar'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.secret_key = 'biyomedikal_secret_key'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'pptx', 'jpg', 'png', 'txt','zip', 'rar', '7z', 'schdoc', 'pcbdoc', 'prjpcb', 'libpkg', 'cmp', 'csv', 'm', 'ino', 'py', 'c', 'cpp', 'hex'}
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'jpg', 'png', 'txt','zip', 'rar', '7z', 'schdoc', 'pcbdoc', 'prjpcb', 'libpkg', 'cmp', 'csv', 'm', 'ino', 'py', 'c', 'cpp', 'hex'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, kategori):
    kategori_yolu = os.path.join(app.config['UPLOAD_FOLDER'], kategori)
    os.makedirs(kategori_yolu, exist_ok=True)
    file.save(os.path.join(kategori_yolu, file.filename))


# === Veritabanı ===
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT DEFAULT 'user',
                        email TEXT,
                        profile_pic TEXT DEFAULT 'profile_icon.png')''')
    conn.execute('''CREATE TABLE IF NOT EXISTS dersler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content TEXT,
                        filename TEXT
    )''')
    conn.commit()
    conn.close()

init_db()


import time

@app.before_request
def add_timestamp():
    g.ts = int(time.time())

# === Giriş Sayfası ===
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], role=session['role'])
    else:
        return render_template('index.html', role=None)


    upload_dir = os.path.join(app.root_path, 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    uploaded_files = os.listdir(upload_dir)

    return render_template('index.html',
                           username=session.get('username'),
                           role=session.get('role'),
                           uploaded_files=uploaded_files)



# === Kayıt ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = get_db()
        try:
            role = 'admin' if username == 'ibo' else 'user'
            cur.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)',
                        (username, password, role, email))                          
            conn.commit()
        except Exception as e:
            print("Kayıt hatası:", e)
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# === Giriş ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Veritabanını aç
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        # Kullanıcı yoksa hata ver
        if user is None:
            return "Kullanıcı bulunamadı veya şifre hatalı"

        # Session bilgilerini kaydet
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role'] if 'role' in user.keys() else 'user'
        session['profile_pic'] = user['profile_pic'] if user['profile_pic'] else 'profile_icon.jpg'
   

        # Role kontrolü
        if session['role'] in ['user', 'admin']:
            return redirect(url_for('index'))
        # Ana sayfaya yönlendir
        else:
            return render_template('login.html', error="Hatalı kullanıcı adı veya şifre.")
        
    # GET isteği ise login sayfasını göster
    return render_template('login.html')

# === Admin Paneli ===
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session:
        flash("Giriş yapmalısınız.")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Bu sayfaya erişim yetkiniz yok.")
        return redirect(url_for('index'))

    conn = get_db()

    # Dersler
    dersler = conn.execute('SELECT * FROM dersler').fetchall()

    # Yüklenmiş dosyalar
    import os
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    uploaded_files = os.listdir(upload_dir)


    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_dir, filename))
                flash(f"{filename} yüklendi!")


    uploaded_files = []    
    for filename in os.listdir(upload_dir):
         path = os.path.join(upload_dir, filename)
         if os.path.isfile(path):
             size = round(os.path.getsize(path) / 1024, 2)  # KB cinsinden
             ext = filename.split('.')[-1].upper()
             uploaded_files.append({
                 'name': filename,
                 'size': size,
                 'type': ext
             })

    conn.close()
    return render_template('admin.html', dersler=dersler, upload_files=uploaded_files)

# === Dosya İndirme ===
@app.route('/uploads/<path:filename>')
def upload1_file(filename):
    return send_from_directory('static/uploads', filename)
# === Dosya görüntüle ===
@app.route("/view_file/<filename>")
def view_file(filename):
    return send_from_directory("static/uploads", filename)
# === Ders Silme ===
@app.route('/delete_file/<filename>')
def delete_file(filename):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('admin'))

# === Ders Düzenleme ===
@app.route('/edit_file/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        new_name = request.form['new_name']
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        os.rename(old_path, new_path)
        return redirect(url_for('admin'))
    return render_template('edit_file.html', filename=filename)

# === Dosya yükleme kontrolü ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# === Dosya yükleme ===
@app.route('/upload', methods=['POST'])
def upload2_file():
    if 'user_id' not in session:
        flash("Giriş yapmalısınız.")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Bu sayfaya erişim yetkiniz yok.")
        return redirect(url_for('index'))

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           
            from datetime import datetime
            conn = get_db()
            conn.execute(
                "INSERT INTO uploaded_files (filename, uploaded_by, upload_date, description) VALUES (?, ?, ?, ?)",
                (filename, session['username'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request.form.get('description',''))
            )
            conn.commit()
            conn.close()


            flash(f"{filename} başarıyla yüklendi!")

    return redirect(url_for('admin'))

# === Normal Kullanıcı Sayfası ===
@app.route('/user')
def user_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Hatalı kullanıcı adı veya şifre.")

    # GET isteği ise login sayfasını göster
    return render_template('login.html')

# === Dersler ===
@app.route('/ders_notlari')  
def ders_notları():   
     if 'username' not in session:
         return redirect(url_for('login'))

     import os
     UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
     os.makedirs(UPLOAD_FOLDER, exist_ok=True)

     # Dosya bilgilerini listele
     files = []
     for f in os.listdir(UPLOAD_FOLDER):
         path = os.path.join(UPLOAD_FOLDER, f)
         if os.path.isfile(path):
             files.append({
                 "name": f,
                 "type": f.split('.')[-1].upper(),
                 "size": f"{os.path.getsize(path) / 1024:.1f} KB"
             })

     return render_template('ders_notları.html', files=files)

# === Projeler sayfası ===
@app.route('/projeler')
def projeler():
    if 'username' not in session:
        return redirect(url_for('login'))

    arduino_files = os.listdir(os.path.join(UPLOAD_FOLDER, "Arduino"))
    altium_files = os.listdir(os.path.join(UPLOAD_FOLDER, "Altium"))
    bio_files = os.listdir(os.path.join(UPLOAD_FOLDER, "Matlab"))
    return render_template("projeler.html",
                           arduino=arduino_files,
                           altium=altium_files,
                           biyomedikal=bio_files)


@app.route('/projeler/<kategori>', methods=['GET', 'POST'])
def kategori_sayfasi(kategori):
    kategori_klasoru = os.path.join('uploads', kategori)
    os.makedirs(kategori_klasoru, exist_ok=True)

    if request.method == 'POST' and 'role' in session and session['role'] == 'admin':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(kategori_klasoru, file.filename))
            flash('Dosya başarıyla yüklendi!', 'success')
        else:
            flash('Dosya türüne izin verilmiyor.', 'error')

    # Dosya listesini oku
    dosyalar = []
    for filename in os.listdir(kategori_klasoru):
        path = os.path.join(kategori_klasoru, filename)
        boyut_kb = round(os.path.getsize(path) / 1024, 2)
        dosyalar.append({
            'isim': filename,
            'boyut': f"{boyut_kb} KB"
        })

    return render_template('kategori.html', kategori=kategori, dosyalar=dosyalar)

@app.route('/indir/<kategori>/<filename>')
def indir_dosya(kategori, filename):
    return send_from_directory(os.path.join('uploads', kategori), filename, as_attachment=True)

@app.route('/sil/<kategori>/<filename>')
def sil_dosya(kategori, filename):
    if 'role' in session and session['role'] == 'admin':
        path = os.path.join('uploads', kategori, filename)
        if os.path.exists(path):
            os.remove(path)
            flash('Dosya silindi!', 'success')
    return redirect(url_for('kategori_sayfasi', kategori=kategori))

@app.route('/kategori/<kategori>/ekle', methods=['POST'])
def proje_ekle(kategori):
    if session.get('username') != 'admin':
        flash("Sadece yöneticiler dosya yükleyebilir!", "danger")
        return redirect(url_for('kategori_sayfasi', kategori=kategori))

    dosya = request.files['dosya']
    if dosya:
        kategori_klasoru = os.path.join(UPLOAD_FOLDER, kategori)
        os.makedirs(kategori_klasoru, exist_ok=True)
        dosya_yolu = os.path.join(kategori_klasoru, dosya.filename)
        dosya.save(dosya_yolu)
        flash(f"{kategori} kategorisine '{dosya.filename}' yüklendi.", "success")

    return redirect(url_for('kategori_sayfasi', kategori=kategori))


@app.route('/arduino_projects')
def arduino_projects():
    return render_template('arduino_projects.html')

@app.route('/altium_projects')
def altium_projects():
    return render_template('altium_projects.html')

@app.route('/biosensor_projects')
def biosensor_projects():
    return render_template('biosensor_projects.html')


# === topluluk ===
@app.route('/topluluk')
def topluluk():
    if 'username' in session:
        return render_template('topluluk.html', username=session['username'])
    return redirect(url_for('login'))

# === profil ===
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=?", (session['username'],)).fetchone()

    if request.method == 'POST':
        email = request.form['email']
        bio = request.form['bio']
        file = request.files.get('profile_pic')

        profile_pic = user['profile_pic']

        if file and file.filename != '':
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)

            upload_path = os.path.join(app.root_path, 'static', 'profile_pic')
            os.makedirs(upload_path, exist_ok=True)

            save_path = os.path.join(upload_path, filename)
            file.save(save_path)

            profile_pic = filename

        conn.execute("""
            UPDATE users 
            SET email=?, bio=?, profile_pic=? 
            WHERE id=?
        """, (email, bio, profile_pic, user['id']))

        conn.commit()
        conn.close()

        # SESSION’A DOĞRU GÜNCEL VERİYİ KAYDET!
        session['profile_pic'] = profile_pic
        session.modified = True
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user,ts=int(time.time()))



@app.route('/profile_pic/<filename>')
def profile_pic(filename):
    return send_from_directory('static/profile_pic', filename, cache_timeout=0)

# === profil resmi ===
@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'profile_pic' not in request.files:
        return redirect(url_for('profile'))

    file = request.files['profile_pic']
    if file.filename == '':
        return redirect(url_for('profile'))

    # Güvenli dosya adı
    filename = secure_filename(file.filename)

    # Klasör yoksa oluştur
    upload_folder = os.path.join(app.root_path, 'static/profile_pic')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Dosyayı kaydet
    file.save(os.path.join(upload_folder, filename))
    
    # after file.save(...) and DB update:
    session['profile_pic'] = filename
    session.modified = True
    print("SESSION PHOTO =", session.get('profile_pic'))


    # Veritabanına kaydet
    conn = get_db()
    conn.execute("UPDATE users SET profile_pic=? WHERE username=?", (filename, session['username']))
    conn.commit()
    conn.close()


    return redirect(url_for('profile'))

# === Hakkında ===
@app.route('/hakkında')
def hakkında():
    return render_template('hakkında.html')

# === İletişim ===
@app.route('/iletişim')
def iletişim():
    return render_template('iletişim.html')

# === Çıkış ===
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
