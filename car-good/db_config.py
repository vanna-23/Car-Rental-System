import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL server host
    'user': 'root',           # Your MySQL username
    'password': 'your_password',  # Your MySQL password
    'database': 'car_rental'  # Your database name
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize the database with required tables"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create admin_accounts table
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
        
        # Create cars table
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
        
        # Create bookings table
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
        
        # Insert default admin account
        cursor.execute("""
            INSERT IGNORE INTO admin_accounts (username, name, email, password)
            VALUES ('admin', 'Administrator', 'admin@luxedrive.com', '0707200717')
        """)
        
        connection.commit()
        print("✅ Database tables created successfully!")
        print("✅ Default admin account created: admin / 0707200717")
        return True
        
    except Error as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    # Run this file directly to initialize the database
    init_database()
