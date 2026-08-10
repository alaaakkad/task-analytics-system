from fastapi import FastAPI
import os
import redis
import psycopg2

app = FastAPI()

# Connect to Redis using the service name from Docker Compose
cache = redis.Redis(host='cache_redis', port=6379, decode_responses=True)

@app.get("/")
def read_root():
    # 1. Increment the visit counter in Redis cache
    visits = cache.incr("counter")
    
    # 2. Test the connection to PostgreSQL using credentials from .env
    db_status = "Success and Connected ✅"
    try:
        conn = psycopg2.connect(
            host="postgres_db",
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        conn.close()
    except Exception as e:
        db_status = f"Failed ❌ (Reason: {e})"

    return {
        "message": "Welcome to the Distributed Task Analytics System!",
        "visit_count": f"This page has been visited {visits} times.",
        "database_connection": db_status
    }

