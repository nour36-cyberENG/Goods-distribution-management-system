# صفحة تسجيل الدخول

users = {
    "admin": "1234",
    "nour": "pass"
}

def login():
    print("==========================================")
    print("      مرحباً بك في نظام تسجيل الدخول")
    print("==========================================" )

    for attempt in range(3):
        print(f"\nالمحاولة {attempt + 1} من 3")
        username = input("أدخل اسم المستخدم: ").strip()
        password = input("أدخل كلمة المرور: ").strip()


        # التحقق من الإدخال الفارغ
        if not username or not password:
            print(" خطأ: لا يمكن ترك الحقول فارغة!")
            continue

        # التحقق من صحة البيانات
        if users.get(username) == password:
            print("\n تم تسجيل الدخول بنجاح!")
            print(f"مرحباً {username}!")
            return True
        else:
            remaining =\
                3 - attempt - 1
            if remaining > 0:
                print(f" خطأ! اسم المستخدم أو كلمة المرور غير صحيحة")
                print(f"المحاولات المتبقية: {remaining}")

    # بعد استنفاد المحاولات
    print("\n" + "==========================================")
    print(" نأسف! لقد استنفذت جميع المحاولات")
    print("   تم رفض الوصول إلى النظام")
    print("==========================================")
    return False


# اختبار الدالة
if __name__ == "__main__":
    if login():
        print("\n🎉 الانتقال إلى الصفحة الرئيسية...")
        # هنا استدعاء الصفحة الثانية
    else:
        print("\n شكراً لاستخدامك النظام")