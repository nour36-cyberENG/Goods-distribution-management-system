"""
الملف الرئيسي - Main.py
=========================
نظام إدارة محل القهوة المتكامل
يجمع جميع أجزاء المشروع:
1. تسجيل الدخول (Authentication)
2. نظام المستودع والتوزيع (Exported Goods)
3. إدارة الفروع (Branches)
4. الإحصائيات (Statistics)
"""

import sys
import os

# استيراد جميع الوحدات
try:
    from authentication import login
    from exportedGoods import main_second_screen
    from Branches import branches_menu
    from statistic import main_menu as statistics_menu
    from Data import save_data_collection, warehouse_goods, store_branches, distributions_log, next_product_id, \
        next_branch_id
except ImportError as e:
    print(f"❌ خطأ في استيراد الوحدات: {e}")
    print("تأكد من وجود جميع الملفات في نفس المجلد:")
    print("  - authentication.py")
    print("  - exportedGoods.py")
    print("  - Branches.py")
    print("  - statistic.py")
    print("  - Data.py")
    sys.exit(1)


def save_current_data():
    """
    حفظ البيانات الحالية إلى data_collection.json
    """
    try:
        data_obj = {
            "warehouse_goods": warehouse_goods,
            "store_branches": store_branches,
            "distributions_log": distributions_log,
            "next_product_id": next_product_id,
            "next_branch_id": next_branch_id
        }
        save_data_collection(data_obj)
        print("\n💾 تم حفظ البيانات بنجاح!")
    except Exception as e:
        print(f"\n⚠️ تحذير: فشل في حفظ البيانات: {e}")


def display_welcome_banner():
    """عرض شعار الترحيب"""
    print("\n" + "=" * 70)
    print("                  ☕ نظام إدارة محل القهوة المتكامل ☕")
    print("=" * 70)
    print("                     Coffee Shop Management System")
    print("=" * 70)


def display_main_menu():
    """عرض القائمة الرئيسية"""
    print("\n" + "=" * 70)
    print("                         🏠 القائمة الرئيسية")
    print("=" * 70)
    print("\nاختر أحد الخيارات التالية:")
    print("-" * 70)
    print("  1. 📦 نظام المستودع والتوزيع (Warehouse & Distribution)")
    print("  2. 🏪 إدارة الفروع (Branches Management)")
    print("  3. 📊 الإحصائيات والرسوم البيانية (Statistics)")
    print("  0. 🚪 تسجيل الخروج (Logout)")
    print("-" * 70)


def main_menu_loop():
    """حلقة القائمة الرئيسية"""
    while True:
        display_main_menu()

        try:
            choice = input("\n👉 اختيارك (0-3): ").strip()

            if choice == "0":
                # تسجيل الخروج
                print("\n" + "=" * 70)
                save_option = input("هل تريد حفظ البيانات قبل الخروج؟ (نعم/لا): ").strip().lower()
                if save_option in ['نعم', 'yes', 'y']:
                    save_current_data()
                print("\n" + "=" * 70)
                print("                   👋 شكراً لاستخدامك النظام!")
                print("                        نراك قريباً")
                print("=" * 70)
                break

            elif choice == "1":
                # نظام المستودع والتوزيع
                print("\n" + "=" * 70)
                print("         📦 الانتقال إلى نظام المستودع والتوزيع...")
                print("=" * 70)
                try:
                    main_second_screen()
                except Exception as e:
                    print(f"\n❌ حدث خطأ في نظام المستودع: {e}")
                    input("\nاضغط Enter للعودة...")

            elif choice == "2":
                # إدارة الفروع
                print("\n" + "=" * 70)
                print("                🏪 الانتقال إلى إدارة الفروع...")
                print("=" * 70)
                try:
                    branches_menu()
                except Exception as e:
                    print(f"\n❌ حدث خطأ في إدارة الفروع: {e}")
                    input("\nاضغط Enter للعودة...")

            elif choice == "3":
                # الإحصائيات
                print("\n" + "=" * 70)
                print("            📊 الانتقال إلى نظام الإحصائيات...")
                print("=" * 70)
                try:
                    statistics_menu()
                except Exception as e:
                    print(f"\n❌ حدث خطأ في الإحصائيات: {e}")
                    input("\nاضغط Enter للعودة...")


            else:
                print("\n❌ خيار غير صحيح! الرجاء اختيار رقم من 0 إلى 3")
                input("\nاضغط Enter للمتابعة...")

        except KeyboardInterrupt:
            print("\n\n⚠️ تم إيقاف البرنامج")
            save_option = input("هل تريد حفظ البيانات؟ (نعم/لا): ").strip().lower()
            if save_option in ['نعم', 'yes', 'y']:
                save_current_data()
            print("\n👋 إلى اللقاء!")
            break

        except Exception as e:
            print(f"\n❌ حدث خطأ غير متوقع: {e}")
            input("\nاضغط Enter للمتابعة...")


def main():
    """
    نقطة البداية الرئيسية للنظام
    """
    # عرض شعار الترحيب
    display_welcome_banner()

    # صفحة تسجيل الدخول
    print("\n" + "=" * 70)
    print("                  🔐 يجب تسجيل الدخول أولاً")
    print("=" * 70)

    try:
        if login():
            # إذا نجح تسجيل الدخول
            print("\n" + "=" * 70)
            print("                    ✅ تم تسجيل الدخول بنجاح!")
            print("                    الانتقال إلى القائمة الرئيسية...")
            print("=" * 70)
            input("\nاضغط Enter للمتابعة...")

            # دخول القائمة الرئيسية
            main_menu_loop()

        else:
            # إذا فشل تسجيل الدخول
            print("\n" + "=" * 70)
            print("                ❌ فشل تسجيل الدخول!")
            print("            تم رفض الوصول إلى النظام")
            print("=" * 70)
            print("\n💡 ملاحظة: يمكنك المحاولة مرة أخرى بتشغيل البرنامج")

    except KeyboardInterrupt:
        print("\n\n⚠️ تم إلغاء العملية")
        print("👋 إلى اللقاء!")

    except Exception as e:
        print(f"\n❌ حدث خطأ في النظام: {e}")
        print("الرجاء التواصل مع مسؤول النظام")


# ==================================================
# 🚀 نقطة البداية
# ==================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ خطأ فادح: {e}")
        print("تم إنهاء البرنامج")
    finally:
        print("\n" + "=" * 70)
        print("                      تم إغلاق النظام")
        print("=" * 70)