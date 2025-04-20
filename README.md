# Real-Time Anomaly Detection in Transactions

This project implements a **real-time anomaly detection system** for financial transactions using streaming data, machine learning, and data visualization. It detects fraudulent transactions using PyOD and Isolation Forest, processes data in real-time using Redpanda (Kafka-compatible), and stores anomalies in a PostgreSQL database, which are then displayed through a live dashboard built with Streamlit.

---

## Tech Stack
- **Producer:** Python + `kafka-python` (Redpanda-compatible)
- **Streaming Platform:** [Redpanda](https://redpanda.com/) (Kafka-compatible)
- **Anomaly Detection:** Python, [PyOD](https://github.com/yzhao062/pyod), Isolation Forest
- **Storage:** PostgreSQL (via Docker)
- **Dashboard:** Streamlit

---

## ?? Project Structure

```bash
RealTime-Anomaly-Detection/
??? producer/              # Kafka producer script
??? detector/              # PyOD anomaly detection script
??? dashboard/             # Streamlit dashboard
??? docker-compose.yml     # Redpanda and PostgreSQL setup
??? requirements.txt       # Python dependencies
??? README.md


---

##  Setup Instructions (for macOS / Windows with WSL)

### 1. Clone the repository
```bash
git clone https://github.com/Kruti0910/RealTime-Anomaly-Detection.git
cd RealTime-Anomaly-Detection
```

### 2. Install Python dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Start Docker services
Ensure Docker is installed and running.
```bash
docker-compose up -d
```
This will start Redpanda (Kafka) and PostgreSQL.

### 4. Create Kafka topic
Install Redpanda CLI (`rpk`) if not already installed:
```bash
curl -LO https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-linux-amd64.zip
unzip rpk-linux-amd64.zip -d ~/.local/bin
chmod +x ~/.local/bin/rpk
```
Then create the topic:
```bash
rpk topic create transactions --brokers localhost:9092
```

---

##  Running the Application

### A. Start the Kafka Producer (generates transaction data)
```bash
python3 producer/produce.py
```

### B. Start the Real-Time Anomaly Detector
This listens to the Kafka topic and writes anomalies to PostgreSQL:
```bash
python3 detector/anomaly_detector.py
```

### C. Launch the Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

##  Verifying PostgreSQL Data
You can check the `frauds` table manually:
```bash
docker exec -it realtime-anomaly-detection-postgres-1 psql -U user -d anomalies
```
Then inside the DB:
```sql
SELECT * FROM frauds;
```

---

##  Python Dependencies (requirements.txt)
```
kafka-python
pyod
pandas
numpy
psycopg2-binary
streamlit
altair
streamlit-autorefresh
```

---

##  Expected Output
- Transactions being printed in terminal via producer
- Detected anomalies logged via detector
- Real-time dashboard showing anomaly table and bar chart of amounts by location

---

##  Notes
- Works on macOS and Windows (with WSL)
- Tested with Python 3.10+
- Make sure Docker Desktop is running

