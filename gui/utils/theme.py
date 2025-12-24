"""
Theme Management and Styling
Provides dark/light themes for the application
"""

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class Theme:
    """Application theme management"""
    
    # Color palette
    COLORS = {
        # Primary colors
        'primary': '#2563eb',  # Blue
        'primary_dark': '#1e40af',
        'primary_light': '#60a5fa',
        
        # Secondary colors
        'secondary': '#7c3aed',  # Purple
        'secondary_dark': '#5b21b6',
        'secondary_light': '#a78bfa',
        
        # Success/Error/Warning
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6',
        
        # Neutral (Dark theme)
        'dark_bg': '#1e1e2e',
        'dark_surface': '#27293d',
        'dark_surface_light': '#363852',
        'dark_text': '#ffffff',
        'dark_text_secondary': '#a1a1aa',
        'dark_border': '#3f3f46',
        
        # Neutral (Light theme)
        'light_bg': '#ffffff',
        'light_surface': '#f9fafb',
        'light_surface_dark': '#f3f4f6',
        'light_text': '#111827',
        'light_text_secondary': '#6b7280',
        'light_border': '#e5e7eb',
    }
    
    @staticmethod
    def get_dark_stylesheet() -> str:
        """Get dark theme stylesheet"""
        return f"""
            /* Main Application */
            QMainWindow, QDialog, QWidget {{
                background-color: {Theme.COLORS['dark_bg']};
                color: {Theme.COLORS['dark_text']};
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                font-size: 13px;
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {Theme.COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 500;
                min-width: 80px;
            }}
            
            QPushButton:hover {{
                background-color: {Theme.COLORS['primary_dark']};
            }}
            
            QPushButton:pressed {{
                background-color: {Theme.COLORS['primary_light']};
            }}
            
            QPushButton:disabled {{
                background-color: {Theme.COLORS['dark_surface_light']};
                color: {Theme.COLORS['dark_text_secondary']};
            }}
            
            QPushButton.secondary {{
                background-color: {Theme.COLORS['dark_surface_light']};
                color: {Theme.COLORS['dark_text']};
            }}
            
            QPushButton.secondary:hover {{
                background-color: {Theme.COLORS['dark_border']};
            }}
            
            QPushButton.success {{
                background-color: {Theme.COLORS['success']};
            }}
            
            QPushButton.danger {{
                background-color: {Theme.COLORS['error']};
            }}
            
            /* Input Fields */
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 2px solid {Theme.COLORS['primary']};
            }}
            
            /* Combo Box */
            QComboBox {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                selection-background-color: {Theme.COLORS['primary']};
                border: 1px solid {Theme.COLORS['dark_border']};
            }}
            
            /* Tables */
            QTableWidget, QTableView {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                gridline-color: {Theme.COLORS['dark_border']};
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
            }}
            
            QTableWidget::item, QTableView::item {{
                padding: 8px;
            }}
            
            QTableWidget::item:selected, QTableView::item:selected {{
                background-color: {Theme.COLORS['primary']};
            }}
            
            QHeaderView::section {{
                background-color: {Theme.COLORS['dark_surface_light']};
                color: {Theme.COLORS['dark_text']};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {Theme.COLORS['primary']};
                font-weight: 600;
            }}
            
            /* List Widget */
            QListWidget {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
            }}
            
            QListWidget::item {{
                padding: 8px;
            }}
            
            QListWidget::item:selected {{
                background-color: {Theme.COLORS['primary']};
            }}
            
            /* Scroll Bar */
            QScrollBar:vertical {{
                background-color: {Theme.COLORS['dark_surface']};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {Theme.COLORS['dark_border']};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {Theme.COLORS['dark_text_secondary']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Labels */
            QLabel {{
                color: {Theme.COLORS['dark_text']};
            }}
            
            QLabel.title {{
                font-size: 24px;
                font-weight: 700;
                color: {Theme.COLORS['dark_text']};
                margin-bottom: 10px;
            }}
            
            QLabel.subtitle {{
                font-size: 16px;
                font-weight: 600;
                color: {Theme.COLORS['dark_text']};
            }}
            
            QLabel.caption {{
                font-size: 12px;
                color: {Theme.COLORS['dark_text_secondary']};
            }}
            
            /* Group Box */
            QGroupBox {{
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            
            /* Tab Widget */
            QTabWidget::pane {{
                border: 1px solid {Theme.COLORS['dark_border']};
                border-radius: 6px;
                background-color: {Theme.COLORS['dark_surface']};
            }}
            
            QTabBar::tab {{
                background-color: {Theme.COLORS['dark_surface_light']};
                color: {Theme.COLORS['dark_text_secondary']};
                border: none;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {Theme.COLORS['primary']};
                color: white;
            }}
            
            /* Menu Bar */
            QMenuBar {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border-bottom: 1px solid {Theme.COLORS['dark_border']};
            }}
            
            QMenuBar::item:selected {{
                background-color: {Theme.COLORS['primary']};
            }}
            
            QMenu {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border: 1px solid {Theme.COLORS['dark_border']};
            }}
            
            QMenu::item:selected {{
                background-color: {Theme.COLORS['primary']};
            }}
            
            /* Status Bar */
            QStatusBar {{
                background-color: {Theme.COLORS['dark_surface']};
                color: {Theme.COLORS['dark_text']};
                border-top: 1px solid {Theme.COLORS['dark_border']};
            }}
            
            /* Checkboxes and Radio Buttons */
            QCheckBox, QRadioButton {{
                color: {Theme.COLORS['dark_text']};
                spacing: 8px;
            }}
            
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {Theme.COLORS['dark_border']};
                border-radius: 4px;
                background-color: {Theme.COLORS['dark_surface']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {Theme.COLORS['primary']};
                border-color: {Theme.COLORS['primary']};
            }}
            
            QRadioButton::indicator {{
                border-radius: 9px;
            }}
        """
    
    @staticmethod
    def get_light_stylesheet() -> str:
        """Get light theme stylesheet"""
        return f"""
            /* Main Application */
            QMainWindow, QDialog, QWidget {{
                background-color: {Theme.COLORS['light_bg']};
                color: {Theme.COLORS['light_text']};
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                font-size: 13px;
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {Theme.COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 500;
                min-width: 80px;
            }}
            
            QPushButton:hover {{
                background-color: {Theme.COLORS['primary_dark']};
            }}
            
            QPushButton:pressed {{
                background-color: {Theme.COLORS['primary_light']};
            }}
            
            QPushButton:disabled {{
                background-color: {Theme.COLORS['light_surface_dark']};
                color: {Theme.COLORS['light_text_secondary']};
            }}
            
            QPushButton.secondary {{
                background-color: {Theme.COLORS['light_surface_dark']};
                color: {Theme.COLORS['light_text']};
            }}
            
            QPushButton.secondary:hover {{
                background-color: {Theme.COLORS['light_border']};
            }}
            
            QPushButton.success {{
                background-color: {Theme.COLORS['success']};
            }}
            
            QPushButton.danger {{
                background-color: {Theme.COLORS['error']};
            }}
            
            /* Input Fields */
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
                background-color: {Theme.COLORS['light_bg']};
                color: {Theme.COLORS['light_text']};
                border: 1px solid {Theme.COLORS['light_border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                border: 2px solid {Theme.COLORS['primary']};
            }}
            
            /* Combo Box */
            QComboBox {{
                background-color: {Theme.COLORS['light_bg']};
                color: {Theme.COLORS['light_text']};
                border: 1px solid {Theme.COLORS['light_border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {Theme.COLORS['light_bg']};
                color: {Theme.COLORS['light_text']};
                selection-background-color: {Theme.COLORS['primary']};
                border: 1px solid {Theme.COLORS['light_border']};
            }}
            
            /* Tables */
            QTableWidget, QTableView {{
                background-color: {Theme.COLORS['light_bg']};
                color: {Theme.COLORS['light_text']};
                gridline-color: {Theme.COLORS['light_border']};
                border: 1px solid {Theme.COLORS['light_border']};
                border-radius: 6px;
            }}
            
            QTableWidget::item:selected, QTableView::item:selected {{
                background-color: {Theme.COLORS['primary']};
                color: white;
            }}
            
            QHeaderView::section {{
                background-color: {Theme.COLORS['light_surface']};
                color: {Theme.COLORS['light_text']};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {Theme.COLORS['primary']};
                font-weight: 600;
            }}
            
            /* Group Box */
            QGroupBox {{
                border: 1px solid {Theme.COLORS['light_border']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
            
            /* Labels */
            QLabel.title {{
                font-size: 24px;
                font-weight: 700;
            }}
            
            QLabel.subtitle {{
                font-size: 16px;
                font-weight: 600;
            }}
            
            QLabel.caption {{
                font-size: 12px;
                color: {Theme.COLORS['light_text_secondary']};
            }}
        """
