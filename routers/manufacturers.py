from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import List
from middlewares.DbMiddleware import DB
from resources.TransformerResource import TransformerResource
from requests.TransformerRequest import SaveTransformer, UpdateTransformer
from services.TransformerService import TransformerService

router = APIRouter(
    prefix='/transformers',
    tags=['transformers']
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TransformerResource], response_model_by_alias=False)
async def get_all(db: DB):
    transformerService = TransformerService(db)
    transformers = transformerService.getTransformers()

    return transformers

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=TransformerResource, response_model_by_alias=False)
async def get_one(db: DB, id: int = Path()):
    transformerService = TransformerService(db)
    transformer = transformerService.getTransformer(id)

    if not transformer:
        raise HTTPException(status_code=400, detail="Transformer does not exist")

    return transformer

@router.post("", status_code=status.HTTP_201_CREATED)
async def save(db: DB, createRequest: SaveTransformer):
    transformerService = TransformerService(db)
    data = createRequest.model_dump()

    exists = transformerService.getTransformerByName(data["name"])

    if(exists):
        raise HTTPException(status_code=400, detail="Transformer exists")

    transformerService.save(data)


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def save(db: DB, updateRequest: UpdateTransformer, id: int = Path()):
    transformerService = TransformerService(db)
    data = updateRequest.model_dump()

    transformer = transformerService.getTransformer(id)

    if transformer:
        transformerService.update(data, transformer)
    else:
        raise HTTPException(status_code=400, detail="Transformer does not exist")
