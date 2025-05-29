from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import List
from middlewares.DbMiddleware import DB
from resources.ManufacturerResource import ManufacturerResource
from requests.ManufacturerRequest import SaveManufacturer, UpdateManufacturer
from services.ManufacturerService import ManufacturerService

router = APIRouter(
    prefix='/manufacturers',
    tags=['manufacturers']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[ManufacturerResource], response_model_by_alias=False)
async def get_all(db: DB):
    manufacturerService = ManufacturerService(db)
    manufacturers = manufacturerService.getManufacturers()

    return manufacturers

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ManufacturerResource, response_model_by_alias=False)
async def get_one(db: DB, id: int = Path()):
    manufacturerService = ManufacturerService(db)
    manufacturer = manufacturerService.getManufacturer(id)

    if not manufacturer:
        raise HTTPException(status_code=400, detail="Manufacturer does not exist")

    return manufacturer

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: SaveManufacturer):
    manufacturerService = ManufacturerService(db)
    data = createRequest.model_dump()

    exists = manufacturerService.getManufacturerByName(data["name"])

    if(exists):
        raise HTTPException(status_code=400, detail="Manufacturer exists")

    manufacturerService.save(data)


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def save(db: DB, updateRequest: UpdateManufacturer, id: int = Path()):
    manufacturerService = ManufacturerService(db)
    data = updateRequest.model_dump()

    manufacturer = manufacturerService.getManufacturer(id)

    if manufacturer:
        manufacturerService.update(data, manufacturer)
    else:
        raise HTTPException(status_code=400, detail="Manufacturer does not exist")
