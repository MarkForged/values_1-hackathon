SELECT DISTINCT
    line_id
FROM extrusion_runs
WHERE
    line_id != '---'
ORDER BY
    line_id;
