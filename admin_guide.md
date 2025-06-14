# دليل استخدام واجهة الإدارة لموقع DU للدفع وشحن الرصيد

## مقدمة

هذا الدليل يشرح كيفية استخدام واجهة الإدارة الخاصة بموقع DU للدفع وشحن الرصيد، والتي تتيح لك الوصول إلى جميع البيانات المخزنة في قاعدة البيانات بطريقة سهلة وآمنة.

## تسجيل الدخول

1. افتح متصفح الويب وانتقل إلى صفحة تسجيل الدخول:
   ```
   http://localhost:5000/admin_login.html
   ```

2. أدخل بيانات تسجيل الدخول الافتراضية:
   - اسم المستخدم: `admin`
   - كلمة المرور: `admin123`

3. انقر على زر "تسجيل الدخول"

4. إذا كانت بيانات الدخول صحيحة، سيتم توجيهك تلقائياً إلى لوحة التحكم.

## استخدام لوحة التحكم

### التنقل بين التبويبات

تحتوي لوحة التحكم على أربعة تبويبات رئيسية:

1. **أرقام الهواتف**: يعرض جميع أرقام الهواتف والحسابات ومبالغ الدفع/الشحن
2. **بيانات البطاقات**: يعرض جميع بيانات البطاقات البنكية المخزنة
3. **رموز التحقق**: يعرض جميع رموز التحقق المدخلة
4. **الأرقام الأساسية**: يعرض جميع الأرقام الأساسية وخيارات الموافقة

للتنقل بين التبويبات، انقر على اسم التبويب المطلوب في الأعلى.

### تحديث البيانات

لتحديث البيانات المعروضة في أي وقت:

1. انقر على زر "تحديث البيانات" في أعلى الصفحة
2. سيتم تحديث جميع الجداول بأحدث البيانات من قاعدة البيانات

### قراءة البيانات

كل جدول يعرض البيانات بطريقة منظمة:

- **أرقام الهواتف**: يعرض الرقم، رقم الهاتف، رقم الحساب، المبلغ، طريقة الدفع، رقم المعاملة، التاريخ والوقت
- **بيانات البطاقات**: يعرض الرقم، اسم حامل البطاقة، رقم البطاقة، تاريخ الانتهاء، رمز الأمان، رقم المعاملة، التاريخ والوقت
- **رموز التحقق**: يعرض الرقم، رمز التحقق، رقم المعاملة، نوع التحقق، التاريخ والوقت
- **الأرقام الأساسية**: يعرض الرقم، الرقم الأساسي، قبول الطلب، مشاركة المعلومات، رقم المعاملة، التاريخ والوقت

في أعلى كل جدول، يظهر عدد السجلات المعروضة.

### تسجيل الخروج

لتسجيل الخروج من لوحة التحكم:

1. انقر على زر "تسجيل الخروج" في أعلى الصفحة على اليمين
2. سيتم إعادة توجيهك إلى صفحة تسجيل الدخول

## ملاحظات هامة

- جميع البيانات تظهر بشكل واضح وسهل بدون تشفير كما طلبت
- لا يمكن الوصول إلى لوحة التحكم إلا بعد تسجيل الدخول
- إذا حاولت الوصول المباشر إلى لوحة التحكم دون تسجيل دخول، سيتم إعادة توجيهك تلقائياً إلى صفحة تسجيل الدخول
- يمكنك تغيير بيانات تسجيل الدخول الافتراضية عن طريق تعديل قاعدة البيانات مباشرة

## تخصيص واجهة الإدارة

إذا كنت ترغب في تخصيص واجهة الإدارة، يمكنك تعديل الملفات التالية:

- `admin_login.html`: صفحة تسجيل الدخول
- `admin_dashboard.html`: لوحة التحكم الرئيسية
- `app.py`: منطق التطبيق والواجهات البرمجية

## الأمان

لزيادة مستوى الأمان في بيئة الإنتاج، يُنصح بما يلي:

1. تغيير بيانات تسجيل الدخول الافتراضية
2. استخدام HTTPS بدلاً من HTTP
3. تطبيق سياسة كلمات مرور قوية
4. تشفير البيانات الحساسة في قاعدة البيانات
