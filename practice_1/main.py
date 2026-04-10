from fastapi import FastAPI, HTTPException

from models import Hackathon, Organizer
from temp_db import temp_hackathons, temp_organizers

app = FastAPI(title="Hackathon Management API")


@app.get("/")
def root():
    return {"message": "Hackathon Management API is running"}


# API для главной сущности: Hackathon

@app.get("/hackathons", response_model=list[Hackathon])
def get_hackathons():
    return temp_hackathons


@app.get("/hackathons/{hackathon_id}", response_model=Hackathon)
def get_hackathon(hackathon_id: int):
    for hackathon in temp_hackathons:
        if hackathon["id"] == hackathon_id:
            return hackathon
    raise HTTPException(status_code=404, detail="Hackathon not found")


@app.post("/hackathons", response_model=Hackathon, status_code=201)
def create_hackathon(hackathon: Hackathon):
    for item in temp_hackathons:
        if item["id"] == hackathon.id:
            raise HTTPException(status_code=400, detail="Hackathon with this id already exists")

    hackathon_data = hackathon.model_dump(mode="json")
    temp_hackathons.append(hackathon_data)
    return hackathon_data


@app.put("/hackathons/{hackathon_id}", response_model=Hackathon)
def update_hackathon(hackathon_id: int, hackathon: Hackathon):
    for index, item in enumerate(temp_hackathons):
        if item["id"] == hackathon_id:
            updated_data = hackathon.model_dump(mode="json")
            temp_hackathons[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Hackathon not found")


@app.delete("/hackathons/{hackathon_id}")
def delete_hackathon(hackathon_id: int):
    for index, item in enumerate(temp_hackathons):
        if item["id"] == hackathon_id:
            temp_hackathons.pop(index)
            return {"message": "Hackathon deleted"}
    raise HTTPException(status_code=404, detail="Hackathon not found")


# API для вложенного объекта: Organizer

@app.get("/organizers", response_model=list[Organizer])
def get_organizers():
    return temp_organizers


@app.get("/organizers/{organizer_id}", response_model=Organizer)
def get_organizer(organizer_id: int):
    for organizer in temp_organizers:
        if organizer["id"] == organizer_id:
            return organizer
    raise HTTPException(status_code=404, detail="Organizer not found")


@app.post("/organizers", response_model=Organizer, status_code=201)
def create_organizer(organizer: Organizer):
    for item in temp_organizers:
        if item["id"] == organizer.id:
            raise HTTPException(status_code=400, detail="Organizer with this id already exists")

    organizer_data = organizer.model_dump(mode="json")
    temp_organizers.append(organizer_data)
    return organizer_data


@app.put("/organizers/{organizer_id}", response_model=Organizer)
def update_organizer(organizer_id: int, organizer: Organizer):
    for index, item in enumerate(temp_organizers):
        if item["id"] == organizer_id:
            organizer_data = organizer.model_dump(mode="json")
            temp_organizers[index] = organizer_data

            # Обновим вложенного организатора внутри всех хакатонов
            for hackathon in temp_hackathons:
                if hackathon["organizer"]["id"] == organizer_id:
                    hackathon["organizer"] = organizer_data

            return organizer_data

    raise HTTPException(status_code=404, detail="Organizer not found")