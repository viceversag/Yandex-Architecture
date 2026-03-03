from fastapi import FastAPI, status
from confluent_kafka import Producer

app = FastAPI()


config = {
        "bootstrap.servers":"kafka:9092",
        "auto.offset.reset":"earliest"
    }


@app.get("/")
def read_root():
    return {"status":"OK"}

@app.get("/api/events/health", status_code = status.HTTP_200_OK)
def health():
    return {"status":True}

@app.post("/api/events/movie", status_code=status.HTTP_201_CREATED)
def send_movie():
    topic = "movie-events"
    producer = Producer(config)
    producer.produce(topic, value = "New movie added")
    producer.flush()
    return {"status":"success"}

@app.post("/api/events/user", status_code = status.HTTP_201_CREATED)
def send_user():
    topic = "user-events"
    producer = Producer(config)
    producer.produce(topic,"New user added")
    producer.flush()
    return {"status":"success"}

@app.post("/api/events/payment", status_code = status.HTTP_201_CREATED)
def send_payment():
    topic = "payment-events"
    producer = Producer(config)
    producer.produce(topic, "New payment added")
    producer.flush()
    return {"status":"success"}
