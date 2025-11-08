# 🚀 Complete Setup Guide - Car Rental System

## Step 1: Install MySQL

### Windows:
1. Download MySQL Installer from [mysql.com](https://dev.mysql.com/downloads/installer/)
2. Run the installer and select "MySQL Server"
3. Choose "Development Default" setup type
4. Set **NO PASSWORD** for root user (or leave it blank during setup)
5. Complete the installation

### Verify MySQL Installation:
```bash
# Check if MySQL is running
net start | findstr MySQL

# If not running, start it
net start MySQL80
```

## Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask
- mysql-connector-python
- werkzeug
- authlib

## Step 3: Configure Database Connection

The database configuration is in `db_config.py`:

```python
def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Empty password (default)
        'database': 'car_rental_db',
        'use_pure': True
    }
```

**If your MySQL has a password:**
Change line 11 in `db_config.py`:
```python
'password': 'your_mysql_password',  # Add your MySQL root password here
```

## Step 4: Initialize the Database

When you run the Flask application for the first time, it will automatically:
1. Create the database `car_rental_db`
2. Create all required tables
3. Create a default admin account

```bash
python app.py
```

You should see output like:
```
============================================================
✅ DEFAULT ADMIN ACCOUNT CREATED SUCCESSFULLY!
============================================================
   📧 Email: admin@luxedrive.com
   👤 Full Name: LuxeDrive Admin
   📱 Phone: 1234567890
   🔑 Password: AdminLuxe2024!
============================================================
⚠️  SAVE THESE CREDENTIALS - You'll need them to login!
============================================================

Database tables created successfully!
 * Running on http://127.0.0.1:5000
```

## Step 5: Access the Application

### Customer Portal:
- URL: `http://localhost:5000/`
- Features: Browse cars, make bookings, view booking history

### Admin Portal:
- URL: `http://localhost:5000/admin/login`
- Email: `admin@luxedrive.com`
- Password: `AdminLuxe2024!`

## Step 6: Verify Everything Works

### Test Database Connection:
```bash
python check_admin.py
```

This will show you all admin accounts in the database.

### Add Sample Cars (Optional):
```bash
python add_sample_comprehensive_cars.py
```

This adds sample cars to your inventory.

## Common Issues & Solutions

### Issue 1: "Can't connect to MySQL server"
**Solution:**
1. Make sure MySQL service is running:
   ```bash
   net start MySQL80
   ```
2. Check MySQL is installed correctly
3. Verify port 3306 is not blocked

### Issue 2: "Access denied for user 'root'"
**Solution:**
1. Check your MySQL password in `db_config.py`
2. If you set a password during MySQL installation, update line 11:
   ```python
   'password': 'your_mysql_password',
   ```

### Issue 3: "Database doesn't exist"
**Solution:**
The database is created automatically on first run. Just run:
```bash
python app.py
```

### Issue 4: "Admin login not working"
**Solution:**
1. Check admin credentials in `ADMIN_CREDENTIALS.md`
2. Email: `admin@luxedrive.com`
3. Password: `AdminLuxe2024!`
4. Make sure you're accessing: `http://localhost:5000/admin/login`

## Database Structure

The system creates 4 main tables:

1. **admin_accounts** - Admin user credentials
   - id, fullname, email, phone, password, created_at

2. **users** - Customer accounts
   - id, name, email, password, phone, created_at

3. **cars** - Vehicle inventory
   - id, name, brand, model, year, category, price, image, seats, transmission, features, etc.

4. **bookings** - Rental bookings
   - id, user_email, car_id, pickup_date, return_date, total_cost, status, etc.

## Changing Admin Password

Edit `db_config.py` line 137:
```python
YOUR_CUSTOM_PASSWORD = 'AdminLuxe2024!'  # Change to your desired password
```

Then:
1. Delete existing admin account from database:
   ```sql
   DELETE FROM admin_accounts WHERE email = 'admin@luxedrive.com';
   ```
2. Restart the application to recreate with new password

## Production Deployment Checklist

Before deploying to production:

- [ ] Change admin password to a strong, unique password
- [ ] Update Flask secret key in `app.py` line 13
- [ ] Set up proper MySQL user (don't use root)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper backup for database
- [ ] Configure environment variables
- [ ] Update CORS settings if needed
- [ ] Set up proper logging
- [ ] Configure Google OAuth credentials

## Support

If you encounter any issues:
1. Check `ADMIN_CREDENTIALS.md` for login info
2. Review MySQL connection in `db_config.py`
3. Verify MySQL service is running
4. Check Python dependencies are installed

---

**Happy Coding! 🚗💨**
