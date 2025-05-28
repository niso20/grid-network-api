from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Station
from typing import List
from middlewares.DbMiddleware import DB
from resources.LineResource import LineResource
from requests.LineRequest import CreateLine, UpdateLine
from services.LineService import LineService

router = APIRouter(
    prefix='/lines',
    tags=['lines']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[LineResource], response_model_by_alias=False)
async def get_all(db: DB):
    lineService = LineService(db)
    lines = lineService.getLines()

    return lines

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: CreateLine):
    lineService = LineService(db)
    data = createRequest.model_dump()

    exists = lineService.getLine(data["identifier"], data["stationId"])

    if(exists):
        raise HTTPException(status_code=400, detail="Line exists")

    lineService.save(data)


@router.put("/{identifier}", status_code=status.HTTP_201_CREATED)
async def save(db: DB, updateRequest: UpdateLine, identifier: str = Path()):
    lineService = LineService(db)
    data = updateRequest.model_dump()

    line = lineService.getLine(identifier)

    if line:
        lineService.update(data, line)
    else:
        if (
                "name" in data and data["name"] is not None
                and
                "identifier" in data and data["identifier"] is not None
        ):
            lineService.save(data)
        else:
            raise HTTPException(status_code=400, detail="Line does not exist")
