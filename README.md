# 🛒 Store Management System (GUI Version)

A cross-platform **Store/Inventory Management System** built with **Python (Tkinter)** and **MySQL**.  
Designed to demonstrate core **CRUD operations**, **inventory management**, and **sales tracking** with a graphical user interface.

---

## ✅ Features

- ➕ Add, update, and view **Products**
- 👥 Manage **Customers** and **Sellers**
- 📦 Handle **Inventory** (stock levels, restocking)
- 💰 Process and track **Sales**
- 📈 View filtered **Sales Reports** by date range

---

## 🧰 Tech Stack

- **Frontend / GUI:** Python (Tkinter)
- **Backend:** MySQL
- **Libraries:** `mysql-connector-python`, `tkinter` (built-in with Python)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nikhilbandodkar/Storage-Management-System.git
cd Storage-Management-System
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
```sql
CREATE DATABASE store_management;
```

Edit `stormanag_2.py`:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Replace with your MySQL password
    database="store_management",
    port=3306
)
```

### 4. Run the App
```bash
python stormanag_2.py
```
