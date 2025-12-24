# 🛒 E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.10+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-yellow.svg)](LICENSE)

> **A complete, enterprise-grade e-commerce platform built with Python, PyQt6, and MySQL for academic demonstration.**

## 📌 Overview

This is a **full-stack e-commerce desktop application** featuring advanced database management, secure authentication, role-based access control, and a professional GUI. Built entirely for **university academic evaluation**, it demonstrates production-quality code while implementing COD-only payment for safety.

### ✨ Key Features

- 🔐 **Secure Authentication** - JWT tokens + bcrypt password hashing
- 👥 **9 User Roles** - Customer, Seller, Admin, Support, Manager, Investor, Supplier, Delivery, Marketing
- 🗄️ **40+ Database Tables** - Normalized schema with triggers, views, and stored procedures
- 🖥️ **Professional GUI** - PyQt6 with dark/light themes and responsive design
- 🛒 **Complete E-Commerce** - Product catalog, cart, orders, inventory, shipping, loyalty program
- 💳 **COD Payment** - Academic-safe Cash-on-Delivery simulation
- 📊 **Analytics** - Comprehensive reporting with SQL views
- 🔍 **50+ SQL Queries** - Complex queries with relational algebra documentation

## 🎯 Quick Start

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- Linux/macOS/Windows

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/E-commerce-Platform.git
cd E-commerce-Platform

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated database setup
./setup_database.sh
# Enter MySQL root password when prompted

# 5. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Launch application
python3 run.py
```

## 🔑 Demo Credentials

All demo users have password: **`Password123`**

| Username | Role | Access Level |
|----------|------|--------------|
| `customer1` | Customer | Product browsing, shopping cart, orders |
| `seller1` | Seller | Product management, inventory, orders |
| `admin1` | Admin | Full system administration |
| `support1` | Support | Customer tickets and support |
| `manager1` | Manager | Business analytics |
| `investor1` | Investor | Financial reports |
| `supplier1` | Supplier | Purchase orders |
| `delivery1` | Delivery Partner | Shipment management |
| `marketing1` | Marketing Agent | Campaign tracking |

## 📂 Project Structure

```
E-commerce-Platform/
├── 📁 backend/                  # Backend services
│   ├── config.py               # Application configuration
│   ├── database.py             # Database connection pool
│   ├── services/
│   │   └── auth_service.py     # Authentication logic
│   └── utils/
│       └── security.py         # Security utilities (JWT, bcrypt)
│
├── 📁 gui/                      # PyQt6 Desktop GUI
│   ├── auth/
│   │   ├── login_window.py     # Login interface
│   │   └── register_dialog.py  # Customer registration
│   ├── dashboards/
│   │   ├── customer_dashboard.py
│   │   ├── seller_dashboard.py
│   │   ├── admin_dashboard.py
│   │   └── [6 more role dashboards]
│   └── utils/
│       └── theme.py            # Dark/Light theme system
│
├── 📁 database/                 # Database scripts
│   ├── schema.sql              # 40+ tables
│   ├── triggers.sql            # 12 automated triggers
│   ├── views.sql               # 11 analytical views
│   ├── procedures.sql          # 5 stored procedures
│   └── seed_data.sql           # Demo data
│
├── 📁 Query/                    # SQL documentation
│   ├── sql_queries.sql         # 50+ example queries
│   ├── relational_algebra.md   # RA notation
│   └── README.md               # Query guide
│
├── 📄 run.py                    # Application entry point
├── 📄 setup_database.sh         # Automated DB setup
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example              # Configuration template
├── 📄 README.md                 # This file
├── 📄 QUICKSTART.md             # Fast setup guide
└── 📄 PROJECT_REPORT.md         # 40-page academic report
```

## 🎨 Features

### Customer Features
- ✅ Product browsing with search and filters
- ✅ Shopping cart with live totals
- ✅ Wishlist functionality
- ✅ Order history and tracking
- ✅ Loyalty points and tier system
- ✅ Product reviews and ratings
- ✅ COD checkout

### Seller Features
- ✅ Product management (CRUD)
- ✅ Inventory tracking (multi-warehouse)
- ✅ Order processing
- ✅ Sales analytics dashboard
- ✅ Revenue reporting

### Admin Features
- ✅ User management (all roles)
- ✅ Product administration
- ✅ Order monitoring
- ✅ Category & brand management
- ✅ Coupon creation
- ✅ Audit log viewing
- ✅ System statistics

### Additional Roles
- ✅ Support ticket management
- ✅ Delivery partner assignment
- ✅ Supplier purchase orders
- ✅ Marketing commission tracking
- ✅ Business analytics (Manager)
- ✅ Financial metrics (Investor)

## 🗄️ Database

### Schema Highlights

- **40+ Tables** organized in modules
- **12 Triggers** for automation (COD payment, loyalty points, notifications)
- **11 Views** for analytics (sales, inventory, customer LTV)
- **5 Stored Procedures** (order placement, refunds, delivery assignment)
- **Complete Normalization** (3NF)
- **Referential Integrity** with foreign keys
- **Performance Optimization** with strategic indexes

### Key Modules

| Module | Tables | Description |
|--------|--------|-------------|
| Authentication | 6 | Users, roles, permissions, sessions |
| Products | 5 | Catalog, categories, brands, images |
| Inventory | 3 | Multi-warehouse stock management |
| Orders | 6 | Orders, items, payments, refunds |
| Shipping | 5 | Delivery partners, tracking |
| Support | 3 | Ticket system |
| Marketing | 3 | Coupons, loyalty, referrals |

## 🔒 Security

- **Password Hashing:** bcrypt with 12 rounds
- **Authentication:** JWT tokens with expiration
- **Authorization:** Role-based access control (RBAC)
- **Audit Logging:** Complete activity trail
- **Input Validation:** SQL injection prevention
- **Session Management:** Token-based with timeout

## 🎓 Academic Features

### SQL Query Examples (50+)

Comprehensive query documentation in `Query/` directory:

- **DQL:** SELECT, JOIN, GROUP BY, HAVING, window functions
- **DML:** INSERT, UPDATE, DELETE with subqueries
- **DDL:** CREATE, ALTER, DROP with indexes
- **Aggregates:** COUNT, SUM, AVG, MIN, MAX
- **Subqueries:** Scalar, correlated, derived tables
- **Set Operations:** UNION, INTERSECT (simulated)
- **Window Functions:** ROW_NUMBER, RANK, LAG, LEAD

### Relational Algebra

Complete mappings from SQL to relational algebra notation:
- Selection (σ), Projection (π), Join (⋈)
- Set operations (∪, ∩, −)
- Aggregation (G), Ordering (τ)
- Step-by-step query transformations

## 🚀 Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.10+ |
| **GUI Framework** | PyQt6 |
| **Database** | MySQL 8.0+ |
| **Authentication** | JWT (PyJWT) |
| **Password Security** | bcrypt |
| **Charts** | matplotlib |
| **Data Processing** | pandas |
| **PDF Reports** | reportlab |

## 📊 Project Statistics

- **Lines of Code:** 10,000+
- **Python Files:** 25+
- **Database Tables:** 40+
- **SQL Triggers:** 12
- **SQL Views:** 11
- **Stored Procedures:** 5
- **GUI Dashboards:** 9
- **Demo Products:** 50+
- **Demo Users:** 12

## 📖 Documentation

- **[README.md](README.md)** - This file
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
- **[PROJECT_REPORT.md](PROJECT_REPORT.md)** - Complete 40-page academic report
- **[Query/README.md](Query/README.md)** - SQL query documentation
- **[Query/relational_algebra.md](Query/relational_algebra.md)** - RA notation guide

## 🎯 Use Cases

### Academic
- ✅ Database course final project
- ✅ Software engineering capstone
- ✅ Full-stack development demonstration
- ✅ Security implementation showcase

### Learning
- ✅ SQL query optimization
- ✅ Database design patterns
- ✅ PyQt6 GUI development
- ✅ Authentication & authorization
- ✅ Role-based access control

## ⚠️ Important Notice

**THIS IS AN ACADEMIC PROJECT**

- ❌ NOT for real commercial use
- ❌ NO real payment processing
- ❌ NO production deployment
- ✅ Academic demonstration only
- ✅ COD payment simulation
- ✅ Safe for university evaluation

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check MySQL is running
sudo systemctl status mysql

# Verify credentials
mysql -u ecommerce_user -proot ecommerce_db

# Re-run setup script
./setup_database.sh
```

### Module Import Errors

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Login Issues

**Problem:** Can't login with demo credentials

**Solution:**
```bash
# Run password fix script
python3 -c "
from backend.utils.security import SecurityUtils
from backend.database import db
hash = SecurityUtils.hash_password('Password123')
db.execute_update('UPDATE users SET password_hash = %s', (hash,))
print('Passwords reset successfully')
"
```

## 🤝 Contributing

This is an academic project. For improvements:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request

## 📝 License

This project is created for **academic purposes only**. 

- Use for educational and demonstration purposes
- Do NOT use for commercial applications
- Do NOT deploy with real customer data
- Cite appropriately if using code snippets

## 👨‍💻 Author

**University Student Project**  
Course: Advanced Database Management & Software Engineering  
Institution: [Your University Name]  
Date: December 2024

## 🙏 Acknowledgments

- PyQt6 for excellent GUI framework
- MySQL for robust database management
- Python community for amazing libraries
- University instructors for guidance

## 📧 Contact

For academic inquiries or project questions:
- Open an issue on GitHub
- Review documentation in project files
- Check troubleshooting section above

---

## ⭐ Star this repository if you found it helpful!

**Built with ❤️ for academic excellence**

---

### Quick Links

- [Installation Guide](#installation)
- [Demo Credentials](#-demo-credentials)
- [Features](#-features)
- [Database Schema](#️-database)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** ✅ Complete and Ready for Demonstration
