from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, release_conn
from app.queries import fetch_geojson_bbox

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "GIS API running 🚀"}


@app.get("/boreholes")
def get_boreholes(
    minx: float = Query(...),
    miny: float = Query(...),
    maxx: float = Query(...),
    maxy: float = Query(...),
    zoom: int = Query(10)       # ← new parameter, default 10 if not sent
):
    precision = max(0, zoom - 6)  # zoom 7→1, zoom 8→2, zoom 9→3, zoom 10+→4+
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "boreholes", minx, miny, maxx, maxy, precision)
        return data
    finally:
        release_conn(conn)


@app.get("/pipelines")
def get_pipelines(
    minx: float = Query(...),
    miny: float = Query(...),
    maxx: float = Query(...),
    maxy: float = Query(...)
    # no zoom — pipelines don't need thinning
):
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "pipelines", minx, miny, maxx, maxy)
        return data
    finally:
        release_conn(conn)


@app.get("/licenses")
def get_licenses(
    minx: float = Query(...),
    miny: float = Query(...),
    maxx: float = Query(...),
    maxy: float = Query(...)
):
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "active_licenses", minx, miny, maxx, maxy)
        return data
    finally:
        release_conn(conn)