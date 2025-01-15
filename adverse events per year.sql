SELECT 
    COUNT(*) AS cnt, 
    YEAR(recvdate) AS year
FROM vdata vd
join vax vx on vx.vaers_id = vd.vaers_id
WHERE recvdate IS NOT NULL
-- and vx.vax_type like 'COVID%'
-- and YEAR(vax_date) >= 2020
GROUP BY YEAR(recvdate)
ORDER BY year;