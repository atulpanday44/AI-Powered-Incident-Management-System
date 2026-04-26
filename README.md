# AI-Powered Incident Management System

A production-grade, event-driven backend system for intelligent incident management using artificial intelligence, anomaly detection, and log clustering.

## 🎯 Overview

This system provides:

- **Real-time Log Ingestion**: FastAPI service for receiving application logs
- **Event-Driven Architecture**: Apache Kafka for scalable event processing
- **AI/ML Capabilities**: Anomaly detection and log clustering
- **Incident Management**: Automatic incident creation, deduplication, and severity classification
- **PostgreSQL Storage**: Persistent storage for logs and incidents
- **React UI**: Modern web interface for viewing incidents and logs
- **Docker Deployment**: Complete containerized setup with Docker Compose

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Services                      │
└──────────────────┬──────────────────────────────────────────┘
                   │ (Sends logs)
                   ▼
        ┌──────────────────────┐
        │   FastAPI Service    │
        │  (Log Ingestion API) │
        └──────────┬───────────┘
                   │ (Publishes)
                   ▼
        ┌──────────────────────┐
        │   Kafka Topic:       │
        │   logs-topic         │
        └──────────┬───────────┘
                   │ (Consumes)
                   ▼
        ┌──────────────────────────┐
        │  Kafka Consumer Service  │
        │  (Log Processing Engine) │
        └──────────┬───────────────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Anomaly │ │        │ │        │
    │Detect. │ │Cluster │ │Dedup.  │
    └────┬───┘ └───┬────┘ └───┬────┘
         │         │          │
         └─────────┼──────────┘
                   ▼
        ┌──────────────────────┐
        │  Incident Engine     │
        │  (Severity Classify) │
        └──────────┬───────────┘
                   │ (Creates/Updates)
                   ▼
        ┌──────────────────────┐
        │  PostgreSQL Database │
        │  (Logs & Incidents)  │
        └──────────────────────┘
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                      # FastAPI routes
│   │   ├── logs.py              # Log ingestion endpoints
│   │   ├── incidents.py         # Incident management endpoints
│   │   └── __init__.py
│   │
│   ├── core/                     # Configuration and logging
│   │   ├── config.py            # Settings from environment variables
│   │   ├── logging_config.py    # Structured JSON logging
│   │   └── __init__.py
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── incident.py          # Log and Incident models
│   │   └── __init__.py
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── schemas.py           # Request/response validation
│   │   └── __init__.py
│   │
│   ├── services/                 # Business logic
│   │   ├── incident_service.py  # Log and Incident services
│   │   └── __init__.py
│   │
│   ├── kafka/                    # Event streaming
│   │   ├── producer.py          # Kafka producer
│   │   ├── consumer.py          # Kafka consumer
│   │   └── __init__.py
│   │
│   ├── ai/                       # AI/ML modules
│   │   ├── anomaly_detection.py # Statistical anomaly detection
│   │   ├── clustering.py        # Log clustering with TF-IDF
│   │   └── __init__.py
│   │
│   ├── incident/                 # Incident management
│   │   ├── deduplication.py     # Incident deduplication
│   │   ├── severity.py          # Severity classification
│   │   └── __init__.py
│   │
│   ├── db/                       # Database
│   │   ├── session.py           # SQLAlchemy setup
│   │   └── __init__.py
│   │
│   ├── main.py                   # FastAPI app entry point
│   ├── consumer.py               # Consumer service entry point
│   └── __init__.py
│
├── docker/
│   ├── fastapi.Dockerfile       # FastAPI service image
│   └── consumer.Dockerfile      # Consumer service image
│
├── requirements.txt              # Python dependencies
└── docker-compose.yml            # Docker Compose setup (at root)
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ (for local development)
- Git

### Running with Docker Compose

```bash
# Clone the repository
git clone https://github.com/atulpanday44/AI-Powered-Incident-Management-System.git
cd AI-Powered-Incident-Management-System

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- FastAPI: `http://localhost:8000`
- Kafka: `localhost:9092`
- PostgreSQL: `localhost:5432`

### Local Development Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables (create .env file)
cat > .env << EOF
DATABASE_URL=postgresql://incident_user:incident_password@localhost:5432/incident_db
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
LOG_LEVEL=INFO
EOF

# Start FastAPI (in one terminal)
python -m uvicorn app.main:app --reload

# Start Consumer (in another terminal)
python -m app.consumer
```

## 📡 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Ingest Logs

```bash
curl -X POST http://localhost:8000/api/v1/logs \
  -H "Content-Type: application/json" \
  -d '{
    "service": "auth-service",
    "level": "ERROR",
    "message": "Database connection failed",
    "timestamp": "2024-04-25T10:30:00"
  }'
```

### Get Logs

```bash
curl http://localhost:8000/api/v1/logs?service=auth-service&limit=10

# With filtering
curl "http://localhost:8000/api/v1/logs?service=auth-service&level=ERROR"
```

### Get Specific Log

```bash
curl http://localhost:8000/api/v1/logs/{log_id}
```

### Create Incident

```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "High Error Rate in Auth Service",
    "service": "auth-service",
    "severity": "HIGH",
    "cluster_id": "cluster_1",
    "anomaly_score": 3.2
  }'
```

### Get Incidents

```bash
curl http://localhost:8000/api/v1/incidents
curl "http://localhost:8000/api/v1/incidents?status=OPEN&severity=HIGH"
```

### Update Incident

```bash
curl -X PATCH http://localhost:8000/api/v1/incidents/{incident_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "RESOLVED",
    "severity": "MEDIUM"
  }'
```

### Get Statistics

```bash
curl http://localhost:8000/api/v1/incidents-summary
```

## 🔄 Kafka Event Flow

The consumer processes logs through the following pipeline:

1. **Consume**: Read log from Kafka topic `logs-topic`
2. **Store**: Save log to PostgreSQL
3. **Detect Anomalies**: Statistical analysis (Z-score) for error spikes
4. **Cluster**: Group similar logs using TF-IDF + Cosine Similarity
5. **Deduplicate**: Check if similar incident exists in time window
6. **Classify**: Determine severity based on rules
7. **Create/Update**: Add new or update existing incident in database

```
Log Consumed from Kafka
       ▼
Store in PostgreSQL
       ▼
┌──────────────────────────────────┐
│  Run AI Analysis                 │
├──────────────────────────────────┤
│ 1. Anomaly Detection (Z-score)   │
│ 2. Log Clustering (TF-IDF)       │
│ 3. Deduplication Check           │
└──────────────────────────────────┘
       ▼
Classify Severity (Rule-based)
       ▼
Create or Update Incident
       ▼
Store in Database
```

## 🤖 AI/ML Features

### Anomaly Detection

- **Method**: Z-score based statistical analysis
- **Window**: Tracks last 100 logs per service
- **Threshold**: Default 2.0 (configurable)
- **Detection**: Identifies spikes in ERROR/CRITICAL frequency

```python
# Example configuration
ANOMALY_DETECTION_THRESHOLD=2.0
ANOMALY_WINDOW_SIZE=100
```

### Log Clustering

- **Method**: TF-IDF + Cosine Similarity
- **Approach**: Groups similar error messages
- **Threshold**: Default 0.7 similarity score
- **Output**: Cluster ID for grouping related logs

```python
# Example configuration
CLUSTERING_SIMILARITY_THRESHOLD=0.7
```

### Incident Deduplication

- **Window**: Default 5 minutes (300 seconds)
- **Approach**: Normalized message hash + cluster matching
- **Benefit**: Prevents duplicate incident creation

```python
# Example configuration
DEDUPLICATION_TIME_WINDOW=300
```

### Severity Classification

Rule-based system:

| Condition | Severity |
|-----------|----------|
| CRITICAL level OR "critical"/"panic"/"crash" keywords | CRITICAL |
| ERROR level + anomaly detected | HIGH |
| ERROR level + error keywords | HIGH |
| WARNING level | MEDIUM |
| INFO level or lower | LOW |

## 🗄️ Database Schema

### logs table

```sql
CREATE TABLE logs (
    id UUID PRIMARY KEY,
    message VARCHAR(2048) NOT NULL,
    level VARCHAR(20) NOT NULL,
    service VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_logs_service ON logs(service);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_timestamp ON logs(timestamp);
```

### incidents table

```sql
CREATE TABLE incidents (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    service VARCHAR(255) NOT NULL,
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    status ENUM('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED') NOT NULL,
    cluster_id VARCHAR(255),
    anomaly_score FLOAT,
    log_count INTEGER DEFAULT 1,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_incidents_service ON incidents(service);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_created_at ON incidents(created_at);
```

## ⚙️ Configuration

All configuration is managed through environment variables:

```bash
# FastAPI
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/incident_db
SQLALCHEMY_ECHO=false

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_LOGS_TOPIC=logs-topic
KAFKA_INCIDENTS_TOPIC=incidents-topic
KAFKA_CONSUMER_GROUP=incident-processor

# Logging
LOG_LEVEL=INFO

# AI/ML Features
ENABLE_ANOMALY_DETECTION=true
ENABLE_CLUSTERING=true
ANOMALY_DETECTION_THRESHOLD=2.0
CLUSTERING_SIMILARITY_THRESHOLD=0.7
ANOMALY_WINDOW_SIZE=100
DEDUPLICATION_TIME_WINDOW=300
```

## 📊 Logging

Structured JSON logging for all components:

```json
{
  "timestamp": "2024-04-25T10:30:00.123456",
  "level": "INFO",
  "logger": "incident_manager.api.logs",
  "message": "Log ingested successfully",
  "log_id": "550e8400-e29b-41d4-a716-446655440000",
  "service": "auth-service",
  "level": "ERROR"
}
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app

# Run specific test file
pytest tests/test_anomaly_detection.py -v
```

## 🔒 Production Deployment

For production deployment:

1. **Use environment variables** for all secrets
2. **Configure database backups** and replication
3. **Set up Kafka replication factor > 1**
4. **Enable authentication** for Kafka and PostgreSQL
5. **Use load balancer** for FastAPI service
6. **Configure monitoring** (Prometheus, Grafana)
7. **Set up alerting** for incident thresholds
8. **Use proper secrets management** (Vault, AWS Secrets Manager)

```yaml
# Production docker-compose adjustments
kafka:
  environment:
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
    KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3

postgres:
  volumes:
    - postgres_backup:/backups
  command: >
    postgres -c wal_level=replica
```

## 📈 Performance Metrics

Expected performance characteristics:

- **Log Ingestion**: ~1000 logs/second per FastAPI instance
- **Kafka Processing**: Sub-second latency for consumer
- **Database**: <50ms p95 latency for queries
- **Anomaly Detection**: O(1) per log with rolling window
- **Clustering**: O(n) where n = cluster count

## 🐛 Debugging

### View logs from specific service

```bash
# FastAPI service logs
docker-compose logs fastapi -f

# Consumer service logs
docker-compose logs consumer -f

# Kafka logs
docker-compose logs kafka -f

# PostgreSQL logs
docker-compose logs postgres -f
```

### Connect to database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U incident_user -d incident_db

# List tables
\dt

# Check logs table
SELECT COUNT(*) FROM logs;
SELECT COUNT(*) FROM incidents;
```

### Kafka debugging

```bash
# List topics
docker-compose exec kafka kafka-topics.sh --list --bootstrap-server kafka:9092

# View consumer group status
docker-compose exec kafka kafka-consumer-groups.sh --group incident-processor --bootstrap-server kafka:9092 --describe

# Check topic offsets
docker-compose exec kafka kafka-run-class.sh kafka.tools.JmxTool --object-name kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
```

## 📝 License

MIT License - see LICENSE file for details

## 👤 Author

AI Incident Management Team

## 🤝 Contributing

1. Create a feature branch
2. Commit changes
3. Push to remote
4. Create pull request

## 📞 Support

For issues and questions, open an issue on GitHub.
