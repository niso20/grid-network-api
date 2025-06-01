from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Station
from typing import List
from middlewares.DbMiddleware import DB
from middlewares.UserMiddleware import User, SuperAdminUser, AdminUser, ManagerUser, OperatorUser

from resources.StationResource import StationResource
from requests.StationRequest import CreateStation, UpdateStation
from services.StationService import StationService
from services.LineService import LineService
from enums.Role import Role
import collections.abc

router = APIRouter(
    prefix='/stations',
    tags=['station']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[StationResource], response_model_by_alias=False)
async def get_all(db: DB, currentUser: ManagerUser):
    stationService = StationService(db)
    # stations = db.query(Station).all()
    stations = stationService.getStations()

    # stations_response = [StationResource.model_validate(station, from_attributes=True).model_dump(by_alias=True) for
    #                      station in stations]

    # test this manually
    # test_output = StationResource.model_validate(stations[0], from_attributes=True).model_dump(by_alias=True)
    # print(test_output)  # 👀 see what's going on in your console

    return stations

@router.get("/displayed", status_code=status.HTTP_200_OK, response_model=List[StationResource], response_model_by_alias=False)
async def get_displayed(db: DB):
    stationService = StationService(db)
    stations = stationService.getStations(True)

    return stations

@router.get("/{identifier}", status_code=status.HTTP_200_OK, response_model=StationResource, response_model_by_alias=False)
async def get_station(db: DB, identifier: str = Path()):
    stationService = StationService(db)
    station = stationService.getStation(identifier)

    if not station:
        raise HTTPException(status_code=400, detail="Station does not exist")

    return station

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: CreateStation):
    stationService = StationService(db)
    data = createRequest.model_dump()

    exists = stationService.getStation(createRequest.identifier)

    if(exists):
        raise HTTPException(status_code=400, detail="Identifier must be unique")

    stationService.save(data)


@router.put("/{identifier}", status_code=status.HTTP_201_CREATED)
async def update(db: DB, updateRequest: UpdateStation, identifier: str = Path()):
    stationService = StationService(db)
    lineService = LineService(db)
    data = updateRequest.model_dump()

    station = stationService.getStation(identifier)

    #if Station exists
    if station:
        # Update the station
        stationService.update(data, station)

        # if lines are passed in the request data
        if "lines" in data and data["lines"] is not None:
            print("lines", data["lines"])
            if isinstance(data["lines"], collections.abc.Iterable):
                for lineData in data["lines"]:
                    if (
                            "name" in lineData and lineData["name"] is not None
                            and
                            "id" in lineData and lineData["id"] is not None
                    ):
                        lineData["identifier"] = lineData["id"]
                        lineData["stationId"] = station.id
                        line = lineService.getLine(lineData["identifier"], station.id)
                        if line:
                            lineService.update(lineData, line)
                        else:
                            lineService.save(lineData)

    else:
        if (
                "name" in data and data["name"] is not None
                and
                "identifier" in data and data["identifier"] is not None
        ):
            station = stationService.save(data)
            if "lines" in data and data["lines"] is not None:
                if isinstance(data["lines"], collections.abc.Iterable):
                    for line in data["lines"]:
                        line['stationId'] = station.id
                        line['identifier'] = line['id']
                        lineService.save(line)
        else:
            raise HTTPException(status_code=400, detail="Station does not exist")
