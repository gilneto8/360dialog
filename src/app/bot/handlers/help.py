def handle_help() -> str:
    return (
        "Available commands:\n"
        "- add --title <Title> --start <Date> [--end <Date>]\n"
        "- update --title <Title> [--new-title <Title>] [--start <Date>] [--end <Date>]\n"
        "- remove --title <Title> | --all\n"
        "- list [--start <Date>] [--end <Date>]\n"
        "- free --start <Date> [--end <Date>]\n"
        "- help\n"
        "\n"
        "Supported Date formats for 'add', 'list', 'free' commands:\n"
        "    - YYYY-MM-DD HH:MM (e.g., 2026-03-02 15:00)\n"
        "    - MM-DD HH:MM (e.g., 03-02 15:00)\n"
        "    - Month DD [HH:MM] (e.g., Feb 14 15:00, March 2)\n"
        "    - DD HH:MM (e.g., 02 15:00)\n"
        "    - DD HH (e.g., 02 15)\n"
        "    - Weekday [Time] (e.g., Tue 15:00, Monday)\n"
        "    - HH:MM (e.g., 15:00)"
    )
