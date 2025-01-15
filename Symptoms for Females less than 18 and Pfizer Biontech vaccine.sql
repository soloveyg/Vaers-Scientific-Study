SELECT top 50
    s.SYMPTOM,
    COUNT(*) AS Symptom_Count
FROM 
    vdata vd
JOIN 
    vax v ON vd.VAERS_ID = v.VAERS_ID
JOIN 
    (
        SELECT VAERS_ID, SYMPTOM1 AS SYMPTOM FROM sympt
        UNION ALL
        SELECT VAERS_ID, SYMPTOM2 AS SYMPTOM FROM sympt
        UNION ALL
        SELECT VAERS_ID, SYMPTOM3 AS SYMPTOM FROM sympt
        UNION ALL
        SELECT VAERS_ID, SYMPTOM4 AS SYMPTOM FROM sympt
        UNION ALL
        SELECT VAERS_ID, SYMPTOM5 AS SYMPTOM FROM sympt
    ) s ON vd.VAERS_ID = s.VAERS_ID
WHERE 
    v.VAX_TYPE LIKE 'COVID%' -- Filter for COVID vaccines
	and v.VAX_NAME like '%Biontech%'
    AND s.SYMPTOM IS NOT NULL -- Exclude NULL symptoms
	and s.SYMPTOM != 'No adverse event'
	and s.SYMPTOM not like '%test%'
	-- and s.SYMPTOM = 'Death'
	and vd.AGE_YRS < 18
	and vd.SEX = 'F'
GROUP BY 
    s.SYMPTOM
ORDER BY 
    Symptom_Count DESC;