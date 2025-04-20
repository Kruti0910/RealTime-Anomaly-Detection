from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    txn = {
        "user_id": random.randint(1, 100),
        "amount": round(random.uniform(1.0, 10000.0), 2),
        "location": random.choice(["US", "IN", "UK"]),
        "timestamp": time.time()
    }
    producer.send("transactions", txn)
    print("Sent:", txn)
    time.sleep(1)
