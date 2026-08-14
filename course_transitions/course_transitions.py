import pandas as pd

def topLearnerCourseTransitions(course_completions: pd.DataFrame) -> pd.DataFrame:
    return (
        course_completions
        .groupby(['user_id'], as_index=False)
        .agg(
            course_count=('user_id', 'size'),
            course_avg=('course_rating', 'mean')
        )
        .query("course_count >= 5 and course_avg >= 4")
        .merge(course_completions, on='user_id', how='inner', validate='one_to_many')
        .loc[:, ['user_id', 'course_name', 'completion_date']]
        .sort_values(by=['user_id', 'completion_date'], ascending=[True, True])
        .assign(second_course=lambda x: x.groupby('user_id')['course_name'].shift(-1))
        .rename(columns={'course_name': 'first_course'})
        .dropna(subset=['second_course'])
        .groupby(['first_course', 'second_course'])
        .size()
        .reset_index(name='transition_count')
        .sort_values(
            by=['transition_count', 'first_course', 'second_course'], 
            ascending=[False, True, True],
            key=lambda col: col.str.lower() if col.name in ['first_course', 'second_course'] else col
        )
    )
