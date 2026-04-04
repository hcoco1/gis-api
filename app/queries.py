

def fetch_geojson_bbox(conn, table, minx, miny, maxx, maxy):
    query = f"""
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', to_jsonb(t) - 'geom'
            )
        )
    )
    FROM {table} t
    WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326);
    """

    with conn.cursor() as cur:
        cur.execute(query, (minx, miny, maxx, maxy))
        result = cur.fetchone()[0]

    if result is None:
        return {
            "type": "FeatureCollection",
            "features": []
        }

    return result