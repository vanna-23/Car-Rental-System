import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash


def get_db_config():
    """Return base database configuration"""
    return {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # 👈 Empty password (try this if no password set)
        'database': 'car_rental_db',
        'use_pure': True
    }


def get_db_connection():
    """Create and return a new database connection"""
    config = get_db_config()
    try:
        return mysql.connector.connect(**config)
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables"""
    conn = None
    try:
        raw_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # 👈 Empty password (try this if no password set)
            use_pure=True
        )
        cursor = raw_conn.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS car_rental_db")
        cursor.close()
        raw_conn.close()

        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create admin_accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
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
                status VARCHAR(20) DEFAULT 'confirmed',
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create cars table with comprehensive fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                brand VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                image TEXT,
                seats INT NOT NULL,
                transmission VARCHAR(20) NOT NULL,
                fuel_type VARCHAR(30) DEFAULT 'Gasoline',
                engine VARCHAR(50),
                horsepower INT,
                mileage INT DEFAULT 0,
                license_plate VARCHAR(20),
                vin VARCHAR(50),
                location VARCHAR(100) DEFAULT 'Main Branch',
                features TEXT,
                color VARCHAR(50),
                doors INT DEFAULT 4,
                luggage_capacity INT DEFAULT 2,
                air_conditioning BOOLEAN DEFAULT TRUE,
                gps BOOLEAN DEFAULT FALSE,
                bluetooth BOOLEAN DEFAULT TRUE,
                backup_camera BOOLEAN DEFAULT FALSE,
                status VARCHAR(20) DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        
        # Create default admin account if none exists
        cursor.execute("SELECT COUNT(*) FROM admin_accounts")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Insert default admin account with hashed password
            default_password = generate_password_hash('0707200717')
            cursor.execute("""
                INSERT INTO admin_accounts (fullname, email, phone, password) 
                VALUES (%s, %s, %s, %s)
            """, ('Admin', 'admin@luxedrive.com', '1234567890', default_password))
            conn.commit()
            print("Default admin account created:")
            print("   Email: admin@luxedrive.com")
            print("   Full Name: Admin")
            print("   Phone: 1234567890")
            print("   Password: 0707200717")
        
        cursor.close()
        conn.close()
        
        print("Database tables created successfully!")
        return True
        
    except Error as e:
        print(f"Database initialization error: {e}")
        return False
