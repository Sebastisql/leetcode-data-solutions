import pandas as pd

def analyze_dna_patterns(samples: pd.DataFrame) -> pd.DataFrame:
    return (
        samples
        .assign(
            has_start=lambda x: x['dna_sequence'].str.startswith('ATG').astype(int),
            has_stop=lambda x: x['dna_sequence'].str.endswith(('TAA', 'TAG', 'TGA')).astype(int),
            has_atat=lambda x: x['dna_sequence'].str.contains('ATAT', regex=False).astype(int),
            has_ggg=lambda x: x['dna_sequence'].str.contains('GGG', regex=False).astype(int),
        )
        .sort_values(by=['sample_id'])
    )