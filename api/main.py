from fastapi import FastAPI
from api.routers import login, user, group, post, reaction

app = FastAPI()
app.include_router(login.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(post.router)
app.include_router(reaction.router)