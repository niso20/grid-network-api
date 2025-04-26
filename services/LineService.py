from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Line

class LineType(TypedDict):
    name: Optional[str] = None
    identifier: Optional[str] = None
    voltageLevel: Optional[float] = None
    stationId: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

class LineService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:LineType):
        lineModel = Line(
            name=data["name"],
            identifier=data["identifier"],
            station_id=data["stationId"],
            voltage_level=data.get("voltageLevel")
        )

        self.__db.add(lineModel)
        self.__db.commit()
        self.__db.refresh(lineModel)

        return lineModel

    def update(self, data:LineType, line:Line):
        if "name" in data and data["name"] is not None: line.name = data["name"]
        if "identifier" in data and data["identifier"] is not None: line.identifier = data["identifier"]
        if "voltageLevel" in data and data["voltageLevel"] is not None: line.voltage_level = data["voltageLevel"]
        if "x" in data and data["x"] is not None: line.x = data["x"]
        if "y" in data and data["y"] is not None: line.y = data["y"]
        if "stationId" in data and data["stationId"] is not None: line.station_id = data["stationId"]

        self.__db.commit()
        self.__db.refresh(line)

        return line

    def getLines(self):
        return self.__db.query(Line).all()

    def getLine(self, identifier, stationId):
        return self.__db.query(Line).filter(Line.station_id == stationId).filter(Line.identifier == identifier).first()
