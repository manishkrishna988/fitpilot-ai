WORKOUT_TEMPLATES: dict[int, list[str]] = {
    3: ["Full Body A", "Full Body B", "Full Body C"],
    4: ["Upper", "Lower", "Upper", "Lower"],
    5: ["Push", "Pull", "Legs", "Upper", "Lower"],
}

EXERCISE_TEMPLATES: dict[str, list[tuple[str, int, int, str]]] = {
    "Push": [
        ("Bench Press", 3, 10, "barbell"),
        ("Incline Dumbbell Press", 3, 10, "dumbbells"),
        ("Triceps Pushdown", 3, 12, "cable_machine"),
    ],
    "Pull": [
        ("Lat Pulldown", 3, 10, "cable_machine"),
        ("Seated Row", 3, 10, "cable_machine"),
        ("Biceps Curl", 3, 12, "dumbbells"),
    ],
    "Legs": [
        ("Leg Press", 3, 10, "machines"),
        ("Leg Curl", 3, 12, "machines"),
        ("Leg Extension", 3, 12, "machines"),
    ],
    "Upper": [
        ("Bench Press", 3, 10, "barbell"),
        ("Seated Row", 3, 10, "cable_machine"),
        ("Shoulder Press", 3, 10, "dumbbells"),
    ],
    "Lower": [
        ("Leg Press", 3, 10, "machines"),
        ("Leg Curl", 3, 12, "machines"),
        ("Calf Raise", 3, 15, "machines"),
    ],
}

EQUIPMENT_ALIASES: dict[str, str] = {
    "dumbbell": "dumbbells",
    "dumbells": "dumbbells",
    "dumbbells": "dumbbells",
    "db": "dumbbells",
    "barbell": "barbell",
    "barbells": "barbell",
    "machine": "machines",
    "machines": "machines",
    "cable": "cable_machine",
    "cables": "cable_machine",
    "cable machine": "cable_machine",
    "cable_machine": "cable_machine",
}
