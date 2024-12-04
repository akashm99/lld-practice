from datetime import datetime
from uuid import uuid4
from typing import List, Dict

# Coupon Factory
class CouponFactory:
    @staticmethod
    def create_coupon(rules: Dict, overall_limit: int, per_user_limit: int, expiry_date: datetime):
        return Coupon(rules, overall_limit, per_user_limit, expiry_date)

# Base Coupon Class
class Coupon:
    def __init__(self, rules: Dict, overall_limit: int, per_user_limit: int, expiry_date: datetime):
        self.id = str(uuid4())
        self.rules = rules
        self.overall_limit = overall_limit
        self.per_user_limit = per_user_limit
        self.usage_count = 0
        self.active = True
        self.expiry_date = expiry_date

    def is_valid(self, user) -> bool:
        # Validation logic using strategy pattern
        return all(strategy.validate(user) for strategy in self.rules['validation_strategies'])

# Strategy Interface
class CouponStrategy:
    def validate(self, user) -> bool:
        pass

# Age Validation Strategy
class AgeValidationStrategy(CouponStrategy):
    def validate(self, user) -> bool:
        return user.age > 18

# Cart Value Validation Strategy
class CartValueValidationStrategy(CouponStrategy):
    def validate(self, user) -> bool:
        return user.cart_value > 1000

# Admin Command Class
class AdminCommand:
    @staticmethod
    def activate_coupon(coupon: Coupon):
        coupon.active = True

    @staticmethod
    def deactivate_coupon(coupon: Coupon):
        coupon.active = False

# Voucher Class
class Voucher:
    def __init__(self, voucher_type: str, user_id=None):
        self.id = str(uuid4())
        self.voucher_type = voucher_type  # 'unassigned' or 'preassigned'
        self.user_id = user_id
        self.used = False

# Example Controller
class CouponVoucherController:
    def __init__(self):
        self.coupons = []
        self.vouchers = []

    def create_coupon(self, rules, overall_limit, per_user_limit, expiry_date):
        coupon = CouponFactory.create_coupon(rules, overall_limit, per_user_limit, expiry_date)
        self.coupons.append(coupon)
        return coupon.id

    def delete_coupon(self, coupon_id):
        self.coupons = [c for c in self.coupons if c.id != coupon_id]

    def list_coupons(self):
        return [vars(coupon) for coupon in self.coupons if coupon.active]

    def create_voucher(self, voucher_type, user_id=None):
        voucher = Voucher(voucher_type, user_id)
        self.vouchers.append(voucher)
        return voucher.id

    def list_vouchers(self):
        return [vars(voucher) for voucher in self.vouchers]

# Example Usage
if __name__ == "__main__":
    controller = CouponVoucherController()
    # Create some strategies for coupon validation
    age_strategy = AgeValidationStrategy()
    cart_value_strategy = CartValueValidationStrategy()

    # Example of creating a coupon
    rules = {
        'validation_strategies': [age_strategy, cart_value_strategy]
    }
    coupon_id = controller.create_coupon(rules, overall_limit=10, per_user_limit=1, expiry_date=datetime(2024, 12, 31))
    print(f"Coupon created with ID: {coupon_id}")

    # List coupons
    print("Active Coupons:", controller.list_coupons())

    # Create a voucher
    voucher_id = controller.create_voucher('unassigned')
    print(f"Voucher created with ID: {voucher_id}")

    # List vouchers
    print("Vouchers:", controller.list_vouchers())
