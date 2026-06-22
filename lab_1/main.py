from fastapi import FastAPI

from routers import auth, hackathons, organizers, participants, tasks

app = FastAPI(title="Hackathon API")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hackathon API is running"}


app.include_router(auth.router)
app.include_router(organizers.router)
app.include_router(participants.router)
app.include_router(hackathons.router)
app.include_router(tasks.router)
