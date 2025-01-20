WITH SymptomCounts AS (
    SELECT
        vax.vax_name,
        COALESCE(ag.name, 'Unknown') AS age_group,
        s.SYMPTOM,
        COUNT(*) AS symptom_count
    FROM 
        VDATA vd
    JOIN 
        VAX ON vd.VAERS_ID = VAX.VAERS_ID
    LEFT JOIN 
        age_group ag
        ON vd.AGE_YRS BETWEEN ag.min_age AND ag.max_age
    JOIN (
        SELECT VAERS_ID, SYMPTOM1 AS SYMPTOM FROM sympt WHERE SYMPTOM1 IS NOT NULL AND SYMPTOM1 != 'No adverse event'
        UNION ALL
        SELECT VAERS_ID, SYMPTOM2 AS SYMPTOM FROM sympt WHERE SYMPTOM2 IS NOT NULL AND SYMPTOM2 != 'No adverse event'
        UNION ALL
        SELECT VAERS_ID, SYMPTOM3 AS SYMPTOM FROM sympt WHERE SYMPTOM3 IS NOT NULL AND SYMPTOM3 != 'No adverse event'
        UNION ALL
        SELECT VAERS_ID, SYMPTOM4 AS SYMPTOM FROM sympt WHERE SYMPTOM4 IS NOT NULL AND SYMPTOM4 != 'No adverse event'
        UNION ALL
        SELECT VAERS_ID, SYMPTOM5 AS SYMPTOM FROM sympt WHERE SYMPTOM5 IS NOT NULL AND SYMPTOM5 != 'No adverse event'
    ) s ON vd.VAERS_ID = s.VAERS_ID
    WHERE 
        VAX.VAX_TYPE = 'COVID19' -- Filters for COVID vaccines
        AND vd.SEX = 'F'
    GROUP BY 
        vax.VAX_NAME, 
        COALESCE(ag.name, 'Unknown'),
        s.SYMPTOM
),
ScalingFactors AS (
    SELECT
        MAX(symptom_count) AS max_count,
        MIN(symptom_count) AS min_count
    FROM SymptomCounts
),
RankedSymptoms AS (
    SELECT
        sc.vax_name,
        sc.age_group,
        sc.SYMPTOM,
        sc.symptom_count,
        -- Scale the symptom_count to create scaled_events
        CAST((sc.symptom_count - sf.min_count) AS FLOAT) / NULLIF(sf.max_count - sf.min_count, 0) * 100 AS scaled_events,
        ROW_NUMBER() OVER (
            PARTITION BY sc.age_group, sc.SYMPTOM
            ORDER BY sc.symptom_count DESC
        ) AS symptom_rank
    FROM SymptomCounts sc
    CROSS JOIN ScalingFactors sf
)
SELECT
    vax_name,
    age_group,
    SYMPTOM,
    symptom_count,
    scaled_events
FROM 
    RankedSymptoms
WHERE 
    symptom_rank <= 5
    AND scaled_events >= 0.5
ORDER BY 
    age_group, scaled_events DESC;
