# MySQL Setup Instructions

## Prerequisites
1. Install MySQL Server on your machine
2. Make sure MySQL service is running

## Step 1: Configure Database Connection

Edit `db_config.py` and update the following values:

```python
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL server host
    'user': 'root',           # Your MySQL username
    'password': 'your_password',  # Your MySQL password (CHANGE THIS!)
    'database': 'car_rental'  # Your database name
}
```

## Step 2: Create Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE car_rental;
```

## Step 3: Initialize Tables

Run the database initialization script:

```bash
python db_config.py
```

This will create the required tables:
- `users` - Store user accounts
- `bookings` - Store car rental bookings

## Step 4: Update Your Application

You have two options:

### Option A: Replace app.py (Recommended)
1. Backup your current `app.py`
2. Replace it with `app_mysql_example.py`:
   ```bash
   copy app.py app_backup.py
   copy app_mysql_example.py app.py
   ```

### Option B: Manual Integration
Copy the MySQL functions from `app_mysql_example.py` and integrate them into your existing `app.py`:
- `create_user()`
- `get_user_by_email()`
- `create_booking_db()`
- `get_user_bookings()`
- `update_booking_status()`

Then update your routes to use these functions instead of in-memory storage.

## Step 5: Test the Connection

Create a test file `test_connection.py`:

```python
from db_config import get_db_connection

connection = get_db_connection()
if connection and connection.is_connected():
    print("✓ Successfully connected to MySQL!")
    connection.close()
else:
    print("✗ Failed to connect to MySQL")
```

Run it:
```bash
python test_connection.py
```

## Common Issues

### Issue: "Access denied for user"
- Check your MySQL username and password in `db_config.py`
- Ensure your MySQL user has proper permissions

### Issue: "Unknown database"
- Make sure you created the database: `CREATE DATABASE car_rental;`

### Issue: "Can't connect to MySQL server"
- Ensure MySQL service is running
- Check if MySQL is listening on port 3306
- Verify firewall settings

## Security Best Practices

1. **Never commit passwords to version control**
   - Use environment variables for sensitive data
   - Add `db_config.py` to `.gitignore`

2. **Hash passwords before storing**
   - Use libraries like `bcrypt` or `werkzeug.security`
   - Never store plain text passwords

3. **Use prepared statements**
   - The example already uses parameterized queries to prevent SQL injection

## Next Steps

1. Add password hashing (use `werkzeug.security.generate_password_hash`)
2. Add environment variables for database credentials
3. Implement connection pooling for better performance
4. Add proper error logging
5. Create database indexes for better query performance
