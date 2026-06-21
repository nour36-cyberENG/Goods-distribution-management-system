# Goods-distribution-management-system
A comprehensive Python-based POS system featuring secure login, goods distribution, multi-branch handling, and real-time data analytics with matplotlib.
```markdown
# Integrated Coffee Shop Management System ☕

## 🎯 Overview

A comprehensive system for managing a coffee shop, including:
- 🔐 Secure login system
- 📦 Warehouse and distribution management
- 🏪 Branch management
- 📊 Dynamic statistics and charts

---

## 📁 Project Structure

```
coffee-shop-system/
│
├── 🎯 Main.py                      # Main entry point
│   └─→ Brings all modules together
│
├── 🔐 authentication.py            # Login system
│   ├─ User data
│   ├─ 3 login attempts
│   └─ Data validation
│
├── 📦 exportedGoods.py             # Warehouse system
│   ├─ Supply items (increase quantities)
│   ├─ View available goods
│   └─ Distribute to branches
│
├── 🏪 Branches.py                  # Branch management
│   ├─ View all branches
│   ├─ Delete a branch
│   └─ Edit branch information
│
├── 📊 statistic.py                 # Statistics
│   ├─ Import chart (Grouped Bar by Month)
│   └─ Export chart (4 columns per product)
│
├── 💾 Data.py                      # Shared data
│   ├─ warehouse_goods (18 products)
│   ├─ store_branches (7 branches)
│   ├─ distributions_log (distribution log)
│   ├─ load_data_collection()
│   └─ save_data_collection()
│
└── 📄 data_collection.json         # Data save file (auto-generated)
    └─ Permanent storage for all data
```

---

## 🔄 Workflow

```
                    🚀 START
                      │
                      ▼
            ┌─────────────────────┐
            │   python Main.py    │
            └─────────────────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │ 🔐 Authentication   │
            │   (3 attempts)      │
            └─────────────────────┘
                      │
                  ✅ Success
                      │
                      ▼
            ┌─────────────────────┐
            │  🏠 Main Menu       │
            │  (4 options)        │
            └─────────────────────┘
                      │
        ┌─────────────┼────────────┬────────────┐
        │             │            │            │
        ▼             ▼            ▼            ▼
    ┌────  ───┐  ┌───  ────┐  ┌────   ───┐   ┌───────┐
    │  📦     │  │    📊   │  │   🏪    │   │  💾   │
    │Warehouse│  │Statistic│  │Branches  │   │ Save  │
    └────  ───┘  └────  ───┘  └────   ───┘   └───────┘
        │             │           │            │
        │             │           │            │
        ▼             ▼           ▼            ▼
    ┌───────┐     ┌───────┐   ┌───────┐   ┌───────┐
    │  Save │   │View   │   │Chart1 │   │Supply │
    │ JSON  │   │Delete │   │Chart2 │   │View   │
    │       │   │Edit   │   │       │   │Dist.  │
    └───────┘     └───────┘   └───────┘   └───────┘
```

---

## 📊 Data

### **warehouse_goods (18 products)**
```python
{
  1: {
    "name": "Yemeni Arab Coffee",
    "amount": 50,
    "price": 45,
    "cost": 35,
    "arrival_date": "2025-01-15",
    "import_location": "Yemen",
    "unit": "kg"
  },
  # ... 17 other products
}
```

### **store_branches (7 branches)**
```python
{
  1: {
    "name": "Abdoun Branch",
    "location": "",
    "branch_manager_phone": "0765954227"
  },
  # ... 6 other branches
}
```

### **distributions_log (Distribution Log)**
```python
[
  {
    "branch": "City Sports Branch",
    "product_name": "Small Paper Cups",
    "product_id": 6,
    "quantity": 150.0,
    "delivery_date": "2026-01-26",
    "total_revenue": 12.0,
    "total_profit": 4.5,
    "timestamp": "2026-01-29 15:56:34"
  },
  # ... other records
]
```

---

## 🎨 Key Features

### **1. Login System 🔐**
- Protected user data
- 3 attempts before rejection
- Empty input validation

### **2. Warehouse Management 📦**
- **Supply Items:**
  - Increase existing quantities
  - Update dates
  - Update prices (optional)
  - Auto-save

- **Distribution to Branches:**
  - Select branch
  - Select product
  - Specify quantity
  - Automatic profit calculation
  - Immediate inventory update

### **3. Branch Management 🏪**
- View all branches
- Delete a branch (with confirmation)
- Edit any field in a branch

### **4. Statistics 📊**
- **Chart 1: Import**
  - Grouped Bar Chart
  - 18 products × multiple months
  - Distinct colors per product
  - Dynamic based on dates

- **Chart 2: Export**
  - 4 columns per product:
    - Base quantity (purple)
    - Imported quantity (pink)
    - Exported quantity (yellow)
    - Difference (blue)

### **5. Data Saving 💾**
- Auto-save after every operation
- Manual save from the menu
- Save on exit
- Easy-to-read JSON format

---

## 🛠️ Technologies Used

```python
# Language
Python 3.7+

# Libraries
matplotlib  # Charts and graphs
numpy       # Mathematical calculations
json        # Data saving
datetime    # Date management
```

---

## 📈 Statistics

### **Initial Data:**
```
📦 Products:      18 items
🏪 Branches:      7 branches
💰 Inventory value:  ~50,000 Dinar
📊 Distribution records: Dynamic
```

### **Operations:**
```
➕ Supply:      Increase quantities + Update data
➖ Distribute:  Transfer to branches + Calculate profits
📝 Edit:       Update branch information
📊 Statistics: Automatic charts
```

---

## 🔐 Security

### **Login:**
```
✅ Password protected
✅ Only 3 attempts
✅ Input validation
✅ Empty field prevention
```

### **Data:**
```
✅ Auto-save
✅ Secure JSON format
✅ Backups possible
✅ No data loss
```

---

## 🎯 Use Cases

### **1. Start of Day:**
```
1. Log in
2. View available goods
3. Check inventory
```

### **2. Receiving a Shipment:**
```
1. Select "Supply Items"
2. Select the product
3. Enter quantity and date
4. ✅ Immediate inventory update
```

### **3. Distributing to a Branch:**
```
1. Select "Distribution"
2. Select the branch and product
3. Specify the quantity
4. Review the summary
5. Confirm
6. ✅ Update + Save record
```

### **4. Performance Review:**
```
1. Select "Statistics"
2. View the import chart
3. View the export chart
4. ✅ Comprehensive performance insight
```

---

## 📊 Example of a Complete Scenario

```
📅 Date: 2026-01-30
👤 User: admin

1. Login ✅
   └─ Username: admin | Password: 1234

2. Supply Goods 📦
   └─ Product: Turkish Coffee (ID 2)
   └─ Quantity: 50 kg
   └─ Date: 2026-02-15
   └─ ✅ Inventory: 30 → 80 kg

3. Distribution 🚚
   └─ Branch: City Sports (ID 2)
   └─ Product: Small Cups (ID 6)
   └─ Quantity: 200 pieces
   └─ Delivery: 2026-02-05
   └─ Revenue: 16 Dinar
   └─ Profit: 6 Dinar
   └─ ✅ Inventory: 4650 → 4450 pieces

4. Review Statistics 📊
   └─ Import Chart: ✅ Display all months
   └─ Export Chart: ✅ Compare items

5. Save Data 💾
   └─ ✅ Saved in data_collection.json

6. Logout 🚪
   └─ ✅ Data saved
```

---

## 🔄 Future Updates (Suggestions)

```
🔮 Possible additions:
- [ ] Permission system (admin, employee, manager)
- [ ] PDF reports
- [ ] Low inventory notifications
- [ ] Database integration (MySQL/PostgreSQL)
- [ ] Web interface (Flask/Django)
- [ ] Mobile application
- [ ] Invoicing system
- [ ] Employee tracking
## 📞 Support
```
```
