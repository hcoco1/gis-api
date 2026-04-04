# queries.py — return raw string, not a Python dict
def fetch_geojson_bbox_raw(conn, table, minx, miny, maxx, maxy, precision=4):
    if precision < 4:
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
        )::text                          -- ← cast to text here, stays a string
        FROM (
            SELECT DISTINCT ON (
                ROUND(ST_X(geom)::numeric, {precision}),
                ROUND(ST_Y(geom)::numeric, {precision})
            )
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', to_jsonb(t) - 'geom'
            ) AS feature
            FROM {table} t
            WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
            ORDER BY
                ROUND(ST_X(geom)::numeric, {precision}),
                ROUND(ST_Y(geom)::numeric, {precision})
            LIMIT 2000
        ) sub
        """
    else:
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
        )::text                          -- ← same here
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
        return '{"type":"FeatureCollection","features":[]}'

    return result  # ← already a string, goes straight to Response()