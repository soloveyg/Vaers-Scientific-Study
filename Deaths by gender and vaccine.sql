WITH GenderGroups AS (
    SELECT 
        vx.vax_name,
        vd.sex AS Gender,
        COUNT(*) AS Event_Count
    FROM vdata vd
    JOIN vax vx ON vd.vaers_id = vx.vaers_id
    WHERE 
	vx.vax_type like 'COVID%'
	and vd.died = 1
    GROUP BY vx.vax_name, vd.sex
)
SELECT 
	VAX_NAME,
    Gender,
    SUM(Event_Count) AS Total_Events
FROM GenderGroups
GROUP BY vax_name, Gender
ORDER BY Total_Events desc