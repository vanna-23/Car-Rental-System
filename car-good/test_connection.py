from .db_config import get_db_connection

def test_connection():
    """Test MySQL database connection"""
    print("Testing MySQL connection...")
    
    connection = get_db_connection()
    
    if connection and connection.is_connected():
        db_info = connection.get_server_info()
        print(f"✓ Successfully connected to MySQL Server version {db_info}")
        
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        database = cursor.fetchone()
        print(f"✓ Connected to database: {database[0]}")
        
        cursor.close()
        connection.close()
        print("✓ Connection closed successfully")
        return True
    else:
        print("✗ Failed to connect to MySQL")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in db_config.py are correct")
        print("3. Database 'car_rental' exists")
        return False

if __name__ == "__main__":
    test_connection()
