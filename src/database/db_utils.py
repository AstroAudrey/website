import json
import mariadb
from database.db_config import DB_CONFIG
from logger import logger, terminal_only_logger

class Database:
    """Base class to handle database connections."""
    
    @staticmethod
    def get_connection():
        try:
            conn = mariadb.connect(
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database']
            )
            return conn
        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB Platform: {e}")
            return None
    
    @staticmethod
    def ensure_tables_exist():
        tables = {
            'configs': """
                CREATE TABLE configs (
                    `key` VARCHAR(255) PRIMARY KEY,
                    `value` TEXT NOT NULL
                );
            """
        }
        
        conn = Database.get_connection()
        if not conn:
            logger.error("Failed to connect to database.")
            return False
        
        try:
            cursor = conn.cursor()
            for table_name, create_statement in tables.items():
                # Check if the table exists
                cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?", (DB_CONFIG['database'], table_name))
                exists = cursor.fetchone()[0]
                
                if not exists:
                    cursor.execute(create_statement)
                    conn.commit()
                    logger.info(f"Table '{table_name}' created successfully.")
                # else:
                    # logger.info(f"Table '{table_name}' already exists.")
            return True
        except mariadb.Error as e:
            logger.error(f"Error ensuring tables exist: {e}")
            return False
        finally:
            conn.close()

class Config(Database):
    """Handles CRUD operations for the Configs table."""
    
    @staticmethod
    def load(specific_key=None):
        conn = Config.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            if specific_key is None:
                cursor.execute("SELECT `key`, `value` FROM configs")
            else:
                cursor.execute("SELECT `value` FROM configs WHERE `key` = ?", (specific_key,))
                
            rows = cursor.fetchall()
            if specific_key:
                row = rows[0] if rows else None
                return json.loads(row[0]) if row and row[0] else None
            else:
                return {row[0]: json.loads(row[1]) if row[1] else None for row in rows}
        except mariadb.Error as e:
            logger.error(f"Error loading config from database: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def save(key, value):
        conn = Config.get_connection()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO configs (`key`, `value`) VALUES (?, ?)"
                "ON DUPLICATE KEY UPDATE `value` = VALUES(`value`)",
                (key, json.dumps(value))
            )
            conn.commit()
            return True
        except mariadb.Error as e:
            logger.error(f"Error saving config '{key}' to database: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(key):
        conn = Config.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM configs WHERE `key` = ?", (key,))
            conn.commit()
            return True
        except mariadb.Error as e:
            logger.error(f"Error deleting config '{key}' from database: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()


# Example usage:
# Load all configs
# all_configs = Config.load()
# print("Configs:", all_configs)

# Save a config
# success = Config.save("some_key", {"some": "value"})
# print("Config saved:", success)

# Delete a config
# success = Config.delete("some_key")
# print("Config deleted:", success)

