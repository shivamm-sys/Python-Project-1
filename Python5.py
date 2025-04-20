import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class HealthTracker:
    def __init__(self):
        self.df = pd.DataFrame(columns=["Date", "Steps", "Sleep", "Calories", "Water"])
        self.daily_goals = {
            "steps": 10000,
            "sleep": 8,  # hours
            "calories": 2000,
            "water": 2.5  # Liters
        }
        self.bmi_data = []
        self.calories_data = []

    def add_data(self, date, steps, sleep, calories, water_intake):
        # Check if the date already exists
        if date in self.df["Date"].values:
            self.df.loc[self.df["Date"] == date, ["Steps", "Sleep", "Calories", "Water"]] += [steps, sleep, calories, water_intake]
        else:
            new_data = pd.DataFrame([[date, steps, sleep, calories, water_intake]],
                                    columns=["Date", "Steps", "Sleep", "Calories", "Water"])
            self.df = pd.concat([self.df, new_data], ignore_index=True)

    def view_data(self):
        print(self.df)

    def check_goals(self, date):
        row = self.df[self.df["Date"] == date]
        if row.empty:
            print(f"No data for {date}")
            return

        row = row.iloc[0]
        print(f"Health Data for {date}:")
        print(f"Steps: {row['Steps']} / {self.daily_goals['steps']} (Goal)")
        print(f"Sleep: {row['Sleep']} hours / {self.daily_goals['sleep']} hours (Goal)")
        print(f"Calories: {row['Calories']} kcal / {self.daily_goals['calories']} kcal (Goal)")
        print(f"Water Intake: {row['Water']} L / {self.daily_goals['water']} L (Goal)")

        if row['Steps'] >= self.daily_goals['steps']:
            print("Great job on reaching your daily steps goal!")
        else:
            print(f"You need {self.daily_goals['steps'] - row['Steps']} more steps to reach your goal.")

        if row['Sleep'] >= self.daily_goals['sleep']:
            print("You reached your daily sleep goal!")
        else:
            print(f"You need {self.daily_goals['sleep'] - row['Sleep']} more hours of sleep.")

        if row['Calories'] <= self.daily_goals['calories']:
            print("You are within your daily calorie limit.")
        else:
            print(f"You have exceeded your daily calorie goal by {row['Calories'] - self.daily_goals['calories']} kcal.")

        if row['Water'] >= self.daily_goals['water']:
            print("You reached your daily water intake goal!")
        else:
            print(f"You need {self.daily_goals['water'] - row['Water']} more liters of water.")

    def calculate_bmi(self, weight, height):
        bmi = weight / (height ** 2)
        self.bmi_data.append(bmi)
        print(f"Your BMI is: {bmi:.2f}")

    def generate_report(self):
        print("Weekly Health Report:")
        week_data = self.df.tail(7).sum()
        print(f"Steps: {week_data['Steps']} steps")
        print(f"Sleep: {week_data['Sleep']} hours")
        print(f"Calories: {week_data['Calories']} kcal")
        print(f"Water Intake: {week_data['Water']} L")

    def hydration_reminder(self, current_water_intake):
        if current_water_intake < self.daily_goals["water"]:
            print("Reminder: You need to drink more water to reach your goal!")
        else:
            print("Good job! You've reached your daily water intake goal.")

    def graph_progress(self):
        # Sort data by Date to make sure it's in chronological order
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        self.df = self.df.sort_values(by="Date")

        plt.figure(figsize=(10, 6))
        plt.plot(self.df["Date"], self.df["Steps"], label="Steps", color="blue", marker="o")
        plt.plot(self.df["Date"], self.df["Sleep"], label="Sleep (hours)", color="green", marker="o")
        plt.plot(self.df["Date"], self.df["Calories"], label="Calories", color="red", marker="o")
        plt.plot(self.df["Date"], self.df["Water"], label="Water Intake (L)", color="orange", marker="o")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Health Tracker Progress")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    tracker = HealthTracker()

    # Sample data for 5 days
    tracker.add_data('2025-04-14', 8000, 7, 1800, 2.0)
    tracker.add_data('2025-04-15', 12000, 8, 1900, 2.2)
    tracker.add_data('2025-04-16', 9000, 6, 2100, 2.0)
    tracker.add_data('2025-04-17', 11000, 7, 2000, 2.5)
    tracker.add_data('2025-04-18', 10000, 8, 1950, 2.0)

    tracker.view_data()

    # Checking daily goal progress for a date
    tracker.check_goals('2025-04-15')

    # BMI Calculation
    tracker.calculate_bmi(70, 1.75)

    # Weekly Report
    tracker.generate_report()

    # Hydration reminder
    tracker.hydration_reminder(2.0)

    # Graph Progress
    tracker.graph_progress()
