import json
import time
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_order_event(order_id=None):
    """Simulates a customer placing an order."""
    o_id = order_id or str(uuid.uuid4())
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "ORDER_PLACED",
        "event_timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "order_id": o_id,
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "items": [
                {
                    "product_id": f"PROD-{random.randint(100, 500)}",
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(10.0, 500.0), 2)
                } for _ in range(random.randint(1, 4))
            ],
            "total_amount": round(random.uniform(50.0, 2000.0), 2),
            "currency": "USD",
            "shipping_address": fake.address().replace("\n", ", ")
        }
    }

def generate_payment_event(order_id, status="SUCCESS"):
    """Simulates a payment confirmation or failure."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "PAYMENT_PROCESSED",
        "event_timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "order_id": order_id,
            "payment_id": f"PAY-{uuid.uuid4().hex[:8].upper()}",
            "payment_method": random.choice(["CREDIT_CARD", "PAYPAL", "STRIPE", "APPLE_PAY"]),
            "status": status,
            "error_code": None if status == "SUCCESS" else random.choice(["INSUFFICIENT_FUNDS", "EXPIRED_CARD", "GATEWAY_TIMEOUT"])
        }
    }

def generate_inventory_event():
    """Simulates inventory stock updates."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "INVENTORY_UPDATE",
        "event_timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "product_id": f"PROD-{random.randint(100, 500)}",
            "warehouse_id": random.choice(["WH-EAST-01", "WH-WEST-02", "WH-CENTRAL-01"]),
            "change_type": random.choice(["RESTOCK", "DAMAGE", "RETURN_TO_STOCK"]),
            "quantity_delta": random.randint(1, 100)
        }
    }

if __name__ == "__main__":
    # Quick test to see if it works
    print("Simulating 5 events...")
    for _ in range(5):
        order = generate_order_event()
        print(json.dumps(order, indent=2))
        time.sleep(0.5)
        
        # 80% chance of a success payment following an order immediately
        if random.random() > 0.2:
            payment = generate_payment_event(order["payload"]["order_id"])
            print(json.dumps(payment, indent=2))
    
    # 2 events with duplicate order IDs to test silver layer deduplication
    print("\n--- Simulating Duplicates ---")
    dup_id = str(uuid.uuid4())
    print(json.dumps(generate_order_event(dup_id), indent=2))
    time.sleep(1)
    print(json.dumps(generate_order_event(dup_id), indent=2))
