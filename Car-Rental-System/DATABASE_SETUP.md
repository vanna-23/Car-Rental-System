# 🗄️ Database Setup Guide - LuxeDrive

## 📋 Prerequisites

Before connecting to a database, you need:
1. **MySQL Server** installed on your computer
2. **Python MySQL Connector** installed
3. Database credentials (username, password)

---

## 🚀 Step-by-Step Setup

### **Step 1: Install MySQL Server**

#### **Option A: XAMPP (Recommended for Windows)**
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Open XAMPP Control Panel
4. Click "Start" next to **MySQL**
5. Default credentials:
   - Host: `localhost`
   - User: `root`
   - Password: `` (empty) or `root`
   - Port: `3306`

#### **Option B: MySQL Standalone**
1. Download MySQL from: https://dev.mysql.com/downloads/
2. Install MySQL Community Server
3. Remember the root password you set during installation

---

### **Step 2: Install Python MySQL Connector**

Open terminal and run:
```bash
pip install mysql-connector-python
```

---

### **Step 3: Configure Database Connection**

1. Open `db_config.py`
2. Update the database credentials:

```python
DB_CONFIG = {
    'host': 'localhost',           # Your MySQL server host
    'user': 'root',                # Your MySQL username  
    'password': 'your_password',   # Your MySQL password (or leave empty '')
    'database': 'car_rental'       # Database name
}
```

**For XAMPP users:**
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Usually empty for XAMPP
    'database': 'car_rental'
}
```

---

### **Step 4: Create the Database**

#### **Method 1: Using phpMyAdmin (XAMPP)**
1. Open browser: http://localhost/phpmyadmin
2. Click "New" in left sidebar
3. Database name: `car_rental`
4. Collation: `utf8mb4_general_ci`
5. Click "Create"

#### **Method 2: Using MySQL Command Line**
```bash
mysql -u root -p
```
Enter password, then run:
```sql
CREATE DATABASE car_rental;
EXIT;
```

---

### **Step 5: Initialize Database Tables**

Run the initialization script:
```bash
cd "c:\Users\VANNA.LEN\Desktop\car-good - Copy\car-good"
python db_config.py
```

**Expected Output:**
```
✅ Database tables created successfully!
✅ Default admin account created: admin / 0707200717
```

This creates:
- ✅ `users` table - Customer accounts
- ✅ `admin_accounts` table - Admin accounts
- ✅ `cars` table - Vehicle inventory
- ✅ `bookings` table - Rental bookings

---

### **Step 6: Populate Cars Data** (Optional)

To load sample cars into the database:
```bash
python populate_cars.py
```

---

### **Step 7: Update app.py to Use Database**

You have two options:

#### **Option A: Use app_with_database.py** (if created)
```bash
python app_with_database.py
```

#### **Option B: Manually integrate database**
I'll create a database-integrated version for you...

---

## 📊 Database Schema

### **users Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| name | VARCHAR(255) | User's full name |
| email | VARCHAR(255) | Email (unique) |
| password | VARCHAR(255) | Password |
| created_at | TIMESTAMP | Account creation date |

### **admin_accounts Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| username | VARCHAR(255) | Username (unique) |
| name | VARCHAR(255) | Admin's full name |
| email | VARCHAR(255) | Email (unique) |
| password | VARCHAR(255) | Password |
| created_at | TIMESTAMP | Account creation date |

### **cars Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| name | VARCHAR(255) | Car name |
| category | VARCHAR(100) | Category (Electric, SUV, etc.) |
| price | DECIMAL(10,2) | Daily rental price |
| image | TEXT | Image URL |
| seats | INT | Number of seats |
| transmission | VARCHAR(50) | Transmission type |
| color | VARCHAR(50) | Car color |
| features | TEXT | JSON array of features |
| created_at | TIMESTAMP | Date added |

### **bookings Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| user_email | VARCHAR(255) | Customer email |
| user_name | VARCHAR(255) | Customer name |
| car_id | INT | Car ID |
| car_name | VARCHAR(255) | Car name |
| car_image | TEXT | Car image URL |
| pickup_date | DATE | Rental start date |
| return_date | DATE | Rental end date |
| days | INT | Number of days |
| total_cost | DECIMAL(10,2) | Total cost |
| status | VARCHAR(50) | Booking status |
| booking_date | TIMESTAMP | Booking creation date |

---

## 🔧 Troubleshooting

### **Error: "Access denied for user"**
**Solution:** Check your username and password in `db_config.py`

### **Error: "Unknown database 'car_rental'"**
**Solution:** Create the database first (Step 4)

### **Error: "No module named 'mysql'"**
**Solution:** Install connector:
```bash
pip install mysql-connector-python
```

### **Error: "Can't connect to MySQL server"**
**Solution:** 
- Make sure MySQL is running (check XAMPP or Services)
- Verify host is 'localhost'
- Check port is 3306

### **XAMPP MySQL won't start**
**Solution:**
- Port 3306 might be in use
- Change port in XAMPP config
- Or stop other MySQL services

---

## ✅ Verification

To verify everything is set up correctly:

1. **Check MySQL is running:**
   - XAMPP: Green "Running" next to MySQL
   - Services: MySQL service is started

2. **Check database exists:**
```bash
mysql -u root -p
SHOW DATABASES;
```
Should list `car_rental`

3. **Check tables exist:**
```sql
USE car_rental;
SHOW TABLES;
```
Should show: users, admin_accounts, cars, bookings

4. **Check default admin:**
```sql
SELECT * FROM admin_accounts;
```
Should show admin account

---

## 🎯 Default Credentials

**Database:**
- Host: localhost
- User: root
- Password: (your MySQL password)
- Database: car_rental

**Admin Panel:**
- Username: admin
- Password: 0707200717

---

## 📝 Next Steps

1. ✅ Install MySQL
2. ✅ Install mysql-connector-python
3. ✅ Configure `db_config.py`
4. ✅ Create database
5. ✅ Run `python db_config.py`
6. ✅ (Optional) Run `python populate_cars.py`
7. ✅ Use database-connected version of app

---

## 🔄 Migration from In-Memory to Database

**Current (In-Memory):**
- Data stored in Python dictionaries
- Data lost on server restart
- No persistence

**After Database:**
- Data stored in MySQL
- Permanent storage
- Data persists across restarts
- Multiple users can access
- Scalable and production-ready

---

## 💡 Benefits of Database

✅ **Persistence** - Data saved permanently  
✅ **Reliability** - No data loss on restart  
✅ **Scalability** - Handle thousands of records  
✅ **Concurrent Access** - Multiple users simultaneously  
✅ **Data Integrity** - Foreign keys and constraints  
✅ **Backup** - Easy to backup/restore  
✅ **Production Ready** - Professional solution  

---

**Need help? Check the troubleshooting section or contact support!**
