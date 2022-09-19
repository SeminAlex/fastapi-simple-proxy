from asyncio import gather
from app.utils.settings import Settings
from app.utils.aiohttpsingleton import SingletonAiohttp

from fastapi import HTTPException
from fastapi.responses import JSONResponse


def page_offset_generator(offset: int, total: int, max_limit: int):
    def generator(start, stop):
        for i in range(start, stop):
            yield i
    real_offset = offset % max_limit
    page_num = round(float(total) / max_limit + 0.5)
    begin = int(offset / max_limit)
    return real_offset, generator(begin, begin + page_num)


async def collect_images(limit: int, offset: int):
    params = {
        "client_id": Settings.AUTH_TOKEN,
        "per_page": Settings.MAX_OBJECTS_LIMIT
    }
    offset, page_gen = page_offset_generator(offset, limit, params["per_page"])
    async_calls = list()
    for page in page_gen:
        params["page"] = page
        async_calls.append(SingletonAiohttp.query_url(Settings.MAIN_URL, params=params))

    all_results = await gather(*async_calls)  # wait for all async operations
    result = list()
    for json_list, headers in all_results:
        if headers.get("ERROR", ""):
            return HTTPException(status_code=502, detail=f"Problem with main server: '{headers['ERROR']}'")
        result.extend(json_list)
    result = [{
        "id": info["id"],
        "description": info["description"] or info["alt_description"] or "",
        "image": info["urls"]["regular"]
    } for info in result[offset:limit + offset]]

    headers = {'X-Total': all_results[0][1]['X-Total']}
    return JSONResponse(content=result, headers=headers)
