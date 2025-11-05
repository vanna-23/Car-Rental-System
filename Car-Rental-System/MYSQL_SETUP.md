# 🔧 MySQL Easy Setup Guide

## ✅ Quick MySQL Setup (3 Minutes)

### Step 1: Set MySQL Root Password to `1234`

**Option A: Using MySQL Command Line**
```bash
# Login to MySQL (might ask for current password, press Enter if none)
mysql -u root -p

# Inside MySQL, run:
ALTER USER 'root'@'localhost' IDENTIFIED BY '1234';
FLUSH PRIVILEGES;
EXIT;
```

**Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Connect to Local instance
3. Go to `Server` → `Users and Privileges`
4. Select `root` user
5. Click `Change Password`
6. Set new password: `1234`
7. Click `Apply`

---

### Step 2: Run the Application

```bash
# Make sure you're in the virtual environment
cd c:\Users\VANNA.LEN\Desktop\Car-Rental-System-one

# Activate virtual environment
.venv\Scripts\activate

# Navigate to project folder
cd Car-Rental-System

# Run the app
python app.py
```

---

## 🎯 MySQL Configuration Details

**Current Settings:**
- **Host:** localhost
- **User:** root
- **Password:** `1234` 👈 Easy to remember!
- **Database:** car_rental_db (created automatically)

**Location in Code:** `db_config.py` (lines 11 and 33)

---

## 🚀 What Happens on First Run?

The app will automatically:
1. ✅ Connect to MySQL
2. ✅ Create database `car_rental_db`
3. ✅ Create all required tables (users, cars, bookings, admin_accounts)
4. ✅ Insert default admin account
5. ✅ Ready to use!

---

## 📝 Default Admin Account

After first run, you can login with:
- **URL:** http://localhost:5000/admin/login
- **Email:** admin@luxedrive.com
- **Password:** 0707200717

---

## ⚠️ Troubleshooting

**Error: "Can't connect to MySQL server"**
- Make sure MySQL service is running
- Check Windows Services for "MySQL" or "MySQL80"
- Verify password is set to `1234`

**Error: "Access denied for user 'root'@'localhost'"**
- Your MySQL password is different
- Change password in `db_config.py` (line 11 and 33) to match your actual password

---

## 🎨 Visual Summary

```
┌─────────────────────────────────────┐
│  Car Rental System                  │
│  ↓                                   │
│  Flask App (app.py)                 │
│  ↓                                   │
│  Database Config (db_config.py)     │
│  ↓                                   │
│  MySQL Server                       │
│  • User: root                       │
│  • Password: 1234 ← EASY!           │
│  • Database: car_rental_db          │
└─────────────────────────────────────┘
```

---

## ✨ Benefits of MySQL Connection

- ✅ Data persists after restart
- ✅ Better performance
- ✅ Real database features
- ✅ Can view data in MySQL Workbench
- ✅ Production-ready

**Enjoy your Car Rental System! 🚗💨**
