import json
from typing import Any

from fastapi_cache.coder import JsonCoder
from fastapi.responses import JSONResponse


class PhotoCoder(JsonCoder):
    @classmethod
    def decode(cls, value: Any):
        result = super().decode(value=value)
        if result["status_code"] == 200:
            return JSONResponse(content=json.loads(result["body"]), headers=dict(result["raw_headers"]))
        return result
