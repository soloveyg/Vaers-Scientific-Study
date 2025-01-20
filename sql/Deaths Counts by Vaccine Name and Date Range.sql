SELECT
    r.Date_Range,
    v.VAX_NAME,
    COUNT(vd.DIED) AS Death_Count
FROM 
    range r
LEFT JOIN 
    vdata vd ON vd.RECVDATE >= r.start_date AND vd.RECVDATE <= r.end_date
LEFT JOIN 
    vax v ON vd.VAERS_ID = v.VAERS_ID
WHERE 
    vd.DIED = 1
    AND v.VAX_TYPE LIKE 'COVID%'
    AND v.VAX_NAME != 'COVID19 (COVID19 (UNKNOWN))'
GROUP BY 
    r.Date_Range, r.start_date, r.end_date, v.VAX_TYPE, v.VAX_NAME
ORDER BY 
    r.start_date, Death_Count DESC;