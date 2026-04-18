import time
import random
from datetime import datetime

# Realistic log mapping
logs = [
    ("ERROR", "Database connection failed db=orders"),
    ("ERROR", "Timeout while calling payment API"),
    ("ERROR", "Payment failed transaction_id=789"),
    ("WARNING", "High memory usage detected service=auth"),
    ("WARNING", "Disk usage high server=prod-1"),
    ("INFO", "User login successful user_id=123"),
    ("INFO", "Order placed order_id=567"),
    ("INFO", "User logout user_id=123"),
]


def generate_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level, message = random.choice(logs)
    return f"{timestamp} {level} {message}\n"


if __name__ == "__main__":
    print("🔄 Generating logs... Press Ctrl+C to stop.\n")

    while True:
        log_line = generate_log()

        with open("logs/sample.log", "a", encoding="utf-8") as file:
            file.write(log_line)

        print(log_line.strip())

        time.sleep(2)