"""
Quick Database Setup Script
This script automates the database setup process
"""

import mysql.connector
from mysql.connector import Error
import sys

def print_header():
    print("="*60)
    print("🗄️  LuxeDrive - Database Setup Wizard")
    print("="*60)
    print()

def get_user_input():
    """Get database credentials from user"""
    print("📝 Please enter your MySQL credentials:")
    print("   (Press Enter to use default values)")
    print()
    
    host = input("MySQL Host [localhost]: ").strip() or 'localhost'
    user = input("MySQL Username [root]: ").strip() or 'root'
    password = input("MySQL Password [empty]: ").strip() or ''
    
    return {
        'host': host,
        'user': user,
        'password': password
    }

def test_connection(config):
    """Test MySQL connection"""
    print("\n🔌 Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            connection.close()
            return True
    except Error as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure MySQL is running")
        print("   2. Check your username and password")
        print("   3. For XAMPP, password is usually empty")
        return False

def create_database(config):
    """Create the car_rental database"""
    print("\n📦 Creating database 'car_rental'...")
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS car_rental")
        print("✅ Database 'car_rental' created successfully!")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_config_file(config):
    """Update db_config.py with user credentials"""
    print("\n📝 Updating db_config.py...")
    try:
        with open('db_config.py', 'r') as f:
            content = f.read()
        
        # Replace values
        content = content.replace("'host': 'localhost'", f"'host': '{config['host']}'")
        content = content.replace("'user': 'root'", f"'user': '{config['user']}'")
        content = content.replace("'password': 'your_password'", f"'password': '{config['password']}'")
        
        with open('db_config.py', 'w') as f:
            f.write(content)
        
        print("✅ db_config.py updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        return False

def create_tables(config):
    """Create all database tables"""
    print("\n🏗️  Creating database tables...")
    try:
        full_config = {**config, 'database': 'car_rental'}
        connection = mysql.connector.connect(**full_config)
        cursor = connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✓ Users table created")
        
        # Admin accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✓ Admin accounts table created")
        
        # Cars table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                image TEXT,
                seats INT NOT NULL,
                transmission VARCHAR(50) NOT NULL,
                color VARCHAR(50),
                features TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("  ✓ Cars table created")
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(255) NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                car_id INT NOT NULL,
                car_name VARCHAR(255) NOT NULL,
                car_image TEXT,
                pickup_date DATE NOT NULL,
                return_date DATE NOT NULL,
                days INT NOT NULL,
                total_cost DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'confirmed',
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
            )
        """)
        print("  ✓ Bookings table created")
        
        # Insert default admin
        cursor.execute("""
            INSERT IGNORE INTO admin_accounts (username, name, email, password)
            VALUES ('admin', 'Administrator', 'admin@luxedrive.com', '0707200717')
        """)
        print("  ✓ Default admin account created")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ All tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    print_header()
    
    # Get credentials
    config = get_user_input()
    
    # Test connection
    if not test_connection(config):
        print("\n❌ Setup failed. Please fix the connection issues and try again.")
        sys.exit(1)
    
    # Create database
    if not create_database(config):
        print("\n❌ Setup failed. Could not create database.")
        sys.exit(1)
    
    # Update config file
    if not update_config_file(config):
        print("\n⚠️  Warning: Could not update db_config.py automatically.")
        print("   Please update it manually with your credentials.")
    
    # Create tables
    if not create_tables(config):
        print("\n❌ Setup failed. Could not create tables.")
        sys.exit(1)
    
    # Success!
    print("\n" + "="*60)
    print("🎉 Database Setup Complete!")
    print("="*60)
    print("\n📊 Summary:")
    print(f"   • Database: car_rental")
    print(f"   • Tables: users, admin_accounts, cars, bookings")
    print(f"   • Default Admin: admin / 0707200717")
    print("\n🚀 Next Steps:")
    print("   1. Run: python app.py")
    print("   2. Visit: http://localhost:5000")
    print("   3. Login as admin to add cars")
    print("\n💡 Note: The app will now use MySQL database instead of")
    print("   in-memory storage. All data will persist!")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
