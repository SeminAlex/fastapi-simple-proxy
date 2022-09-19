from typing import Union
from app.cache import PhotoCoder
from app.utils.algos import collect_images

from fastapi import APIRouter
from fastapi_cache.decorator import cache


router = APIRouter()


@router.get("/photos", tags=["photos"])
@cache(expire=30*60, coder=PhotoCoder)
async def photos_list(limit: Union[int, None] = 50, offset: Union[int, None] = 0):
    """
    :param limit: Total photos number that will be returned. Default: 50\n
    :param offset: Offset of looking images. Default: 0\n
    :return: Json list with tuples: (id, description, url) of regular image
    """
    offset = 0 if offset < 0 else offset
    limit = 0 if limit < 0 else limit
    return await collect_images(limit, offset)

