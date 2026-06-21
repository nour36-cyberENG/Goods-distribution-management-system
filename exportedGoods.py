from datetime import datetime

# ==================================================
# نظام إدارة مستودع محل قهوة ☕
# ==================================================

# استيراد المتغيرات من Data.py
from Data import warehouse_goods, store_branches, distributions_log, next_product_id, next_branch_id
import Data  # للاستفادة من دوال الحفظ load/save في Data.py

# ==================================================
# دالة مساعدة لطباعة جميع البضائع
# ==================================================

def list_all_goods():
    """عرض قائمة مختصرة بجميع البضائع"""
    for gid, item in sorted(warehouse_goods.items()):
        unit = item.get('unit', 'قطعة')
        print(f"  {gid}. {item['name']} - متوفر: {item['amount']} {unit}")


# ==================================================
# 1️⃣ إضافة بضائع جديدة للمستودع
# ==================================================

def add_warehoused_goods():
    """
    توريد أصناف موجودة: زيادة الكميات للأصناف في المستودع.
    لا تضيف صنفًا جديدًا. تحفظ التغييرات في Data.save_data_collection().
    """
    # استخدام المتغيرات المستوردة من Data
    global warehouse_goods

    if not warehouse_goods:
        print("\n⚠️ لا توجد أصناف في المستودع حالياً!")
        input("اضغط Enter للعودة...")
        return

    while True:
        print("\n" + "=" * 60)
        print("      📦 توريد أصناف (زيادة كميات في المستودع)")
        print("=" * 60)

        # عرض الأصناف الحالية
        list_all_goods()
        print("\n0. الرجوع للقائمة الرئيسية")

        try:
            prod_choice_str = input("\nأدخل رقم الصنف الذي تريد توريده (أو 0 للرجوع): ").strip()
            if prod_choice_str == '0':
                print("↩️ العودة للقائمة الرئيسية...")
                return

            prod_choice = int(prod_choice_str)
        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح للصنف.")
            continue

        if prod_choice not in warehouse_goods:
            print("❌ رقم المنتج غير موجود!")
            continue

        product = warehouse_goods[prod_choice]
        unit = product.get('unit', 'قطعة')
        print(f"\n📊 الصنف المختار: {product['name']} - المتوفر الآن: {product['amount']} {unit}")

        # إدخال كمية التوريد (إجبار المستخدم على إدخال رقم صحيح > 0)
        try:
            qty_input = input(f"أدخل كمية التوريد (بـ {unit}) أو 0 للرجوع: ").strip()
            if qty_input == '0':
                print("↩️ إلغاء التوريد، العودة لاختيار صنف آخر...")
                continue
            add_qty = float(qty_input)
        except ValueError:
            print("❌ الرجاء إدخال رقم صالح للكمية.")
            continue

        if add_qty <= 0:
            print("❌ الكمية يجب أن تكون أكبر من صفر.")
            continue

        # إدخال تاريخ الوصول (نحتاج تاريخ صالح أو 0 لإلغاء)
        while True:
            date_input = input("أدخل تاريخ وصول الشحنة (YYYY-MM-DD) أو 0 للرجوع: ").strip()
            if date_input == '0':
                print("↩️ إلغاء التوريد، العودة لاختيار صنف آخر...")
                break
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                arrival_date = date_input
                break
            except ValueError:
                print("❌ تنسيق التاريخ غير صحيح. اكتب YYYY-MM-DD أو 0 للرجوع.")

        if date_input == '0':
            continue

        # هل تريدين تحديث التكلفة أو السعر لهذا الصنف؟ (اختياري)
        try:
            update_choice = input("هل تريدين تحديث (تكلفة/سعر) هذا الصنف؟ اكتب 'نعم' للتحديث أو أي شيء للمتابعة: ").strip()
            if update_choice.lower() == 'نعم':
                # تكلفة جديدة؟
                try:
                    new_cost_input = input(f"أدخل تكلفة الوحدة الجديدة (حاليًا {product.get('cost')}) أو 0 لتخطي: ").strip()
                    if new_cost_input != '0' and new_cost_input != '':
                        new_cost = float(new_cost_input)
                        if new_cost > 0:
                            product['cost'] = new_cost
                except ValueError:
                    print("⚠️ تم تجاهل قيمة التكلفة غير الصالحة.")

                # سعر بيع جديد؟
                try:
                    new_price_input = input(f"أدخل سعر البيع الجديد (حاليًا {product.get('price')}) أو 0 لتخطي: ").strip()
                    if new_price_input != '0' and new_price_input != '':
                        new_price = float(new_price_input)
                        if new_price > 0:
                            product['price'] = new_price
                except ValueError:
                    print("⚠️ تم تجاهل قيمة السعر غير الصالحة.")
        except Exception:
            pass

        # تنفيذ التوريد: زيادة الكمية وتحديث تاريخ الوصول (نضع التاريخ الأخير كـ arrival_date)
        previous_amount = product['amount']
        product['amount'] = round(previous_amount + add_qty, 4)
        # نحدّث تاريخ الوصول إلى التاريخ الذي أدخلته
        product['arrival_date'] = arrival_date

        # حساب قيمة البضاعة الموردة (بناءً على تكلفة الوحدة)
        added_value = product.get('cost', 0) * add_qty

        # حفظ الحالة في Data (نستخدم Data.save_data_collection كما في باقي الكود)
        try:
            Data.save_data_collection({
                "warehouse_goods": Data.warehouse_goods,
                "store_branches": Data.store_branches,
                "distributions_log": Data.distributions_log,
                "next_product_id": Data.next_product_id,
                "next_branch_id": Data.next_branch_id
            })
        except Exception as e:
            print(f"⚠️ تحذير: فشل حفظ البيانات بعد التوريد: {e}")

        # إخراج ملخص التوريد
        print("\n" + "=" * 60)
        print("      ✅ تم توريد الأصناف بنجاح")
        print("=" * 60)
        print(f"المنتج: {product['name']}")
        print(f"الكمية المضافة: {add_qty} {unit}")
        print(f"الكمية قبل التوريد: {previous_amount} {unit}")
        print(f"الكمية الآن في المستودع: {product['amount']} {unit}")
        print(f"قيمة الكمية المضافة (بالتكلفة): {added_value:.2f} دينار")
        print(f"آخر تاريخ وصول تم تسجيله: {product['arrival_date']}")
        print("=" * 60)

        # خيارات بعد التوريد
        print("\n1. توريد صنف آخر")
        print("2. العودة للقائمة الرئيسية")
        next_action = input("اختيارك: ").strip()
        if next_action == "2":
            print("↩️ العودة للقائمة الرئيسية...")
            return
        # أي خيار آخر يعيد الحلقة (توريد صنف آخر)

# ==================================================
# 2️⃣ عرض البضائع المتاحة في المستودع
# ==================================================

def display_available_goods():
    """عرض البضائع - الخيار 1 من قائمة "بضائع مصدرة إلى الأفرع" """

    if not warehouse_goods:
        print("\n⚠️ لا توجد بضائع في المستودع!")
        input("\nاضغط Enter للعودة...")
        return

    while True:
        print("\n" + "=" * 60)
        print("      📋 البضائع المتاحة في المستودع الرئيسي")
        print("=" * 60)

        list_all_goods()

        print("\n0. الرجوع")

        try:
            choice = int(input("\nأدخل رقم المنتج لعرض تفاصيله الكاملة (أو 0 للرجوع): ").strip())

            if choice == 0:
                print("↩️ العودة للقائمة السابقة...")
                return

            if choice in warehouse_goods:
                product = warehouse_goods[choice]
                unit = product.get('unit', 'قطعة')
                profit_per_unit = product['price'] - product['cost']

                print("\n" + "=" * 60)
                print(f"      📦 تفاصيل المنتج الكاملة")
                print("=" * 60)
                print(f"اسم المنتج: {product['name']}")
                print(f"الكمية المتوفرة: {product['amount']} {unit}")
                print(f"سعر البيع: {product['price']:.2f} دينار/{unit}")
                print(f"تكلفة الاستيراد: {product['cost']:.2f} دينار/{unit}")
                print(f"الربح لكل وحدة: {profit_per_unit:.2f} دينار")
                print(f"تاريخ الوصول: {product['arrival_date']}")
                print(f"مكان الاستيراد: {product['import_location']}")
                print("=" * 60)

                input("\nاضغط Enter للعودة...")
            else:
                print("❌ رقم المنتج غير موجود!")

        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح!")


# ==================================================
# 3️⃣ توزيع البضائع على الفروع (مكان التوزيع)
# ==================================================

def distribution_to_branches():
    """توزيع البضائع - الخيار 2 من قائمة "بضائع مصدرة إلى الأفرع" """

    if not warehouse_goods:
        print("\n⚠️ لا توجد بضائع في المستودع للتوزيع!")
        input("\nاضغط Enter للعودة...")
        return

    while True:
        # عرض الفروع
        print("\n" + "=" * 60)
        print("      🚚 مكان التوزيع - اختيار الفرع")
        print("=" * 60)
        print("\nالفروع المتاحة:")

        for branch_id, branch_info in store_branches.items():
            # branch_info قد يكون dict أو اسم بسيط؛ نتعامل مع كلا الحالتين
            if isinstance(branch_info, dict):
                print(f"{branch_id}. {branch_info.get('الاسم')}")
            else:
                print(f"{branch_id}. {branch_info}")
        print("0. الرجوع")

        try:
            branch_choice = int(input("\nاختر رقم الفرع (أو 0 للرجوع): ").strip())

            if branch_choice == 0:
                print("↩️ العودة للقائمة السابقة...")
                return

            if branch_choice not in store_branches:
                print("❌ رقم الفرع غير موجود!")
                continue

            branch_info = store_branches[branch_choice]
            branch_name = branch_info.get("الاسم") if isinstance(branch_info, dict) else str(branch_info)
            print(f"\n✅ تم اختيار: {branch_name}")

            # عرض البضائع المتوفرة
            print("\n" + "=" * 60)
            print("📦 البضائع المتوفرة للتوزيع:")
            print("=" * 60)
            list_all_goods()
            print("\n0. الرجوع لاختيار فرع آخر")

            product_choice = int(input("\nاختر رقم المنتج للتوزيع (أو 0 للرجوع): ").strip())

            if product_choice == 0:
                print("↩️ العودة لاختيار الفرع...")
                continue

            if product_choice not in warehouse_goods:
                print("❌ رقم المنتج غير موجود!")
                continue

            product = warehouse_goods[product_choice]
            unit = product.get('unit', 'قطعة')

            print(f"\n📊 المنتج المختار: {product['name']}")
            print(f"الكمية المتوفرة في المستودع: {product['amount']} {unit}")

            # إدخال الكمية - loop منفصل لإعادة المحاولة
            qty = None
            while qty is None:
                try:
                    qty_input = input(f"\nأدخل الكمية المراد توزيعها ({unit}) أو 0 للرجوع: ").strip()
                    qty = float(qty_input)

                    if qty == 0:
                        print("↩️ إلغاء التوزيع...")
                        qty = False  # علامة للإلغاء
                        break

                    if qty < 0:
                        print("❌ الكمية يجب أن تكون أكبر من صفر!")
                        qty = None  # إعادة المحاولة
                        continue

                    if qty > product['amount']:
                        print(f"❌ الكمية المطلوبة ({qty}) أكبر من المتوفر ({product['amount']})!")
                        qty = None  # إعادة المحاولة
                        continue

                except ValueError:
                    print("❌ الرجاء إدخال رقم صحيح للكمية")
                    qty = None  # إعادة المحاولة

            # إذا تم الإلغاء، نعود لاختيار منتج آخر
            if qty is False:
                continue

            # إدخال تاريخ التوصيل - loop منفصل لإعادة المحاولة
            delivery_date = None
            while delivery_date is None:
                date_input = input("أدخل تاريخ توصيل البضاعة (YYYY-MM-DD) أو 0 للرجوع: ").strip()

                if date_input == '0':
                    print("↩️ إلغاء التوزيع...")
                    delivery_date = False  # علامة للإلغاء
                    break

                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    delivery_date = date_input  # التاريخ صحيح
                except ValueError:
                    print("❌ تنسيق التاريخ غير صحيح! استخدم: YYYY-MM-DD")
                    print("💡 مثال: 2025-02-15")
                    # سيعيد المحاولة تلقائياً

            # إذا تم الإلغاء، نعود لاختيار فرع آخر
            if delivery_date is False:
                continue

            # حساب الربح والمبيعات
            profit_per_unit = product['price'] - product['cost']
            total_profit = profit_per_unit * qty
            total_revenue = product['price'] * qty

            # عرض ملخص قبل التأكيد
            print("\n" + "=" * 60)
            print("      📋 ملخص التوزيع - يرجى المراجعة")
            print("=" * 60)
            print(f"الفرع: {branch_name}")
            print(f"المنتج: {product['name']}")
            print(f"الكمية: {qty} {unit}")
            print(f"تاريخ التوصيل: {delivery_date}")
            print(f"سعر الوحدة: {product['price']:.2f} دينار")
            print(f"إجمالي المبيعات: {total_revenue:.2f} دينار")
            print(f"الربح المتوقع: {total_profit:.2f} دينار")
            print("=" * 60)

            confirm = input("\nهل تريد تأكيد التوزيع؟ (نعم/لا): ").strip().lower()

            if confirm not in ['نعم', 'yes', 'y']:
                print("❌ تم إلغاء التوزيع")
                continue

            # تنفيذ التوزيع - خصم الكمية من المستودع
            warehouse_goods[product_choice]['amount'] -= qty

            # حفظ سجل التوزيع
            distribution_record = {
                "branch": branch_name,
                "product_name": product['name'],
                "product_id": product_choice,
                "quantity": qty,
                "unit": unit,
                "delivery_date": delivery_date,
                "unit_price": product['price'],
                "total_revenue": total_revenue,
                "profit_per_unit": profit_per_unit,
                "total_profit": total_profit,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            distributions_log.append(distribution_record)

            # حفظ الحالة (المخزون والسجل والمعرفات) في Data.data_collection.json
            try:
                Data.save_data_collection({
                    "warehouse_goods": Data.warehouse_goods,
                    "store_branches": Data.store_branches,
                    "distributions_log": Data.distributions_log,
                    "next_product_id": Data.next_product_id,
                    "next_branch_id": Data.next_branch_id
                })
            except Exception as e:
                print(f"تحذير: فشل حفظ البيانات بعد التوزيع: {e}")

            # عرض رسالة النجاح
            print("\n" + "=" * 60)
            print("      ✅ تم التوزيع بنجاح!")
            print("=" * 60)
            print(f"✓ الفرع: {branch_name}")
            print(f"✓ المنتج: {product['name']}")
            print(f"✓ الكمية الموزعة: {qty} {unit}")
            print(f"✓ إجمالي المبيعات: {total_revenue:.2f} دينار")
            print(f"✓ الربح الإجمالي: {total_profit:.2f} دينار")
            print(f"✓ الكمية المتبقية في المستودع: {warehouse_goods[product_choice]['amount']} {unit}")
            print("=" * 60)

            # خيارات بعد التوزيع
            print("\n" + "-" * 40)
            print("ماذا تريد أن تفعل الآن؟")
            print("-" * 40)
            print("1. توزيع بضاعة أخرى")
            print("2. العودة للقائمة الرئيسية")
            print("-" * 40)

            next_action = input("اختيارك: ").strip()

            if next_action == "2":
                print("↩️ العودة للقائمة الرئيسية...")
                return
            # أي خيار آخر يعيد للبداية (توزيع بضاعة أخرى)

        except ValueError:
            print("❌ خطأ في الإدخال! الرجاء إدخال رقم صحيح")
        except KeyboardInterrupt:
            print("\n\n⚠️ تم إلغاء العملية")
            return


# ==================================================
# 4️⃣ قائمة "بضائع مصدرة إلى الأفرع"
# ==================================================

def exported_goods_menu():
    """الخيار 2 من القائمة الرئيسية - يحتوي على خيارين فرعيين"""

    while True:
        print("\n" + "=" * 60)
        print("      📤 بضائع مصدرة إلى الأفرع")
        print("=" * 60)
        print("\nاختر أحد الخيارات التالية:")
        print("-" * 60)
        print("1. عرض البضائع المتاحة في المستودع الرئيسي")
        print("2. مكان التوزيع (توزيع البضائع على الفروع)")
        print("0. الرجوع للقائمة الرئيسية")
        print("-" * 60)

        try:
            choice = int(input("\nاختر رقم الخيار: ").strip())

            if choice == 0:
                print("↩️ العودة للقائمة الرئيسية...")
                return
            elif choice == 1:
                display_available_goods()
            elif choice == 2:
                distribution_to_branches()
            else:
                print("❌ خيار غير صحيح! الرجاء اختيار 0 أو 1 أو 2")

        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح!")
        except KeyboardInterrupt:
            print("\n\n⚠️ تم إلغاء العملية")
            return


# ==================================================
# 🏠 القائمة الرئيسية (خياران فقط)
# ==================================================

def main_second_screen():
    """القائمة الرئيسية - حسب المتطلبات الدقيقة"""

    print("\n" + "=" * 60)
    print("      ☕ مرحباً في نظام إدارة مستودع محل القهوة")
    print("=" * 60)

    while True:
        print("\n" + "=" * 60)
        print("القائمة الرئيسية:")
        print("=" * 60)
        print("1. بضائع مستودعة (إضافة بضائع جديدة)")
        print("2. بضائع مصدرة إلى الأفرع")
        print("0. تسجيل الخروج")
        print("=" * 60)

        try:
            main_choice = int(input("\nاختر رقم الخيار: ").strip())

            if main_choice == 0:
                print("\n" + "=" * 60)
                print("👋 شكراً لاستخدامك نظام إدارة مستودع محل القهوة")
                print("   تم تسجيل الخروج بنجاح!")
                print("=" * 60)
                break
            elif main_choice == 1:
                add_warehoused_goods()
            elif main_choice == 2:
                exported_goods_menu()
            else:
                print("❌ خيار غير صحيح! الرجاء اختيار 0 أو 1 أو 2")

        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح!")
        except KeyboardInterrupt:
            print("\n\n⚠️ تم إنهاء البرنامج")
            print("👋 إلى اللقاء!")
            break


# ==================================================
# 🚀 نقطة البداية
# ==================================================

if __name__ == "__main__":
    main_second_screen()
