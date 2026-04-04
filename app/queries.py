# NEVER use ; inside Python SQL strings
def fetch_geojson_bbox(conn, table, minx, miny, maxx, maxy):
    query = f"""
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(feature)
    )
    FROM (
        SELECT json_build_object(
            'type', 'Feature',
            'geometry', ST_AsGeoJSON(geom)::json,
            'properties', to_jsonb(t) - 'geom'
        ) AS feature
        FROM {table} t
        WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
        LIMIT 2000
    ) sub
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