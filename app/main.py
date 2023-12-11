from fastapi import FastAPI
from .models import models as model
from .db.config import engine
from .routes import blog, user, auth
from .environment.config import Settings

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)


@app.get("")
def root():
    return {"message": "Hello World"}