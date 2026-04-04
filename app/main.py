from fastapi import FastAPI, Query, Response   # ← single import line, all three
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, release_conn
from app.queries import fetch_geojson_bbox_raw  # ← only import the raw version

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
    zoom: int = Query(10)
):
    precision = max(0, zoom - 6)
    conn = get_conn()
    try:
        raw_json = fetch_geojson_bbox_raw(conn, "boreholes", minx, miny, maxx, maxy, precision)
        return Response(content=raw_json, media_type="application/json")
    finally:
        release_conn(conn)


@app.get("/pipelines")
def get_pipelines(
    minx: float = Query(...),
    miny: float = Query(...),
    maxx: float = Query(...),
    maxy: float = Query(...)
):
    conn = get_conn()
    try:
        raw_json = fetch_geojson_bbox_raw(conn, "pipelines", minx, miny, maxx, maxy)
        return Response(content=raw_json, media_type="application/json")
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
        raw_json = fetch_geojson_bbox_raw(conn, "active_licenses", minx, miny, maxx, maxy)
        return Response(content=raw_json, media_type="application/json")
    finally:
        release_conn(conn)