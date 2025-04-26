from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Station

class StationType(TypedDict):
    name: Optional[str] = None
    identifier: Optional[str] = None
    voltageLevel: Optional[float] = None
    display: Optional[bool] = None
    x: Optional[int] = None
    y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None

class StationService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:StationType):
        print(data)
        stationModel = Station(
            name=data["name"],
            identifier=data["identifier"],
            voltage_level=data.get("voltageLevel"),
            display=data.get("display")
        )

        self.__db.add(stationModel)
        self.__db.commit()
        self.__db.refresh(stationModel)

        return stationModel

    def update(self, data:StationType, station:Station):
        if "name" in data and data["name"] is not None: station.name = data["name"]
        if "identifier" in data and data["identifier"] is not None: station.identifier = data["identifier"]
        if "display" in data and data["display"] is not None: station.display = data["display"]
        if "voltageLevel" in data and data["voltageLevel"] is not None: station.voltage_level = data["voltageLevel"]
        if "x" in data and data["x"] is not None: station.x = data["x"]
        if "y" in data and data["y"] is not None: station.y = data["y"]
        if "width" in data and data["width"] is not None: station.width = data["width"]
        if "height" in data and data["height"] is not None: station.height = data["height"]

        self.__db.commit()
        self.__db.refresh(station)

        return station

    def getStations(self, display=False):
        query = self.__db.query(Station)
        if(display): query = query.filter(Station.display == True)

        return query.all()

    def getStation(self, identifier):
        return self.__db.query(Station).filter(Station.identifier == identifier).first()
