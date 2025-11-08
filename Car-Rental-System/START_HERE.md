# 🚀 QUICK START - Car Rental System

## 🔐 Admin Login Credentials

```
📧 Email: admin@luxedrive.com
🔑 Password: AdminLuxe2024!
🌐 Admin URL: http://localhost:5000/admin/login
```

## ⚡ Quick Setup (3 Steps)

### Step 1: Install MySQL
Make sure MySQL is installed and running on your computer.

**Check if MySQL is running:**
```bash
net start | findstr MySQL
```

**Start MySQL if not running:**
```bash
net start MySQL80
```

### Step 2: Install Python Packages
```bash
pip install flask mysql-connector-python werkzeug authlib
```

### Step 3: Run the Application
```bash
python app.py
```

The application will:
✅ Automatically create the database  
✅ Create all required tables  
✅ Set up the admin account  
✅ Start the web server  

## 🌐 Access the Application

### Customer Portal
- **URL:** http://localhost:5000/
- Browse cars, make bookings, create account

### Admin Portal
- **URL:** http://localhost:5000/admin/login
- **Email:** admin@luxedrive.com
- **Password:** AdminLuxe2024!

## 🧪 Test Database Connection

To verify everything is set up correctly:
```bash
python test_db_connection.py
```

This will show you:
- MySQL connection status
- Database and tables info
- Admin account details
- Password verification

## 📝 Important Files

- **db_config.py** - Database connection settings and admin password
- **app.py** - Main Flask application
- **ADMIN_CREDENTIALS.md** - Complete admin login documentation
- **SETUP_GUIDE.md** - Detailed setup instructions

## 🔧 Troubleshooting

### Can't connect to MySQL?
```bash
# Start MySQL service
net start MySQL80

# Or check if it's running
net start | findstr MySQL
```

### Wrong MySQL password?
Edit `db_config.py` line 11:
```python
'password': 'your_mysql_password',  # Add your password here
```

### Admin login not working?
Make sure you're using:
- Email: `admin@luxedrive.com`
- Password: `AdminLuxe2024!`
- URL: `http://localhost:5000/admin/login` (not `/login`)

## 🎯 Next Steps

1. ✅ Login to admin portal
2. ✅ Add cars to inventory
3. ✅ Customize the admin password (edit db_config.py line 137)
4. ✅ Test customer booking flow

## 📚 More Help

- **SETUP_GUIDE.md** - Complete setup instructions
- **ADMIN_CREDENTIALS.md** - Admin features and security info
- **DATABASE_SETUP_GUIDE.md** - Database configuration details

---

**Need Help?** Check the troubleshooting section or review the setup guide!

**Ready to Go?** Run `python app.py` and visit http://localhost:5000/admin/login 🚗💨
