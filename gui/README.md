# E-Commerce Database GUI Application

## Python GUI for DML Operations

This is a desktop GUI application built with Python tkinter for demonstrating database operations on the E-Commerce platform.

## Features

- **Product Management** (INSERT, UPDATE, DELETE, SELECT)
- **Customer Management** (INSERT, UPDATE, DELETE, SELECT)
- **Order Viewing** (SELECT with JOIN)
- **Inventory Updates** (UPDATE operations)
- **Custom SQL Query Executor**

## Requirements

- Python 3.8+
- MySQL Server
- mysql-connector-python

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure MySQL database is set up:
```bash
mysql -u root -p < ../database/schema_phpmyadmin.sql
mysql -u root -p < ../database/views.sql
mysql -u root -p < ../database/user_access_control.sql
```

3. Update database credentials in `ecommerce_gui.py` (lines 15-18):
```python
HOST = 'localhost'
USER = 'ecommerce_user'
PASSWORD = 'SecurePass123!'
DATABASE = 'ecommerce_db'
```

## Running the Application

```bash
python3 ecommerce_gui.py
```

Or make it executable:
```bash
chmod +x ecommerce_gui.py
./ecommerce_gui.py
```

## GUI Tabs

### 1. Products (CRUD)
- **INSERT**: Add new products to catalog
- **UPDATE**: Modify existing product details
- **DELETE**: Remove products from database
- **SELECT**: View all products in table

### 2. Customers (CRUD)
- **INSERT**: Register new customers
- **UPDATE**: Update customer information
- **DELETE**: Remove customer accounts
- **SELECT**: View all customers

### 3. Orders (SELECT)
- **SELECT with JOIN**: View orders with customer names
- Demonstrates INNER JOIN operation

### 4. Inventory (UPDATE)
- **UPDATE**: Modify inventory quantities
- **SELECT**: View current stock levels

### 5. Custom Query
- Execute any SQL query
- View results in scrollable text area

## DML Operations Demonstrated

✅ **INSERT** - Adding records to tables  
✅ **UPDATE** - Modifying existing records  
✅ **DELETE** - Removing records  
✅ **SELECT** - Retrieving data  
✅ **JOIN** - Combining data from multiple tables  

## Screenshots

Take screenshots of the following for academic documentation:

1. Main window with all tabs
2. Product INSERT operation
3. Customer UPDATE operation
4. Order SELECT with JOIN results
5. Inventory UPDATE operation
6. Custom query execution

## Troubleshooting

### Connection Error
If you get "Failed to connect to database":
- Check MySQL is running: `sudo systemctl status mysql`
- Verify user exists: `mysql -u ecommerce_user -p`
- Check password in code matches database

### Import Error
If you get "No module named 'mysql.connector'":
```bash
pip3 install mysql-connector-python
```

### Permission Error
If you get "Access denied":
- Run user access control script first
- Verify user permissions in MySQL

## Academic Use

This GUI demonstrates all required DML operations for Database Management Systems course:

- **R#7 (Bonus)**: GUI Implementation
- All CRUD operations (CREATE, READ, UPDATE, DELETE)
- JOIN operations
- Custom query execution
- Professional user interface

## License

Academic Project - Database Management Systems  
Fall 2025/2026
