from fastapi import FastAPI
from .models import models as model
from .db.config import engine
from .routes import blog, user, auth
from .environment.config import Settings

# Creating database tables based on the models using the engine
model.Base.metadata.create_all(bind=engine)

# Initializing the FastAPI application
app = FastAPI()

# Including routers for different components (user, blog, and authentication) in the FastAPI app
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)

# Root endpoint to handle HTTP GET requests to the base URL
@app.get("")
def root():
    # Returning a simple JSON response with a "Hello World" message
    return {"message": "Hello World"}
