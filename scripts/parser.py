def parse_log_line(line):
    parts = line.strip().split(" ", 3)

    if len(parts) < 4:
        return None

    date = parts[0]
    time = parts[1]
    level = parts[2]
    message = parts[3]

    return {
        "timestamp": f"{date} {time}",
        "level": level,
        "message": message
    }


def parse_log_file(file_path):
    parsed_logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)

    return parsed_logs


if __name__ == "__main__":
    logs = parse_log_file("logs/sample.log")

    for log in logs[:5]:  # preview only
        print(log)