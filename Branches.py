"""
شاشة إدارة الفروع - branches.py
===================================
نظام إدارة فروع محل القهوة
"""

# استيراد البيانات من ملف data.py
from Data import store_branches


def print_branches_list():
    """عرض قائمة الفروع"""
    print("\nقائمة الفروع (الرقم: الاسم):")
    for bid, info in store_branches.items():
        print(f"  {bid}: {info.get('الاسم')}")


def delete_branch():
    """حذف فرع"""
    print_branches_list()
    try:
        bid = int(input("\nاكتب رقم الفرع الذي تريد حذفه (أو 0 للعودة): ").strip())
    except ValueError:
        print("❌ رقم غير صالح.")
        return
    if bid == 0:
        return
    if bid not in store_branches:
        print("❌ هذا الرقم غير موجود.")
        return

    # تأكيد الحذف
    name = store_branches[bid].get("الاسم")
    confirm = input(f"هل أنت متأكد أنك تريد حذف الفرع '{name}'؟ اكتب 'نعم' للتأكيد: ").strip()
    if confirm == "نعم":
        store_branches.pop(bid)
        print(f"✅ تم حذف الفرع '{name}'.")
    else:
        print("تم إلغاء الحذف.")


def edit_branch():
    """تعديل معلومات فرع"""
    print_branches_list()
    try:
        bid = int(input("\nاختر رقم الفرع الذي تريد تعديل معلوماته (أو 0 للعودة): ").strip())
    except ValueError:
        print("❌ رقم غير صالح.")
        return
    if bid == 0:
        return
    if bid not in store_branches:
        print("❌ هذا الرقم غير موجود.")
        return

    branch = store_branches[bid]
    # عرض الحقول المتاحة للتعديل برقم لكل حقل
    print(f"\nمعلومات الفرع '{branch.get('الاسم')}' الحالية:")
    fields = list(branch.items())  # قائمة من (key, value)
    for idx, (k, v) in enumerate(fields, start=1):
        print(f"  {idx}. {k}: {v}")

    try:
        choice = int(input("اختر رقم المعلومة التي تريد تعديلها (أو 0 للعودة): ").strip())
    except ValueError:
        print("❌ رقم غير صالح.")
        return
    if choice == 0:
        return
    if not (1 <= choice <= len(fields)):
        print("❌ اختيار خارج النطاق.")
        return

    key_to_edit = fields[choice - 1][0]
    new_value = input(f"ادخل القيمة الجديدة لحقل '{key_to_edit}': ").strip()
    if new_value == "":
        print("❌ لا يمكن ترك القيمة فارغة.")
        return
    store_branches[bid][key_to_edit] = new_value
    print(f"✅ تم تحديث '{key_to_edit}' للفرع '{store_branches[bid].get('الاسم')}'.")


def branches_menu():
    """القائمة الرئيسية لإدارة الفروع"""
    while True:
        print("\n--- شاشة إدارة الفروع ---")
        print("1. عرض الفروع كافة")
        print("2. حذف فرع")
        print("3. تعديل معلومات فرع")
        print("4. خروج")
        choice = input("اكتب رقم العملية التي تريد: ").strip()

        if choice == "1":
            print_branches_list()
        elif choice == "2":
            delete_branch()
        elif choice == "3":
            edit_branch()
        elif choice == "4":
            print("خروج من إدارة الفروع.")
            break
        else:
            print("❌ خيار غير معروف. حاول مرة أخرى.")


# ==================================================
# 🚀 نقطة البداية (للاختبار المستقل)
# ==================================================

if __name__ == "__main__":
    branches_menu()