SELECT
    sample_id,
    dna_sequence,
    species,
    CASE 
        WHEN starts_with(dna_sequence, 'ATG') THEN 1
        else 0
    END AS has_start,
    CASE
        WHEN dna_sequence LIKE ANY (ARRAY['%TAA', '%TAG', '%TGA']) THEN 1
        else 0
    END AS has_stop,
    CASE
        WHEN dna_sequence LIKE '%ATAT%' THEN 1
        else 0
    END AS has_atat,
    CASE
        WHEN dna_sequence LIKE '%GGG%' THEN 1
        else 0
    END AS has_ggg
FROM samples
ORDER BY sample_id ASC
