WITH AgeGroups AS (
    SELECT 
        vx.vax_name,
        CASE 
            WHEN vd.age_yrs IS NULL THEN 'Unknown'
            WHEN vd.age_yrs < 18 THEN '0-17'
            WHEN vd.age_yrs BETWEEN 18 AND 30 THEN '18-30'
            WHEN vd.age_yrs BETWEEN 31 AND 50 THEN '31-50'
            WHEN vd.age_yrs BETWEEN 51 AND 65 THEN '51-65'
            WHEN vd.age_yrs > 65 THEN '65+'
        END AS Age_Group,
--        vd.sex AS Gender,
--        vd.state AS State,
        COUNT(*) AS Event_Count
    FROM vdata vd
    JOIN vax vx ON vd.vaers_id = vx.vaers_id
    WHERE 
	vx.vax_type like 'COVID%'
	and vd.died = 1
    GROUP BY vx.vax_name,
             CASE 
                 WHEN vd.age_yrs IS NULL THEN 'Unknown'
                 WHEN vd.age_yrs < 18 THEN '0-17'
                 WHEN vd.age_yrs BETWEEN 18 AND 30 THEN '18-30'
                 WHEN vd.age_yrs BETWEEN 31 AND 50 THEN '31-50'
                 WHEN vd.age_yrs BETWEEN 51 AND 65 THEN '51-65'
                 WHEN vd.age_yrs > 65 THEN '65+'
             END
             --,
             --vd.sex,
             --vd.state
)
SELECT 
    Age_Group,
	VAX_NAME,
--    Gender,
--    State,
    SUM(Event_Count) AS Total_Events
FROM AgeGroups
GROUP BY Age_Group, vax_name
--, Gender, State
ORDER BY Total_Events desc
--Age_Group--, Gender, State;