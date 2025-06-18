from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Station
from typing import List
from middlewares.DbMiddleware import DB
from resources.UnitResource import UnitResource
from requests.UnitRequest import CreateUnit, UpdateUnit
from services.UnitService import UnitService

router = APIRouter(
    prefix='/units',
    tags=['units']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UnitResource], response_model_by_alias=False)
async def get_all(db: DB):
    unitService = UnitService(db)
    units = unitService.getUnits()

    return units

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: CreateUnit):
    unitService = UnitService(db)
    data = createRequest.model_dump()

    exists = unitService.getUnit(data["identifier"], data["stationId"])

    if(exists):
        raise HTTPException(status_code=400, detail="Unit exists")

    unitService.save(data)


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def save(db: DB, updateRequest: UpdateUnit, id: int = Path()):
    unitService = UnitService(db)
    data = updateRequest.model_dump()

    unit = unitService.getUnitById(id)

    if unit:
        unitService.update(data, unit)
    else:
       raise HTTPException(status_code=400, detail="Unit does not exist")
