from middlewares.DbMiddleware import DB
from typing import TypedDict, Optional
from models import Connection

class ConnectionType(TypedDict):
    identifier: Optional[str] = None
    fromStationId: Optional[int] = None
    fromLineId: Optional[int] = None
    fromSide: Optional[str] = None
    toStationId: Optional[int] = None
    toLineId: Optional[int] = None
    toSide: Optional[str] = None

class ConnectionService:

    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:ConnectionType):
        ConnectionModel = Connection(
            identifier=data["identifier"],
            from_station_id=data["fromStationId"],
            from_line_id=data["fromLineId"],
            from_side=data.get("fromSide"),
            to_station_id=data["toStationId"],
            to_line_id=data["toLineId"],
            to_side=data.get("toSide"),
        )

        self.__db.add(ConnectionModel)
        self.__db.commit()
        self.__db.refresh(ConnectionModel)

        return ConnectionModel

    def update(self, data:ConnectionType, connection:Connection):
        if "identifier" in data and data["identifier"] is not None: connection.identifier = data["identifier"]
        if "fromStationId" in data and data["fromStationId"] is not None: connection.from_station_id = data["fromStationId"]
        if "fromLineId" in data and data["fromLineId"] is not None: connection.from_line_id = data["fromLineId"]
        if "fromSide" in data and data["fromSide"] is not None: connection.from_side = data["fromSide"]
        if "toStationId" in data and data["toStationId"] is not None: connection.to_station_id = data["toStationId"]
        if "toLineId" in data and data["toLineId"] is not None: connection.to_line_id = data["toLineId"]
        if "toSide" in data and data["toSide"] is not None: connection.to_side = data["toSide"]

        self.__db.commit()
        self.__db.refresh(connection)

        return connection

    def getConnections(self, display=False):
        query = self.__db.query(Connection)
        if display:
            query.filter(Connection.display == True)

        return query.all()

    def getConnection(self, identifier):
        return self.__db.query(Connection).filter(Connection.identifier == identifier).first()
