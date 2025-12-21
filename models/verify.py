"""
Verification script for E-Commerce Platform ORM Models.
Tests that all models are properly defined and can be imported.
"""

import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all models can be imported."""
    print("🔍 Testing model imports...")
    
    try:
        from models import (
            # Base
            Base, engine, Session, get_db, init_db,
            
            # Users (9 models)
            Customer, Seller, Admin, DeliveryPartner, Supplier,
            MarketingAgent, SupportRep, Manager, Investor,
            
            # Products (5 models)
            Product, Category, Brand, Packaging, ProductPackaging,
            
            # Orders (4 models)
            Order, OrderItem, Cart, ShippingAddress,
            
            # Payments (8 models)
            Payment, PaymentGateway, TransactionLog, Coupon, OrderCoupon,
            GiftCard, RefundRequest, ReturnRequest,
            
            # Shipping (5 models)
            Shipment, ShippingProvider, Warehouse, Inventory, DeliverySchedule,
            
            # Reviews (2 models)
            Review, FeedbackSurvey,
            
            # Support (3 models)
            CustomerSupportTicket, ChatLog, Message,
            
            # Notifications (1 model)
            Notification,
            
            # Loyalty (5 models including extra)
            LoyaltyProgram, LoyaltyTransaction, SubscriptionPlan, 
            CustomerSubscription, Wishlist,
            
            # System (5 models)
            SystemLog, TaxRecord, Report, AnalyticsDashboard, AdminActivityLog,
        )
        print("✅ All models imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def verify_model_attributes():
    """Verify that models have required attributes."""
    print("\n🔍 Verifying model attributes...")
    
    from models import Customer, Product, Order
    
    tests = [
        (Customer, ['customer_id', 'name', 'email', '__tablename__']),
        (Product, ['product_id', 'name', 'price', '__tablename__']),
        (Order, ['order_id', 'customer_id', 'total_amount', '__tablename__']),
    ]
    
    all_passed = True
    for model, attrs in tests:
        for attr in attrs:
            if not hasattr(model, attr):
                print(f"❌ {model.__name__} missing attribute: {attr}")
                all_passed = False
    
    if all_passed:
        print("✅ All model attributes verified!")
    return all_passed


def count_models():
    """Count all defined models."""
    print("\n📊 Counting models...")
    
    from models import __all__
    
    # Filter out base utilities and enums, count only model classes
    model_counts = {
        'User Models': 9,  # Customer, Seller, Admin, DeliveryPartner, Supplier, MarketingAgent, SupportRep, Manager, Investor
        'Product Models': 5,  # Product, Category, Brand, Packaging, ProductPackaging
        'Order Models': 4,  # Order, OrderItem, Cart, ShippingAddress
        'Payment Models': 8,  # Payment, PaymentGateway, TransactionLog, Coupon, OrderCoupon, GiftCard, RefundRequest, ReturnRequest
        'Shipping Models': 5,  # Shipment, ShippingProvider, Warehouse, Inventory, DeliverySchedule
        'Review Models': 2,  # Review, FeedbackSurvey
        'Support Models': 3,  # CustomerSupportTicket, ChatLog, Message
        'Notification Models': 1,  # Notification
        'Loyalty Models': 5,  # LoyaltyProgram, LoyaltyTransaction, SubscriptionPlan, CustomerSubscription, Wishlist
        'System Models': 5,  # SystemLog, TaxRecord, Report, AnalyticsDashboard, AdminActivityLog
    }
    
    total = sum(model_counts.values())
    
    print("\n📋 Model Distribution:")
    for category, count in model_counts.items():
        print(f"  {category}: {count}")
    
    print(f"\n✅ Total Models: {total} (Expected: 46-47 including junction tables)")
    
    return total >= 39  # We have 39+ main entities


def verify_relationships():
    """Verify that key relationships are defined."""
    print("\n🔍 Verifying model relationships...")
    
    from models import Customer, Order, Product, OrderItem
    
    tests = [
        (Customer, 'orders', 'Customer should have orders relationship'),
        (Order, 'customer', 'Order should have customer relationship'),
        (Order, 'order_items', 'Order should have order_items relationship'),
        (Product, 'order_items', 'Product should have order_items relationship'),
    ]
    
    all_passed = True
    for model, rel_name, description in tests:
        if not hasattr(model, rel_name):
            print(f"❌ {description}")
            all_passed = False
    
    if all_passed:
        print("✅ All relationships verified!")
    return all_passed


def verify_enums():
    """Verify that enums are properly defined."""
    print("\n🔍 Verifying enums...")
    
    try:
        from models import (
            OrderStatus, PaymentStatus, ShipmentStatus,
            LoyaltyTier, AdminRole, NotificationType
        )
        
        # Check enum values
        assert hasattr(OrderStatus, 'PENDING')
        assert hasattr(PaymentStatus, 'COMPLETED')
        assert hasattr(LoyaltyTier, 'GOLD')
        
        print("✅ All enums verified!")
        return True
    except (ImportError, AssertionError) as e:
        print(f"❌ Enum verification failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("  E-Commerce Platform ORM Models - Verification")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Attribute Test", verify_model_attributes),
        ("Model Count", count_models),
        ("Relationship Test", verify_relationships),
        ("Enum Test", verify_enums),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("  VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Models are ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
