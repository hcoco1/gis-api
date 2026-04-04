from fastapi import FastAPI
from app.db import get_conn
from app.queries import fetch_geojson

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GIS API running 🚀"}


@app.get("/boreholes")
def get_boreholes():
    conn = get_conn()
    data = fetch_geojson(conn, "boreholes")
    conn.close()
    return data


@app.get("/pipelines")
def get_pipelines():
    conn = get_conn()
    data = fetch_geojson(conn, "pipelines")
    conn.close()
    return data


@app.get("/licenses")
def get_licenses():
    conn = get_conn()
    data = fetch_geojson(conn, "active_licenses")
    conn.close()
    return data