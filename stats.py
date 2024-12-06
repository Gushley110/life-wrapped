def calculate_percentages(minutes_music, work_hours, sleep_hours, exercise_hours, hobby_hours):
    total_year_minutes = 525600  # Total minutes in a year (365 days)
    activities_minutes = {
        "Music": minutes_music,
        "Work": work_hours * 60 * 365,
        "Sleep": sleep_hours * 60 * 365,
        "Exercise": exercise_hours * 60 * 365,
        "Hobbies": hobby_hours * 60 * 365,
    }
    percentages = {k: (v / total_year_minutes) * 100 for k, v in activities_minutes.items()}
    return percentages


def calculate_hours_in_day(minutes_music, work_hours, sleep_hours, exercise_hours, hobby_hours):
    activities_hours = {
        "Music": minutes_music // 365 // 60,  # Convert yearly minutes to daily hours
        "Work": work_hours,
        "Sleep": sleep_hours,
        "Exercise": exercise_hours,
        "Hobbies": hobby_hours,
    }
    return activities_hours
