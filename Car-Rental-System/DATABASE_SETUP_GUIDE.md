# 🗄️ Car Rental System - MySQL Database Setup Guide

Complete guide to set up and configure MySQL database for your Car Rental System.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Setup (Automated)](#quick-setup-automated)
3. [Manual Setup](#manual-setup)
4. [Database Configuration](#database-configuration)
5. [Database Schema](#database-schema)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before setting up the database, ensure you have:

- **MySQL Server** installed (5.7+ or 8.0+)
  - Download: https://dev.mysql.com/downloads/mysql/
- **MySQL running** on your system
- **Python 3.8+** installed
- **Required Python packages**:
  ```bash
  pip install mysql-connector-python werkzeug Flask
  ```

---

## 🚀 Quick Setup (Automated)

### Option 1: Python Setup Script (Recommended)

Run the automated setup script:

```bash
python setup_mysql.py
```

This script will:
- ✅ Create the `car_rental_db` database
- ✅ Create all required tables (users, admin_accounts, cars, bookings)
- ✅ Insert default admin account
- ✅ Populate sample car data
- ✅ Verify the setup

**Default Admin Credentials:**
- **Email:** `admin@luxedrive.com`
- **Password:** `Admin@123`

---

### Option 2: Direct SQL Import

If you prefer to use SQL directly:

```bash
mysql -u root -p < database_schema.sql
```

Or using MySQL Workbench:
1. Open MySQL Workbench
2. File → Open SQL Script → Select `database_schema.sql`
3. Execute (⚡ icon or Ctrl+Shift+Enter)

---

## 🔧 Manual Setup

### Step 1: Create Database

```sql
CREATE DATABASE car_rental_db;
USE car_rental_db;
```

### Step 2: Create Tables

Run the SQL commands in `database_schema.sql` or use the Python script.

### Step 3: Create Admin Account

```python
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Admin@123'))"
```

Then insert into database:
```sql
INSERT INTO admin_accounts (fullname, email, phone, password) 
VALUES ('System Administrator', 'admin@luxedrive.com', '0891234567', '<hashed_password_here>');
```

---

## ⚙️ Database Configuration

### Configuration File: `db_config.py`

```python
def get_db_config():
    return {
        'host': 'localhost',      # Change if MySQL is on different server
        'user': 'root',            # Your MySQL username
        'password': '',            # Your MySQL password
        'database': 'car_rental_db',
        'use_pure': True
    }
```

### Update MySQL Credentials

If your MySQL has a password or different credentials:

1. Open `db_config.py`
2. Update the configuration:
   ```python
   'user': 'your_mysql_username',
   'password': 'your_mysql_password',
   ```
3. Also update `setup_mysql.py` if using the automated script

---

## 📊 Database Schema

### Tables Overview

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | Customer accounts | id, name, email, password, phone |
| `admin_accounts` | Admin/staff accounts | id, fullname, email, password |
| `cars` | Vehicle inventory | id, name, category, price, features |
| `bookings` | Rental reservations | id, user_email, car_id, dates, cost |

### Table Relationships

```
users (email) ──> bookings (user_email)
cars (id) ──> bookings (car_id) [FOREIGN KEY]
```

---

## 🔍 Database Schema Details

### 1. Users Table

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Stores customer account information

---

### 2. Admin Accounts Table

```sql
CREATE TABLE admin_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Stores administrator account information

---

### 3. Cars Table

```sql
CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,        -- luxury, sedan, suv, sports, exotic
    price DECIMAL(10, 2) NOT NULL,
    image TEXT,
    seats INT NOT NULL,
    transmission VARCHAR(20) NOT NULL,    -- automatic, manual
    features TEXT,                         -- JSON array of features
    color VARCHAR(50),
    status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Stores vehicle inventory

**Categories:**
- `luxury` - High-end luxury vehicles
- `sedan` - Standard sedans
- `suv` - SUVs and crossovers
- `sports` - Sports cars
- `exotic` - Exotic supercars

---

### 4. Bookings Table

```sql
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    car_id INT NOT NULL,
    car_name VARCHAR(100) NOT NULL,
    car_image TEXT,
    pickup_date DATE NOT NULL,
    return_date DATE NOT NULL,
    days INT NOT NULL,
    base_cost DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    total_cost DECIMAL(10, 2) NOT NULL,
    discounts_applied TEXT,
    status VARCHAR(20) DEFAULT 'confirmed',  -- confirmed, cancelled
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id)
);
```

**Purpose:** Stores rental bookings and reservations

---

## 🧪 Testing the Setup

### Verify Database

```sql
-- Check if database exists
SHOW DATABASES LIKE 'car_rental_db';

-- Use the database
USE car_rental_db;

-- Check all tables
SHOW TABLES;

-- Count records in each table
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'admin_accounts', COUNT(*) FROM admin_accounts
UNION ALL
SELECT 'cars', COUNT(*) FROM cars
UNION ALL
SELECT 'bookings', COUNT(*) FROM bookings;
```

### Test Admin Login

1. Start your Flask app:
   ```bash
   python app.py
   ```

2. Navigate to: `http://localhost:5000/admin/login`

3. Login with:
   - Email: `admin@luxedrive.com`
   - Password: `Admin@123`

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Can't connect to MySQL server**

**Error:** `mysql.connector.errors.DatabaseError: 2003`

**Solution:**
- Check if MySQL service is running
  ```bash
  # Windows
  net start MySQL80
  
  # Mac/Linux
  sudo systemctl start mysql
  ```
- Verify MySQL is listening on port 3306

---

#### 2. **Access denied for user 'root'**

**Error:** `mysql.connector.errors.ProgrammingError: 1045`

**Solution:**
- Update credentials in `db_config.py`
- Reset MySQL root password if forgotten:
  ```bash
  mysql -u root -p
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
  ```

---

#### 3. **Database 'car_rental_db' doesn't exist**

**Solution:**
- Run the setup script:
  ```bash
  python setup_mysql.py
  ```
- Or create manually:
  ```sql
  CREATE DATABASE car_rental_db;
  ```

---

#### 4. **Table doesn't exist**

**Error:** `Table 'car_rental_db.cars' doesn't exist`

**Solution:**
- Re-run database initialization:
  ```bash
  python setup_mysql.py
  ```
- Or manually run `database_schema.sql`

---

#### 5. **Foreign key constraint fails**

**Error:** `Cannot add or update a child row: a foreign key constraint fails`

**Solution:**
- Ensure cars table has the car_id before creating booking
- Check referential integrity

---

## 📝 Useful MySQL Commands

```sql
-- View all cars
SELECT * FROM cars;

-- View available cars only
SELECT * FROM cars WHERE status = 'available';

-- View all bookings
SELECT * FROM bookings ORDER BY booking_date DESC;

-- View active bookings
SELECT * FROM bookings WHERE status = 'confirmed';

-- View cars by category with count
SELECT category, COUNT(*) as count, AVG(price) as avg_price 
FROM cars 
GROUP BY category;

-- View all admins
SELECT id, fullname, email, phone FROM admin_accounts;

-- View customer accounts
SELECT id, name, email, phone FROM users;

-- Delete all bookings (use carefully!)
DELETE FROM bookings;

-- Reset car status to available
UPDATE cars SET status = 'available';
```

---

## 🔄 Database Maintenance

### Backup Database

```bash
# Full backup
mysqldump -u root -p car_rental_db > backup_$(date +%Y%m%d).sql

# Backup specific tables
mysqldump -u root -p car_rental_db cars bookings > cars_bookings_backup.sql
```

### Restore Database

```bash
mysql -u root -p car_rental_db < backup_20231104.sql
```

### Reset Database

```sql
DROP DATABASE car_rental_db;
CREATE DATABASE car_rental_db;
```

Then re-run setup script:
```bash
python setup_mysql.py
```

---

## 🚀 Production Deployment

For production environments:

1. **Change default credentials**
   - Update admin password
   - Use strong MySQL passwords

2. **Enable SSL/TLS**
   ```python
   'ssl_ca': '/path/to/ca.pem',
   'ssl_verify_cert': True
   ```

3. **Set up proper user permissions**
   ```sql
   CREATE USER 'car_rental_user'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON car_rental_db.* TO 'car_rental_user'@'localhost';
   ```

4. **Regular backups**
   - Set up automated daily backups
   - Store backups offsite

5. **Monitor database performance**
   - Add indexes for frequently queried columns
   - Optimize queries

---

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Verify MySQL is running
3. Check database credentials
4. Review error logs in the console
5. Ensure all required packages are installed

---

## 📄 Files Reference

- `setup_mysql.py` - Automated Python setup script
- `database_schema.sql` - Complete SQL schema
- `db_config.py` - Database configuration
- `app.py` - Main Flask application
- `init_mysql_database.py` - Alternative setup script

---

**Last Updated:** November 2025  
**Version:** 1.0
