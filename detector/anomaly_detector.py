from kafka import KafkaConsumer
from pyod.models.iforest import IForest
import pandas as pd
import psycopg2
import json
import time

# Kafka consumer configuration
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='anomaly-detector-group'
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="anomalies",
    user="user",
    password="pass",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS frauds (
        user_id INT,
        amount FLOAT,
        location TEXT,
        timestamp FLOAT
    )
""")
conn.commit()

print("Listening for transactions...")

# Buffer to hold incoming messages
batch = []
BATCH_SIZE = 10

for msg in consumer:
    txn = msg.value
    batch.append(txn)

    if len(batch) >= BATCH_SIZE:
        df = pd.DataFrame(batch)
        batch = []

        try:
            model = IForest()
            model.fit(df[['amount']])
            df['anomaly'] = model.predict(df[['amount']])

            anomalies = df[df['anomaly'] == 1]
            for _, row in anomalies.iterrows():
                cursor.execute("""
                    INSERT INTO frauds (user_id, amount, location, timestamp)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row.user_id,
                    row.amount,
                    row.location,
                    float(row.timestamp)  # ensure proper format
                ))

            conn.commit()
            print(f"Inserted {len(anomalies)} anomalies")

        except Exception as e:
            print("Anomaly detection failed:", e)
            continue
