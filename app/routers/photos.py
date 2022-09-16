from typing import Union
from app.cache import PhotoCoder
from app.utils.settings import Settings
from app.utils.algos import nearest_divisor
from app.utils.aiohttpsingleton import SingletonAiohttp

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from fastapi import HTTPException


router = APIRouter()


@router.get("/photos", tags=["photos"])
@cache(expire=30*60, coder=PhotoCoder)
async def photos_list(limit: Union[int, None] = 50, offset: Union[int, None] = 0):
    """
    :param limit: Total photos number that will be returned. Default: 50\n
    :param offset: Offset of looking images. Default: 0\n
    :return: Json list with tuples: (id, description, url) of regular image
    """
    params = {
        "client_id": Settings.AUTH_TOKEN,
    }
    start, end = 0, limit
    if limit >= offset:
        params['per_page'] = limit + offset
        params['page'] = 1
        start = offset
        end = params['per_page']
    else:
        params['per_page'] = nearest_divisor(offset, limit)
        params['page'] = int(offset/params['per_page']) + 1

    result, headers = await SingletonAiohttp.query_url(Settings.MAIN_URL, params=params)
    if headers.get("ERROR", ""):
        return HTTPException(status_code=502, detail=f"Problem with main server: '{headers['ERROR']}'")

    result = [{
        "id": info["id"],
        "description": info["description"] or info["alt_description"] or "",
        "image": info["urls"]["regular"]
    }for info in result[start:end]]

    headers = {'X-Total': headers['X-Total']}
    return JSONResponse(content=result, headers=headers)
