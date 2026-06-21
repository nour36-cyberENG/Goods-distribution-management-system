# Data.py
"""
ملف البيانات المشترك - Data.py
===================================
يحتوي على جميع البيانات المشتركة بين الملفات
ويقوم بتحميل وحفظ data collection (data_collection.json) تلقائياً.
"""

import os
import json
from datetime import datetime

DATA_COLLECTION_FILE = "data_collection.json"

# ---------------------------
# دوال تحميل / حفظ الـ data collection
# ---------------------------
def load_data_collection():
    """
    تحميل محتوى data_collection.json إن وجد.
    """
    if not os.path.exists(DATA_COLLECTION_FILE):
        return {}
    try:
        with open(DATA_COLLECTION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        return {}


def save_data_collection(data_obj):
    """
    حفظ كائن البيانات إلى ملف JSON.
    """
    try:
        # قبل الحفظ: تحويل مفاتيح dict إلى سلاسل لجعل JSON صالحاً
        safe_obj = {}
        for k, v in data_obj.items():
            if isinstance(v, dict):
                # تأكد من تحويل مفاتيح القواميس الداخلية إلى سلاسل
                safe_inner = {}
                for ik, iv in v.items():
                    safe_inner[str(ik)] = iv
                safe_obj[k] = safe_inner
            else:
                safe_obj[k] = v

        with open(DATA_COLLECTION_FILE, "w", encoding="utf-8") as f:
            json.dump(safe_obj, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"تحذير: فشل في حفظ data collection: {e}")


# ---------------------------
# دوال مساعدة لتحويل مفاتيح JSON إلى أعداد صحيحة إذا لزم
# ---------------------------
def keys_to_int_if_possible(d):
    """
    إذا كانت مفاتيح dict هي أعداد على شكل نص، نُحوّلها إلى int.
    """
    if not isinstance(d, dict):
        return d
    new = {}
    for k, v in d.items():
        try:
            ik = int(k)
        except Exception:
            ik = k
        new[ik] = v
    return new

# ==================================================
# البضائع المستودعة (القيم الافتراضية الأصلية)
# ==================================================

warehouse_goods = {
    1: {"name": "بن عربي يمني", "amount": 50, "price": 45, "arrival_date": "2025-01-15", "cost": 35, "import_location": "اليمن", "unit": "كغ"},
    2: {"name": "بن تركي", "amount": 30, "price": 35, "arrival_date": "2025-01-15", "cost": 28, "import_location": "تركيا", "unit": "كغ"},
    3: {"name": "بن إسبريسو إيطالي", "amount": 25, "price": 55, "arrival_date": "2025-01-15", "cost": 42, "import_location": "إيطاليا", "unit": "كغ"},
    4: {"name": "سكر أبيض", "amount": 200, "price": 1.2, "arrival_date": "2025-01-10", "cost": 0.85, "import_location": "مصر", "unit": "كغ"},
    5: {"name": "حليب بودرة", "amount": 100, "price": 8.5, "arrival_date": "2025-01-20", "cost": 6.5, "import_location": "نيوزيلندا", "unit": "كغ"},
    6: {"name": "أكواب ورقية صغيرة", "amount": 5000, "price": 0.08, "arrival_date": "2025-01-05", "cost": 0.05, "import_location": "الصين", "unit": "قطعة"},
    7: {"name": "أكواب ورقية كبيرة", "amount": 3000, "price": 0.12, "arrival_date": "2025-01-05", "cost": 0.08, "import_location": "الصين", "unit": "قطعة"},
    8: {"name": "أغطية أكواب", "amount": 8000, "price": 0.03, "arrival_date": "2025-01-05", "cost": 0.02, "import_location": "الصين", "unit": "قطعة"},
    9: {"name": "مناديل ورقية", "amount": 150, "price": 1.5, "arrival_date": "2025-01-18", "cost": 1.0, "import_location": "تركيا", "unit": "علبة"},
    10: {"name": "شراب فانيلا", "amount": 40, "price": 12, "arrival_date": "2025-01-22", "cost": 9, "import_location": "أمريكا", "unit": "زجاجة"},
    11: {"name": "شراب كراميل", "amount": 35, "price": 12, "arrival_date": "2025-01-22", "cost": 9, "import_location": "أمريكا", "unit": "زجاجة"},
    12: {"name": "شراب هيزل نت", "amount": 30, "price": 13, "arrival_date": "2025-01-22", "cost": 10, "import_location": "أمريكا", "unit": "زجاجة"},
    13: {"name": "شوكولاتة بلجيكية", "amount": 20, "price": 18, "arrival_date": "2025-01-25", "cost": 14, "import_location": "بلجيكا", "unit": "كغ"},
    14: {"name": "مشروبات باردة - فرابيه مكس", "amount": 60, "price": 8, "arrival_date": "2025-01-12", "cost": 6, "import_location": "تركيا", "unit": "علبة"},
    15: {"name": "بسكويت بالشوكولاتة", "amount": 80, "price": 2.5, "arrival_date": "2025-01-28", "cost": 1.8, "import_location": "السعودية", "unit": "علبة"},
    16: {"name": "كرواسون مجمد", "amount": 100, "price": 0.8, "arrival_date": "2025-01-28", "cost": 0.5, "import_location": "السعودية", "unit": "قطعة"},
    17: {"name": "مصاصات بلاستيك", "amount": 10000, "price": 0.02, "arrival_date": "2025-01-05", "cost": 0.01, "import_location": "الصين", "unit": "قطعة"},
    18: {"name": "قهوة تركية فاخرة", "amount": 15, "price": 42, "arrival_date": "2025-01-15", "cost": 32, "import_location": "تركيا", "unit": "كغ"}
}

# ==================================================
# الفروع (القيم الافتراضية)
# ==================================================

store_branches = {
    1: {"الاسم": "فرع عبدون", "المكان": "", "هاتف مدير الفرع": "0765954227"},
    2: {"الاسم": "فرع المدينة الرياضية", "المكان": "بجانب الاستاد الرياضي", "هاتف مدير الفرع": "0769745318"},
    3: {"الاسم": "فرع بوليفارد العبدلي", "المكان": "بجانب امازون", "هاتف مدير الفرع": "0764497259"},
    4: {"الاسم": "فرع الصويفية", "المكان": "بجانب مجوهرات العامودي", "هاتف مدير الفرع": "0762711889"},
    5: {"الاسم": "فرع الجامعة الأردنية", "المكان": "بجانب مطعم ماكدونالدز", "هاتف مدير الفرع": "0763499752"},
    6: {"الاسم": "فرع مكة مول", "المكان": "الطابق الأول", "هاتف مدير الفرع": "0796001239"},
    7: {"الاسم": "فرع تاج مول", "المكان": "الطابق الثاني", "هاتف مدير الفرع": "0796001240"}
}

# ==================================================
# سجل التوزيع (قيمة افتراضية  )
# ==================================================

distributions_log = []

# ==================================================
# معرفات تلقائية (افتراضية)
# ==================================================

next_product_id = max(warehouse_goods.keys()) + 1 if warehouse_goods else 1
next_branch_id = max(store_branches.keys()) + 1 if store_branches else 1

# ==================================================
# تحميل بيانات محفوظة (إن وُجدت) واستبدال القيم الافتراضية بحالتها المحفوظة
# ==================================================
_loaded = load_data_collection()
if _loaded:
    # warehouse_goods
    if "warehouse_goods" in _loaded and isinstance(_loaded["warehouse_goods"], dict):
        # تحويل مفاتيح المحتملة إلى int
        warehouse_goods = keys_to_int_if_possible(_loaded["warehouse_goods"])
    if "store_branches" in _loaded and isinstance(_loaded["store_branches"], dict):
        store_branches = keys_to_int_if_possible(_loaded["store_branches"])
    if "distributions_log" in _loaded and isinstance(_loaded["distributions_log"], list):
        distributions_log = _loaded["distributions_log"]
    if "next_product_id" in _loaded:
        try:
            next_product_id = int(_loaded["next_product_id"])
        except Exception:
            pass
    if "next_branch_id" in _loaded:
        try:
            next_branch_id = int(_loaded["next_branch_id"])
        except Exception:
            pass
