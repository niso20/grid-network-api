from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import List
from middlewares.DbMiddleware import DB
from resources.ConnectionResource import ConnectionResource
from requests.ConnectionRequest import CreateConnection, UpdateConnection
from services.ConnectionService import ConnectionService

router = APIRouter(
    prefix='/connections',
    tags=['connections']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[ConnectionResource], response_model_by_alias=False)
async def get_all(db: DB):
    connectionService = ConnectionService(db)
    connections = connectionService.getConnections()

    return connections

@router.get("/displayed", status_code=status.HTTP_200_OK, response_model=List[ConnectionResource], response_model_by_alias=False)
async def get_displayed(db: DB):
    connectionService = ConnectionService(db)
    connections = connectionService.getConnections(True)

    return connections

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: CreateConnection):
    connectionService = ConnectionService(db)
    data = createRequest.model_dump()

    exists = connectionService.getConnection(data["identifier"])

    if(exists):
        raise HTTPException(status_code=400, detail="Identifier must be unique")

    connectionService.save(data)


@router.put("/{identifier}", status_code=status.HTTP_201_CREATED)
async def save(db: DB, updateRequest: UpdateConnection, identifier: str = Path()):
    connectionService = ConnectionService(db)
    data = updateRequest.model_dump()

    connection = connectionService.getConnection(identifier)

    if connection:
        ConnectionService.update(data, connection)
    else:
        if (
                "identifier" in data and data["identifier"] is not None
                and
                "fromStationId" in data and data["fromStationId"] is not None
                and
                "fromLineId" in data and data["fromLineId"] is not None
                and
                "toStationId" in data and data["toStationId"] is not None
                and
                "toLineId" in data and data["toLineId"] is not None
        ):
            connectionService.save(data)
        else:
            raise HTTPException(status_code=400, detail="Connection does not exist")
