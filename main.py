
import csv
from datetime import datetime
from collections import defaultdict

FILE = "study_log.csv"


def log_session(subject, hours):
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([subject, float(hours), datetime.now().date()])


def load_data():
    data = []

    try:
        with open(FILE, "r") as f:
            reader = csv.reader(f)
            for subject, hours, date in reader:
                data.append((subject, float(hours), date))
    except FileNotFoundError:
        pass

    return data


def show_summary(data):
    totals = defaultdict(float)

    for subject, hours, _ in data:
        totals[subject] += hours

    print("\nStudy Summary:")
    for sub, hrs in totals.items():
        print(f"{sub}: {hrs:.1f} hours")


def productive_day(data):
    days = defaultdict(float)

    for _, hours, date in data:
        days[date] += hours

    if days:
        best_day = max(days, key=days.get)
        print(f"\nMost productive day: {best_day} ({days[best_day]} hrs)")


def study_streak(data):
    dates = sorted({d for _, _, d in data})

    streak = 1
    longest = 1

    for i in range(1, len(dates)):
        prev = datetime.fromisoformat(dates[i-1])
        curr = datetime.fromisoformat(dates[i])

        if (curr - prev).days == 1:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 1

    if dates:
        print(f"Longest study streak: {longest} days")


def goal_progress(data, goal=100):
    total = sum(hours for _, hours, _ in data)
    percent = (total / goal) * 100

    print(f"\nGoal Progress: {total:.1f}/{goal} hours ({percent:.0f}%)")


def main():
    while True:
        print("\n1.Log Session  2.View Insights  3.Exit")
        choice = input("Choose: ")

        if choice == "1":
            subject = input("Subject: ").strip()
            while True:
                try:
                    hours = float(input("Hours studied: "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            log_session(subject, hours)

        elif choice == "2":
            data = load_data()
            show_summary(data)
            productive_day(data)
            study_streak(data)
            goal_progress(data)
        elif choice == "3":
            break
        else:
            print("Invalid input. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
