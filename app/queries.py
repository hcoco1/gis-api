def fetch_geojson_bbox_raw(conn, table, minx, miny, maxx, maxy, precision=4, status=None):

    # build filter
    status_filter = ""
    params = [minx, miny, maxx, maxy]

    if status:
        status_filter = " AND LOWER(status) = LOWER(%s)"
        params.append(status)

    if precision < 4:
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
        )::text
        FROM (
            SELECT (
                ROUND(ST_X(geom)::numeric, {precision}),
                ROUND(ST_Y(geom)::numeric, {precision})
            ),
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', to_jsonb(t) - 'geom'
            ) AS feature
            FROM {table} t
            WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
            {status_filter}
            ORDER BY
                ROUND(ST_X(geom)::numeric, {precision}),
                ROUND(ST_Y(geom)::numeric, {precision})
            LIMIT 5000
        ) sub
        """
    else:
        query = f"""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(feature), '[]'::json)
        )::text
        FROM (
            SELECT json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', to_jsonb(t) - 'geom'
            ) AS feature
            FROM {table} t
            WHERE geom && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
            {status_filter}
            LIMIT 5000
        ) sub
        """

    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetchone()[0]

    if result is None:
        return '{"type":"FeatureCollection","features":[]}'

    return result