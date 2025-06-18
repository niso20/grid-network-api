from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Unit

class UnitType(TypedDict):
    name: Optional[str] = None
    identifier: Optional[str] = None
    voltageLevel: Optional[float] = None
    stationId: Optional[int] = None
    inertia: Optional[float] = None
    active: Optional[bool] = None

class UnitService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:UnitType):
        unitModel = Unit(
            name=data["name"],
            identifier=data["identifier"],
            station_id=data["stationId"],
            voltage_level=data.get("voltageLevel"),
            inertia = data["inertia"],
            active=data.get("active"),
        )

        self.__db.add(unitModel)
        self.__db.commit()
        self.__db.refresh(unitModel)

        return unitModel

    def update(self, data:UnitType, unit:Unit):
        if "name" in data and data["name"] is not None: unit.name = data["name"]
        if "identifier" in data and data["identifier"] is not None: unit.identifier = data["identifier"]
        if "voltageLevel" in data and data["voltageLevel"] is not None: unit.voltage_level = data["voltageLevel"]
        if "inertia" in data and data["inertia"] is not None: unit.inertia = data["inertia"]
        if "active" in data and data["active"] is not None: unit.active = data["active"]
        if "stationId" in data and data["stationId"] is not None: unit.station_id = data["stationId"]

        self.__db.commit()
        self.__db.refresh(unit)

        return unit

    def getUnits(self):
        return self.__db.query(Unit).all()

    def getUnit(self, identifier, stationId):
        return self.__db.query(Unit).filter(Unit.station_id == stationId).filter(Unit.identifier == identifier).first()

    def getUnitById(self, id):
        return self.__db.query(Unit).filter(Unit.id == id).first()
