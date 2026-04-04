def fetch_geojson_bbox(conn, table, minx, miny, maxx, maxy, precision=4):
    """
    precision controls spatial thinning:
    - low precision (1-2) = coarse grid = fewer points = zoomed out views
    - high precision (4+) = fine grid = all points = zoomed in views
    
    DISTINCT ON rounds coordinates to a grid cell and keeps one 
    point per cell, giving geographically even coverage.
    """

    # For boreholes (points), use grid-based deduplication
    # For lines/polygons (pipelines, licenses), skip thinning entirely
    if precision < 4:
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
        )
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
        # Full detail — original query
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
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
        return {"type": "FeatureCollection", "features": []}

    return result