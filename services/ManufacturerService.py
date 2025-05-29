from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Manufacturer

class ManufacturerType(TypedDict):
    name: Optional[str] = None

class ManufacturerService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:ManufacturerType):
        manufacturerModel = Manufacturer(
            name=data["name"]
        )

        self.__db.add(manufacturerModel)
        self.__db.commit()
        self.__db.refresh(manufacturerModel)

        return manufacturerModel

    def update(self, data:ManufacturerType, manufacturer:Manufacturer):
        if "name" in data and data["name"] is not None: manufacturer.name = data["name"]

        self.__db.commit()
        self.__db.refresh(manufacturer)

        return manufacturer

    def getManufacturers(self):
        return self.__db.query(Manufacturer).all()

    def getManufacturer(self, id):
        return self.__db.query(Manufacturer).filter(Manufacturer.id == id).first()

    def getManufacturerByName(self, name):
        return self.__db.query(Manufacturer).filter(Manufacturer.name == name).first()
