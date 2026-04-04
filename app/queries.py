def fetch_geojson(conn, table):
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
    FROM {table} t;
    """

    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()[0]