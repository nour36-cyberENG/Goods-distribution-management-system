# plots_menu.py
"""
قائمة تفاعلية لعرض رسمين بناءً على بيانات المشروع (Data.py):

1) رسم توضيحي لكميات الاستيراد استناداً للتاريخ (الأشهر) وكمية البضائع المستوردة من كل صنف
2) رسم توضيحي لكميات التصدير استناداً للعدد الأساسي لكل صنف في المستودع
0) خروج
"""

import importlib
from collections import OrderedDict, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

DATA_MODULE = "Data"

# ألوان افتراضية لكل صنفِ
product_colors = {
    "بن عربي يمني":      "#1f77b4",
    "بن تركي":          "#ff7f0e",
    "بن إسبريسو إيطالي": "#2ca02c",
    "سكر أبيض":          "#d62728",
    "حليب بودرة":       "#9467bd",
    "أكواب ورقية صغيرة": "#8c564b",
    "أكواب ورقية كبيرة": "#e377c2",
    "أغطية أكواب":       "#7f7f7f",
    "مناديل ورقية":      "#bcbd22",
    "شراب فانيلا":       "#17becf",
    "شراب كراميل":      "#aec7e8",
    "شراب هيزل نت":     "#ffbb78",
    "شوكولاتة بلجيكية": "#98df8a",
    "مشروبات باردة - فرابيه مكس": "#ff9896",
    "بسكويت بالشوكولاتة": "#c5b0d5",
    "كرواسون مجمد":      "#c49c94",
    "مصاصات بلاستيك":    "#f7b6d2",
    "قهوة تركية فاخرة":  "#dbdb8d",
}

# -------------------------
# دوال مساعدة
# -------------------------
def load_data_module():
    """استيراد وإعادة تحميل Data.py"""
    mod = __import__(DATA_MODULE)
    importlib.reload(mod)
    return mod

def parse_date_to_month_key(date_str):
    """تحويل تواريخ مثل '2025-01-15' إلى مفتاح شهر '2025-01'"""
    if not date_str:
        return None
    s = str(date_str).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m", "%Y/%m"):
        try:
            d = datetime.strptime(s, fmt)
            return d.strftime("%Y-%m")
        except Exception:
            continue
    parts = [p for p in s.replace("/", "-").split("-") if p]
    if len(parts) >= 2:
        year = None; month = None
        for p in parts:
            if len(p) == 4 and p.isdigit():
                year = p
            elif p.isdigit() and 1 <= int(p) <= 12:
                month = p.zfill(2)
        if year and month:
            return f"{year}-{month}"
    return s

def generate_color_by_index(i, cmap_name="tab20"):
    cmap = plt.get_cmap(cmap_name)
    return cmap(i % cmap.N)

def get_colors_for_products(products):
    colors = []
    for i, p in enumerate(products):
        if p in product_colors:
            colors.append(product_colors[p])
        else:
            colors.append(generate_color_by_index(i))
    return colors

# -------------------------
# 1) رسم الاستيراد عبر الأشهر لكل صنف
# -------------------------
def build_monthly_matrix_from_warehouse(warehouse_goods):
    """
    بناء مصفوفة: لكل منتج (باسمه) تجميع كميات حسب شهر الوصول أو حسب الحقل 'monthly' إن وُجد.
    يعيد: months_sorted, products_list, matrix (OrderedDict: product -> OrderedDict(month->qty))
    """
    temp = defaultdict(lambda: defaultdict(float))
    month_keys = set()
    product_names_order = []

    for pid, info in (warehouse_goods.items() if isinstance(warehouse_goods, dict) else []):
        name = info.get("name") or info.get("category") or f"prod_{pid}"
        product_names_order.append(name)

        # أولاً: إن وجد حقل 'monthly' داخل العنصر (dict)
        if "monthly" in info and isinstance(info["monthly"], dict):
            for k, v in info["monthly"].items():
                mk = parse_date_to_month_key(k)
                try:
                    val = float(v)
                except Exception:
                    val = 0.0
                temp[name][mk] += val
                month_keys.add(mk)
            continue

        if "monthly_amounts" in info and isinstance(info["monthly_amounts"], dict):
            for k, v in info["monthly_amounts"].items():
                mk = parse_date_to_month_key(k)
                try:
                    val = float(v)
                except Exception:
                    val = 0.0
                temp[name][mk] += val
                month_keys.add(mk)
            continue

        # وإلا: استخدم amount مع arrival_date
        try:
            amount = float(info.get("amount", 0))
        except Exception:
            amount = 0.0
        arrival = info.get("arrival_date") or info.get("date") or None
        mk = parse_date_to_month_key(arrival) if arrival else "unknown"
        temp[name][mk] += amount
        month_keys.add(mk)

    # ترتيب مفاتيح الشهور
    def month_key_sorter(k):
        try:
            if k == "unknown":
                return (9999, 12)
            yy, mm = k.split("-")
            return (int(yy), int(mm))
        except Exception:
            return (9999, 12)

    months_sorted = sorted(list(month_keys), key=month_key_sorter)
    if "unknown" in months_sorted:
        months_sorted = [m for m in months_sorted if m != "unknown"] + ["unknown"]

    matrix = OrderedDict()
    for name in product_names_order:
        od = OrderedDict()
        for mk in months_sorted:
            od[mk] = float(temp[name].get(mk, 0.0))
        matrix[name] = od

    return months_sorted, list(matrix.keys()), matrix

def plot_imports_grouped_by_months(mod, save_path="imports_by_months.png", show_values=False):
    warehouse_goods = getattr(mod, "warehouse_goods", {})
    months, products, matrix = build_monthly_matrix_from_warehouse(warehouse_goods)
    n_months = len(months)
    n_products = len(products)

    # ضبط حجم الشكل ليتناسب مع عدد الشهور والمنتجات
    width = max(12, n_months * 1.5)
    height = max(6, 0.25 * n_products + 4)
    figsize = (width, height)

    colors = get_colors_for_products(products)

    x = np.arange(n_months)
    total_width = 0.9
    bar_width = total_width / max(n_products, 1)

    plt.figure(figsize=figsize)
    for i, product in enumerate(products):
        vals = list(matrix[product].values())
        offset = (i - (n_products - 1) / 2) * bar_width
        positions = x + offset
        plt.bar(positions, vals, width=bar_width, label=product, color=colors[i])

        if show_values:
            for j, v in enumerate(vals):
                px = positions[j]
                plt.text(px, v + max(0.01 * (max(vals) if max(vals) else 1), 0.3), f'{v:g}',
                         ha='center', va='bottom', fontsize=6)

    plt.title("كميات الاستيراد عبر الأشهر لكل صنف")
    plt.xlabel("الشهر (YYYY-MM)")
    plt.ylabel("الكمية")
    plt.xticks(x, months, rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

    if n_products > 8:
        plt.legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0.)
    else:
        plt.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"تم حفظ رسم الاستيراد في: {save_path}")

# -------------------------
# 2) رسم التصدير مقابل المخزون (الكود الذي زودتيني به سابقاً)
# -------------------------
COLOR_BASE = "#C9A3FF"    # بنفسجي (العدد الأساسي في المستودع)
COLOR_IMPORTED = "#FF94A6" # وردي (العدد المستورد)
COLOR_EXPORTED = "#FFB84D" # أصفر/برتقالي (العدد المصدّر)
COLOR_DIFF = "#3AA1FF"     # أزرق (الفرق بين المستورد والمصدر)
#تجميع ما صدر من سجل التوزيع #
def aggregate_exports(distributions_log):
    exported_sum = defaultdict(float)
    for rec in (distributions_log or []):
        pid = rec.get("product_id") if isinstance(rec, dict) else None
        qty = rec.get("quantity", 0) if isinstance(rec, dict) else 0
        try:
            exported_sum[int(pid)] += float(qty)
        except Exception:
            continue
    return exported_sum
##حساب اجمالي الاستيراد والفرق بين الاستيراد والتصدير
def prepare_series(warehouse_goods, exported_sum):
    names = []
    base_totals = []
    imported_totals = []
    exported_totals = []
    diffs = []

    for pid in sorted(warehouse_goods.keys()):
        info = warehouse_goods[pid]
        name = info.get("name", f"prod_{pid}")
        try:
            current = float(info.get("amount", 0))
        except Exception:
            current = 0.0
        exported = float(exported_sum.get(pid, 0.0))
        imported_total = current + exported
        diff = imported_total - exported

        names.append(name)
        base_totals.append(imported_total)
        imported_totals.append(imported_total)
        exported_totals.append(exported)
        diffs.append(diff)

    return names, base_totals, imported_totals, exported_totals, diffs

def plot_exports_vs_stock_from_project(mod, savepath="exports_vs_stock_chart.png", show_values=True):
    warehouse_goods = getattr(mod, "warehouse_goods", {})
    distributions_log = getattr(mod, "distributions_log", [])

    exported_sum = aggregate_exports(distributions_log)
    names, base_totals, imported_totals, exported_totals, diffs = prepare_series(warehouse_goods, exported_sum)

    n = len(names)
    x = np.arange(n)
    n_bars = 4
    total_w = 0.8
    bar_w = total_w / n_bars
    offsets = [ (i - (n_bars-1)/2) * bar_w for i in range(n_bars) ]

    figsize = (max(14, n * 0.6), 6)
    plt.figure(figsize=figsize)

    plt.bar(x + offsets[0], base_totals, width=bar_w, label="العدد الأساسي في المستودع", color=COLOR_BASE)
    plt.bar(x + offsets[1], imported_totals, width=bar_w, label="العدد المستورد", color=COLOR_IMPORTED)
    plt.bar(x + offsets[2], exported_totals, width=bar_w, label="العدد المصدَّر", color=COLOR_EXPORTED)
    plt.bar(x + offsets[3], diffs, width=bar_w, label="الفرق بين المستورد والمصدر", color=COLOR_DIFF)

    if show_values:
        for i in range(n):
            vals = [base_totals[i], imported_totals[i], exported_totals[i], diffs[i]]
            for j, val in enumerate(vals):
                xpos = x[i] + offsets[j]
                plt.text(xpos, val + max(0.01*val, 0.5), f'{val:g}', ha='center', va='bottom', fontsize=7)

    plt.xticks(x, names, rotation=45, ha='right')
    plt.xlabel("الصنف")
    plt.ylabel("الكمية")
    plt.title("مقارنة: العدد الأساسي - العدد المستورد - العدد المصدَّر - الفرق")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=4, frameon=True)

    plt.tight_layout()
    plt.savefig(savepath, dpi=150)
    plt.show()
    print(f"تم حفظ رسم التصدير في: {savepath}")

# -------------------------
# واجهة المستخدم
# -------------------------
def main_menu():
    while True:
        print("\n" + "="*60)
        print("اختر الرسم الذي تريد عرضه:")
        print("1. رسم كميات الاستيراد استناداً للتاريخ وكمية البضائع المستوردة من كل صنف")
        print("2. رسم كميات التصدير استناداً للعدد الأساسي لكل صنف في المستودع")
        print("0. خروج")
        print("="*60)
        choice = input("اختيارك: ").strip()
        if choice == "0":
            print("خروج. مع السلامة!")
            break
        try:
            mod = load_data_module()  # إعادة تحميل البيانات في كل مرة
            if choice == "1":
                plot_imports_grouped_by_months(mod, show_values=False)
            elif choice == "2":
                plot_exports_vs_stock_from_project(mod, show_values=True)
            else:
                print("خيار غير معروف، حاول مرة أخرى.")
        except Exception as e:
            print(f"حصل خطأ: {e}")

if __name__ == "__main__":
    main_menu()
