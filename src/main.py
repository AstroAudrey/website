import os
import sys
import platform
import threading
import subprocess
from app import app
from database.db_utils import Database, Config
from logger import logger, terminal_only_logger

def initialize_database():
    # Initialize database
    database_verification = Database.ensure_tables_exist()
    if not database_verification:
        logger.error("Failed to verify database connection and tables. Exiting.")
        sys.exit(1)
    else:
        terminal_only_logger.info("Database connection and tables verified successfully.")

def run_flask_app():
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:5000", "app:app"])

if __name__ == "__main__":
    # Initialize database
    initialize_database()

    if platform.system() == 'Windows':
        app.run(host='0.0.0.0', port=5050, debug=True)
    elif 'DOCKER_ENV_VARIABLE' in os.environ:
        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.start()
    else:
        # Default behavior (e.g., for Unix-like systems)
        app.run(host='0.0.0.0', port=5050, debug=True)