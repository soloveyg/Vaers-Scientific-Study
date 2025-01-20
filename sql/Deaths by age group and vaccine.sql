WITH AgeGroups AS (
    SELECT 
        vx.vax_name,
        COALESCE(ag.name, 'Unknown') AS age_group,
        COUNT(*) AS Event_Count
    FROM vdata vd
    JOIN vax vx ON vd.vaers_id = vx.vaers_id
    LEFT JOIN
        age_group ag
        ON vd.AGE_YRS BETWEEN ag.min_age AND ag.max_age
    WHERE 
	vx.vax_type like 'COVID%'
	and vd.died = 1
    GROUP BY vx.vax_name, COALESCE(ag.name, 'Unknown')
)
SELECT 
    Age_Group,
	VAX_NAME,
    SUM(Event_Count) AS Total_Events
FROM AgeGroups
GROUP BY Age_Group, vax_name
ORDER BY Total_Events desc;