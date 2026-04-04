from fastapi import FastAPI
from app.db import get_conn
from fastapi import Query
from app.queries import fetch_geojson_bbox
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

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


from app.db import get_conn, release_conn

@app.get("/boreholes")
def get_boreholes(minx: float = Query(...), miny: float = Query(...),
                  maxx: float = Query(...), maxy: float = Query(...)):
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "boreholes", minx, miny, maxx, maxy)
        return data
    finally:
        release_conn(conn)  # Always return the connection!

# Same pattern for /pipelines and /licenses


@app.get("/pipelines")
def get_pipelines(minx: float = Query(...), miny: float = Query(...),
                  maxx: float = Query(...), maxy: float = Query(...)):
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "pipelines", minx, miny, maxx, maxy)
        return data
    finally:
        release_conn(conn)  # Always return the connection! 


@app.get("/licenses")
def get_licenses(minx: float = Query(...), miny: float = Query(...),
                 maxx: float = Query(...), maxy: float = Query(...)):
    conn = get_conn()
    try:
        data = fetch_geojson_bbox(conn, "active_licenses", minx, miny, maxx, maxy)
        return data
    finally:
        release_conn(conn)  # Always return the connection!
