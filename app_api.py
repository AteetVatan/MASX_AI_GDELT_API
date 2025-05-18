from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import json
import uvicorn

# Rate limiter imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from gdeltdoc import GdeltDoc, Filters
from model import ArticleSearchRequest, TimelineRequest
from configs import MainConfigs
from helpers.validators import Validators

# Create FastAPI app in main scope
with open("project_metadata.json", "r", encoding="utf-8") as f:
    METADATA = json.load(f)

app = FastAPI(**METADATA["project_metadata"])


# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# GDELT client
GDELT_CLIENT = GdeltDoc()

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """Verify API key"""
    system_api_key = MainConfigs.get_api_key()
    if system_api_key:
        if not x_api_key or x_api_key != system_api_key:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key")
    

@app.get("/", tags=["System"])
@limiter.limit("60/minute")
def read_root(request: Request):
    """API metadata"""
    METADATA["api_metadata"]["timestamp"] = datetime.utcnow().isoformat()
    return {
        **METADATA["api_metadata"]
    }


@app.post("/api/articles", tags=["Search"], dependencies=[Depends(verify_api_key)])
@limiter.limit("60/minute")
async def search_articles(req: ArticleSearchRequest, request: Request):
    try:
        start_date, end_date = Validators.get_and_validate_date_range(
            req.start_date, req.end_date
        )
        filters = Filters(
            keyword=req.keyword,
            start_date=start_date,
            end_date=end_date,
            domain=req.domain,
            country=req.country,
            language=req.language,
            max_records=req.maxrecords if req.maxrecords else 100
        )
        articles = GDELT_CLIENT.article_search(filters)
        return JSONResponse(content=articles)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/timeline", tags=["Timeline"], dependencies=[Depends(verify_api_key)])
@limiter.limit("60/minute")
async def search_timeline(req: TimelineRequest, request: Request):
    """Search timeline"""
    try:
        valid_modes = [
            "timelinevol", "timelinevolraw", "timelinetone",
            "timelinelang", "timelinesourcecountry"
        ]
        if req.mode not in valid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid mode. Must be one of: {', '.join(valid_modes)}"
            )

        start_date, end_date = Validators.get_and_validate_date_range(
            req.start_date, req.end_date
        )

        filters = Filters(
            keyword=req.keyword,
            start_date=start_date,
            end_date=end_date,
            domain=req.domain,
            country=req.country,
            language=req.language,
        )

        timeline_data = GDELT_CLIENT.timeline_search(req.mode, filters)

        if timeline_data.empty:
            return []

        timeline_data["datetime"] = timeline_data["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        return timeline_data.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    run_config = MainConfigs.get_run_config()
    uvicorn.run("app_api:app", **run_config)
