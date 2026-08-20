WORKOUT_TEMPLATES: dict[int, list[str]] = {
    3: ["Full Body A", "Full Body B", "Full Body C"],
    4: ["Upper", "Lower", "Upper", "Lower"],
    5: ["Push", "Pull", "Legs", "Upper", "Lower"],
}

EXERCISE_TEMPLATES: dict[str, list[tuple[str, int, int]]] = {
    "Push": [
        ("Bench Press", 3, 10),
        ("Incline Dumbbell Press", 3, 10),
        ("Triceps Pushdown", 3, 12),
    ],
    "Pull": [
        ("Lat Pulldown", 3, 10),
        ("Seated Row", 3, 10),
        ("Biceps Curl", 3, 12),
    ],
    "Legs": [
        ("Leg Press", 3, 10),
        ("Leg Curl", 3, 12),
        ("Leg Extension", 3, 12),
    ],
    "Upper": [
        ("Bench Press", 3, 10),
        ("Seated Row", 3, 10),
        ("Shoulder Press", 3, 10),
    ],
    "Lower": [
        ("Leg Press", 3, 10),
        ("Leg Curl", 3, 12),
        ("Calf Raise", 3, 15),
    ],
}
