# ⚡ Quick Database Setup - 5 Minutes!

## 🎯 Super Simple Setup

### **Option 1: Automatic Setup (Recommended)**

Just run this one command:
```bash
python setup_database.py
```

Then follow the prompts:
- MySQL Host: `localhost` (press Enter)
- MySQL Username: `root` (press Enter)
- MySQL Password: Enter your password (or leave empty for XAMPP)

**That's it!** The script will:
- ✅ Test your MySQL connection
- ✅ Create 'car_rental' database
- ✅ Create all tables
- ✅ Add default admin account
- ✅ Update configuration files

---

### **Option 2: Manual Setup**

#### **Step 1: Install MySQL Connector**
```bash
pip install mysql-connector-python
```

#### **Step 2: Edit db_config.py**
Open `db_config.py` and change:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Your MySQL username
    'password': '',              # Your MySQL password (empty for XAMPP)
    'database': 'car_rental'
}
```

#### **Step 3: Create Database**
Open MySQL/phpMyAdmin and run:
```sql
CREATE DATABASE car_rental;
```

#### **Step 4: Create Tables**
```bash
python db_config.py
```

---

## 🚀 After Setup

Your app is now database-connected! Run:
```bash
python app.py
```

Then visit: http://localhost:5000

---

## ✅ What Changed?

### **Before (In-Memory):**
- Data in Python dictionaries
- Lost on restart ❌
- Not production-ready ❌

### **After (Database):**
- Data in MySQL ✅
- Persists forever ✅
- Production-ready ✅

---

## 📊 Database Info

**Connection:**
- Host: localhost
- Database: car_rental
- Tables: 4

**Default Admin:**
- Username: admin
- Password: 0707200717

---

## 🔧 Troubleshooting

### "No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### "Access denied"
- Check your MySQL password in `db_config.py`
- For XAMPP, password is usually empty: `''`

### "MySQL not running"
- Start XAMPP and click "Start" next to MySQL
- Or start MySQL service in Windows Services

### "Database doesn't exist"
```sql
CREATE DATABASE car_rental;
```

---

## 💡 Quick Tips

1. **Using XAMPP?**
   - Password is usually empty: `password: ''`
   - Access phpMyAdmin: http://localhost/phpmyadmin

2. **Want to see your data?**
   - Open phpMyAdmin
   - Select 'car_rental' database
   - Click on any table

3. **Need to reset?**
   - Drop database: `DROP DATABASE car_rental;`
   - Run setup again: `python setup_database.py`

---

## 🎉 You're Done!

Database is connected and ready to use!

**Test it:**
1. Run the app: `python app.py`
2. Sign up as customer
3. Restart the server
4. Login again - your account still exists! ✅

This proves data is persisted in the database!
