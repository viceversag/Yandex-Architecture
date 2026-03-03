from fastapi import FastAPI
import random

# Create a FastAPI instance, which is the main point of interaction for creating the API
app = FastAPI()

# Define a "path operation" using the @app.get("/") decorator
@app.get("/")
def read_root():
    """
    Function to handle GET requests to the root URL (/).
    It returns a simple JSON response.
    """
    return {"Hello": "World"}

# Another path operation with a path parameter and an optional query parameter
@app.get("/temperature")
def read_item(location: int | None = None):
    """
    Function to handle GET requests to /temperature .
    It takes location as a named parameter and returns random number to location number
    """
    return {"location": random.random() * 10}