# 🔐 MySQL Password Configuration Guide

## Current Configuration

The application is currently configured to connect to MySQL with **NO PASSWORD** (empty password).

```python
# In db_config.py
def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # ← Empty password (default)
        'database': 'car_rental_db',
        'use_pure': True
    }
```

## If Your MySQL Has a Password

If you set a password for the MySQL root user during installation, you need to update the configuration:

### Option 1: Update db_config.py (Recommended)

Edit `db_config.py` and change line 11:

**Before:**
```python
'password': '',  # Empty password
```

**After:**
```python
'password': 'your_actual_mysql_password',  # Your MySQL password
```

You also need to update line 33 in the same file:

**Before:**
```python
password='',  # Empty password
```

**After:**
```python
password='your_actual_mysql_password',  # Your MySQL password
```

### Option 2: Use Environment Variables (Production)

For better security in production, use environment variables:

1. Create a `.env` file:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=car_rental_db
```

2. Update `db_config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'car_rental_db'),
        'use_pure': True
    }
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

## How to Check/Reset MySQL Root Password

### Check Current Password Status

Try connecting to MySQL:
```bash
mysql -u root -p
```

- If it asks for password and you enter it successfully → You have a password set
- If it connects without asking for password → No password is set

### Reset MySQL Root Password (Windows)

If you forgot your MySQL password:

1. Stop MySQL service:
```bash
net stop MySQL80
```

2. Create a text file `reset.txt` with:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '';
```

3. Start MySQL with skip-grant-tables:
```bash
mysqld --init-file=C:\path\to\reset.txt
```

4. Restart MySQL normally:
```bash
net start MySQL80
```

### Set a New MySQL Password

Connect to MySQL and run:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

Then update `db_config.py` with the new password.

## Testing Your Configuration

After updating the password configuration, test it:

```bash
python test_db_connection.py
```

This will verify:
- MySQL connection works
- Database is accessible
- Admin account is set up correctly

## Common MySQL Password Scenarios

### Scenario 1: Fresh MySQL Install (No Password)
- **Configuration:** Keep `password: ''` in db_config.py
- **No changes needed!**

### Scenario 2: MySQL with Password Set
- **Configuration:** Update `password: 'your_password'` in db_config.py
- **Update both lines 11 and 33**

### Scenario 3: Using XAMPP/WAMP
- **Default:** Usually no password for root
- **Configuration:** Keep `password: ''` in db_config.py

### Scenario 4: Production Server
- **Configuration:** Use environment variables
- **Never hardcode passwords in production!**

## Security Best Practices

1. ✅ **Development:** It's OK to use empty password locally
2. ✅ **Production:** Always use strong passwords
3. ✅ **Production:** Use environment variables (.env file)
4. ✅ **Production:** Create a dedicated MySQL user (don't use root)
5. ✅ **Production:** Never commit passwords to version control

## Creating a Dedicated MySQL User (Production)

Instead of using root, create a dedicated user:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create new user
CREATE USER 'car_rental_user'@'localhost' IDENTIFIED BY 'strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON car_rental_db.* TO 'car_rental_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

Then update `db_config.py`:
```python
def get_db_config():
    return {
        'host': 'localhost',
        'user': 'car_rental_user',  # Changed from 'root'
        'password': 'strong_password_here',
        'database': 'car_rental_db',
        'use_pure': True
    }
```

## Summary

| Scenario | Password Value | Action Needed |
|----------|---------------|---------------|
| Fresh MySQL install | Empty (`''`) | ✅ No changes |
| MySQL with password | Your password | Update db_config.py lines 11 & 33 |
| XAMPP/WAMP | Usually empty (`''`) | ✅ No changes |
| Production | Strong password | Use environment variables |

---

**🎯 Quick Test:** Run `python test_db_connection.py` to verify your configuration!
