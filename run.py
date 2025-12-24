"""
Main Application Entry Point
Launch the PyQt6 E-Commerce Platform
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from backend.config import Config
from backend.database import db
from gui.auth.login_window import LoginWindow

# Setup logging
logging.basicConfig(
    level=logging.INFO if Config.DEBUG_MODE else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecommerce.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    logger.info("Starting E-Commerce Platform")
    
    # Validate configuration
    config_errors = Config.validate_config()
    if config_errors:
        for error in config_errors:
            logger.warning(error)
    
    # Test database connection
    try:
        if not db.test_connection():
            logger.error("Failed to connect to database")
            QMessageBox.critical(
                None,
                "Database Error",
                "Failed to connect to database.\n\n"
                "Please ensure:\n"
                "1. MySQL is running\n"
                "2. Database credentials in .env are correct\n"
                "3. Database has been initialized with schema.sql"
            )
            sys.exit(1)
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        QMessageBox.critical(
            None,
            "Database Error",
            f"Database connection failed:\n{str(e)}"
        )
        sys.exit(1)
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)
    app.setApplicationVersion(Config.APP_VERSION)
    
    # High DPI is enabled by default in PyQt6
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    logger.info("Application GUI loaded")
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
