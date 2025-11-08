# 🔐 Admin Login Credentials

## Default Admin Account

The system automatically creates a default admin account when the database is initialized for the first time.

### Login Credentials:

```
📧 Email: admin@luxedrive.com
🔑 Password: AdminLuxe2024!
👤 Full Name: LuxeDrive Admin
📱 Phone: 1234567890
```

## How to Login

1. **Navigate to Admin Login Page:**
   - URL: `http://localhost:5000/admin/login`
   
2. **Enter Credentials:**
   - Email: `admin@luxedrive.com`
   - Password: `AdminLuxe2024!`

3. **Access Admin Dashboard:**
   - After successful login, you'll be redirected to the admin dashboard
   - URL: `http://localhost:5000/admin/dashboard`

## Features Available in Admin Dashboard

- ✅ View all cars in the rental system
- ✅ Add new cars to inventory
- ✅ Edit existing car details
- ✅ Delete cars from inventory
- ✅ View all bookings
- ✅ Manage booking status
- ✅ View statistics (total cars, bookings, etc.)

## Changing the Admin Password

If you want to change the default password, edit the file:
`db_config.py` at line 137

```python
YOUR_CUSTOM_PASSWORD = 'AdminLuxe2024!'  # 👈 Change this to your desired password
```

**Important Notes:**
- The password is securely hashed using Werkzeug's password hashing
- Passwords are never stored in plain text in the database
- After changing the password, restart your application and reinitialize the database if needed

## MySQL Database Connection

The admin system is connected to MySQL database with the following configuration:

```python
Database Name: car_rental_db
Host: localhost
User: root
Password: (empty by default)
```

### Tables Created:
1. **admin_accounts** - Stores admin user credentials
2. **users** - Stores customer accounts
3. **cars** - Stores car inventory
4. **bookings** - Stores rental bookings

## Security Features

✅ **Password Hashing:** All passwords are hashed using `werkzeug.security.generate_password_hash()`  
✅ **Session Management:** Admin sessions are managed securely  
✅ **Authentication Required:** All admin routes require login  
✅ **Protected Routes:** Unauthorized access is prevented

## Troubleshooting

### Can't Login?
1. Make sure MySQL service is running
2. Check that the database is initialized (`car_rental_db` exists)
3. Verify admin account exists in `admin_accounts` table
4. Ensure you're using the correct email and password

### MySQL Connection Error?
1. Start MySQL service: 
   - Windows: Open Services and start "MySQL80" (or your version)
   - Command: `net start MySQL80`
2. Check MySQL is running on port 3306
3. Verify root user has no password (or update `db_config.py` with your password)

### Need to Reset Admin Account?
Run this SQL command in MySQL:
```sql
DELETE FROM admin_accounts WHERE email = 'admin@luxedrive.com';
```
Then restart your Flask application to recreate the default admin account.

## Creating Additional Admin Accounts

You can create additional admin accounts through the admin dashboard or by using the API endpoint:

**Endpoint:** `POST /admin/create`  
**Required Fields:**
- fullname
- email
- phone
- password

---

**🚨 IMPORTANT:** Keep these credentials secure and change the default password for production use!
