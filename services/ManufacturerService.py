from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Transformer

class TransformerType(TypedDict):
    name: Optional[str] = None
    manufacturerId: Optional[int] = None
    serialNo: Optional[str] = None
    powerRating: Optional[int] = None
    powerRatingUnit: Optional[str] = None
    typeOfCooling: Optional[str] = None
    voltageRating: Optional[str] = None
    manufactureYear: Optional[int] = None
    installationYear: Optional[int] = None
    stationId: Optional[int] = None

class TransformerService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:TransformerType):
        transformerModel = Transformer(
            name=data["name"],
            manufacturer_id=data["manufacturerId"],
            serial_no=data.get("serialNo"),
            power_rating=data["powerRating"],
            power_rating_unit=data["powerRatingUnit"],
            type_of_cooling=data.get("typeOfCooling"),
            voltage_rating=data["voltageRating"],
            manufacture_year=data.get("manufactureYear"),
            installation_year=data.get("installationYear"),
            station_id=data["stationId"]
        )

        self.__db.add(transformerModel)
        self.__db.commit()
        self.__db.refresh(transformerModel)

        return transformerModel

    def update(self, data:TransformerType, transformer:Transformer):
        if "name" in data and data["name"] is not None: transformer.name = data["name"]
        if "manufacturerId" in data and data["manufacturerId"] is not None: transformer.manufacturer_id = data["manufacturerId"]
        if "serialNo" in data and data["serialNo"] is not None: transformer.serial_no = data["serialNo"]
        if "powerRating" in data and data["powerRating"] is not None: transformer.power_rating = data["powerRating"]
        if "powerRatingUnit" in data and data["powerRatingUnit"] is not None: transformer.power_rating_unit = data["powerRatingUnit"]
        if "typeOfCooling" in data and data["typeOfCooling"] is not None: transformer.type_of_cooling = data["typeOfCooling"]
        if "voltageRating" in data and data["voltageRating"] is not None: transformer.voltage_rating = data["voltageRating"]
        if "manufactureYear" in data and data["manufactureYear"] is not None: transformer.manufacture_year = data["manufactureYear"]
        if "installationYear" in data and data["installationYear"] is not None: transformer.installation_year = data["installationYear"]
        if "stationId" in data and data["stationId"] is not None: transformer.station_id = data["stationId"]

        self.__db.commit()
        self.__db.refresh(transformer)

        return transformer

    def getTransformers(self):
        return self.__db.query(Transformer).all()

    def getTransformer(self, id):
        return self.__db.query(Transformer).filter(Transformer.id == id).first()

    def getTransformerByName(self, name):
        return self.__db.query(Transformer).filter(Transformer.name == name).first()
