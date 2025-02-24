from fastapi import FastAPI
from game_server.routers import post_router, user_router, comment_router
from game_server.configs import engine
from game_server.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(post_router.router, prefix="/posts", tags=["posts"])
app.include_router(comment_router.router, prefix="/comments", tags=["comments"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
