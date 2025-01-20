WITH StateGroups AS (
    SELECT 
        vx.vax_name, vd.state AS State,
        COUNT(*) AS Event_Count
    FROM vdata vd
    JOIN vax vx ON vd.vaers_id = vx.vaers_id
    WHERE 
	vx.vax_type like 'COVID%'
	and vd.died = 1
    GROUP BY vx.vax_name, vd.state
)
SELECT 
	VAX_NAME,
    State,
    SUM(Event_Count) AS Total_Events
FROM StateGroups
GROUP BY vax_name, State
ORDER BY Total_Events desc;