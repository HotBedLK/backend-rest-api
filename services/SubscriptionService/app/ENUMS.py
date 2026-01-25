from enum import Enum

# payment method enums
class PaymentMethod(str, Enum):
    VISA = "VISA"
    MASTER = "MASTER"
    AMEX = "AMEX"
    EZCASH = "EZCASH"
    MCASH = "MCASH"
    GENIE = "GENIE"

class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"