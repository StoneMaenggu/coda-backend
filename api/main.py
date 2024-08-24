from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import login, user, group, post, reaction, image

app = FastAPI()
app.include_router(login.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(post.router)
app.include_router(reaction.router)
app.include_router(image.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)