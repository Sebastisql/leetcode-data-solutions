import pandas as pd

def find_study_spiral_pattern(students: pd.DataFrame, study_sessions: pd.DataFrame) -> pd.DataFrame:
    return (
        study_sessions
        .assign(
            session_date=lambda x: pd.to_datetime(x['session_date']),
            cycle_length=lambda x: x.groupby('student_id')['subject'].transform('nunique'),
            subjects_count=lambda x: x.groupby('student_id')['subject'].transform('size')
        )
        .query("cycle_length >= 3 and subjects_count >= 6")
        .sort_values(by=['student_id', 'session_date'], ascending=True)
        .assign(
            invalid_group_gap=lambda x: (
                x.groupby('student_id')['session_date'].diff().dt.days > 2
            ).groupby(x['student_id']).transform('any')
        )
        .query("~invalid_group_gap")
        .assign(
            rn=lambda x: x.groupby('student_id').cumcount() + 1,
            rn_shift=lambda x: x['rn'] - x['cycle_length']
        )
        .pipe(lambda x: x.merge(
            x[['student_id', 'subject', 'rn']],
            how='left', 
            left_on=['student_id', 'rn_shift'],
            right_on=['student_id', 'rn'],
            suffixes=('', '_prev')
        ))
        .assign(
            is_repeat_pattern_row=lambda x: (x['subject'] == x['subject_prev']) | x['subject_prev'].isna(),
            is_repeat_pattern_group=lambda x: x.groupby('student_id')['is_repeat_pattern_row'].transform('all')
        )
        .query("is_repeat_pattern_group")
        .groupby('student_id', as_index=False).agg(
            total_study_hours=('hours_studied', 'sum'),
            cycle_length=('cycle_length', 'first')
        )
        .merge(students, on='student_id', how='inner')
        [['student_id', 'student_name', 'major', 'cycle_length', 'total_study_hours']]
        .sort_values(by=['cycle_length', 'total_study_hours'], ascending=[False, False])
    )