from pyod.models.iforest import IForest
import pandas as pd
import psycopg2

df = pd.read_json("mock_batch.json") 

model = IForest()
model.fit(df[['amount']])
df['anomaly'] = model.predict(df[['amount']])

conn = psycopg2.connect(
    dbname="anomalies", user="user", password="pass", host="localhost", port="5432")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS frauds (user_id INT, amount FLOAT, location TEXT, timestamp FLOAT)")

for _, row in df[df['anomaly'] == 1].iterrows():
    cursor.execute("INSERT INTO frauds VALUES (%s, %s, %s, %s)", 
                   (row.user_id, row.amount, row.location, row.timestamp))

conn.commit()
conn.close()
