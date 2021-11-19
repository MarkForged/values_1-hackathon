SELECT DISTINCT
    material_id
FROM extrusion_runs
WHERE
    material_id != '---'
ORDER BY
    material_id;
