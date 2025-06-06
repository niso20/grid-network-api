from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import List
from typing_extensions import TypedDict, Optional
from middlewares.DbMiddleware import DB
from services.FrequencyService import FrequencyService
from resources.RocofResource import RocofResource


router = APIRouter(prefix='/frequency', tags=['frequency'])

class FrequencyType(TypedDict):
    f: Optional[float] = None
    t: Optional[str] = None
    df: Optional[float] = None
    dt: Optional[float] = None
    rocof: Optional[float] = None

@router.get('/rocof_series', status_code=status.HTTP_200_OK, response_model=List[RocofResource])
async def rocofSeries(db: DB):
    frequencyService = FrequencyService(db)
    rocofs = frequencyService.getRocof()

    return rocofs

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, data: FrequencyType):
    frequencyService = FrequencyService(db)

    frequencyService.save(data)




