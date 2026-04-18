from parser import parse_log_file
from collections import Counter
from datetime import datetime
import time


# -----------------------------
# Extract only ERROR logs
# -----------------------------
def extract_errors(logs):
    return [log for log in logs if log["level"] == "ERROR"]


# -----------------------------
# Categorize error messages
# -----------------------------
def categorize_error(message):
    if "Database connection failed" in message:
        return "Database Error"
    elif "Timeout" in message:
        return "Timeout Error"
    elif "Payment failed" in message:
        return "Payment Error"
    else:
        words = message.split()
        return " ".join(words[:2]) + " Error"


# -----------------------------
# Count error types
# -----------------------------
def analyze_errors(logs):
    errors = extract_errors(logs)
    categorized = [categorize_error(log["message"]) for log in errors]
    return Counter(categorized)


# -----------------------------
# Analyze error trend by hour
# -----------------------------
def error_trend_by_hour(logs):
    errors = extract_errors(logs)
    hour_counts = {}

    for log in errors:
        timestamp = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
        hour = timestamp.hour

        hour_counts[hour] = hour_counts.get(hour, 0) + 1

    return hour_counts


# -----------------------------
# Identify critical insights
# -----------------------------
def find_most_critical(error_summary, trend):
    if not error_summary or not trend:
        return "No Errors", "N/A"

    most_common_error = max(error_summary, key=error_summary.get)
    peak_hour = max(trend, key=trend.get)
    return most_common_error, peak_hour


# -----------------------------
# Generate report file
# -----------------------------
def generate_report(error_summary, trend, most_error, peak_hour):
    with open("reports/summary.txt", "w", encoding="utf-8") as file:
        file.write("LOG ANALYSIS REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write("Error Summary:\n")
        for error, count in error_summary.items():
            file.write(f"- {error}: {count}\n")

        file.write("\nError Trend by Hour:\n")
        for hour, count in sorted(trend.items()):
            file.write(f"- {hour}:00 -> {count} errors\n")

        file.write("\nCritical Insights:\n")
        file.write(f"- Most Frequent Error: {most_error}\n")

        if peak_hour != "N/A":
            file.write(f"- Peak Failure Window: {peak_hour}:00–{peak_hour+1}:00\n")
        else:
            file.write("- Peak Failure Window: N/A\n")


# -----------------------------
# Run one cycle
# -----------------------------
def run_analysis():
    logs = parse_log_file("logs/sample.log")

    error_summary = analyze_errors(logs)

    print("\n🔴 Error Summary:\n")
    for error_type, count in error_summary.items():
        print(f"{error_type}: {count}")

    trend = error_trend_by_hour(logs)

    print("\n⏱️ Error Trend by Hour:\n")
    for hour, count in sorted(trend.items()):
        print(f"{hour}:00 - {count} errors")

    most_error, peak_hour = find_most_critical(error_summary, trend)

    print("\n🚨 Critical Insights:\n")
    print(f"Most Frequent Error: {most_error}")

    if peak_hour != "N/A":
        print(f"Peak Failure Hour: {peak_hour}:00")
    else:
        print("Peak Failure Hour: N/A")

    generate_report(error_summary, trend, most_error, peak_hour)

    print("\n📄 Report updated\n")


# -----------------------------
# Continuous monitoring
# -----------------------------
if __name__ == "__main__":
    print("🔄 Monitoring logs... Press Ctrl+C to stop.\n")

    try:
        while True:
            run_analysis()
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")