import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = 'covid_data.csv'

def init_file():
    try:
        pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "City", "New_Cases", "Recoveries", "Deaths"])
        df.to_csv(CSV_FILE, index=False)

def add_daily_data():
    date = input("Date (YYYY-MM-DD) [default: today]: ") or datetime.today().strftime('%Y-%m-%d')
    city = input("City Name: ")
    new_cases = int(input("New Cases: "))
    recoveries = int(input("Recoveries: "))
    deaths = int(input("Deaths: "))

    new_data = pd.DataFrame([[date, city, new_cases, recoveries, deaths]],
                            columns=["Date", "City", "New_Cases", "Recoveries", "Deaths"])

    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print("✅ Data added successfully!\n")

def import_csv():
    file_path = input("Enter CSV file path to import: ")
    try:
        new_data = pd.read_csv(file_path)
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        print("📥 Data imported successfully!")
    except Exception as e:
        print(f" Error importing: {e}")

def risk_zone_analysis():
    df = pd.read_csv(CSV_FILE)
    recent = df.groupby('City').tail(7)
    summary = recent.groupby('City')[['New_Cases']].sum()

    def classify_risk(row):
        if row['New_Cases'] >= 100:
            return 'Red Zone'
        elif row['New_Cases'] >= 30:
            return ' Orange Zone'
        else:
            return 'Green Zone'

    summary['Risk_Zone'] = summary.apply(classify_risk, axis=1)
    print("\nRisk Zone Analysis (Last 7 Days):\n")
    print(summary)

def predict_hotspots():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # Rolling average for the last 7 days per city
    rolling = df.groupby('City')['New_Cases'].rolling(window=7, min_periods=1).mean().reset_index()
    latest = rolling.groupby('City').tail(1)

    threshold = latest['New_Cases'].mean() + latest['New_Cases'].std()
    hotspots = latest[latest['New_Cases'] > threshold]

    print("\n Predicted Hotspots (Based on 7-Day Avg & Std):\n")
    print(hotspots[['City', 'New_Cases']].round(2))

def plot_trends():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    cities = df['City'].unique()

    for city in cities:
        city_data = df[df['City'] == city].groupby('Date')[['New_Cases', 'Recoveries', 'Deaths']].sum()
        city_data = city_data.rolling(window=7).mean()  # Smooth trend

        plt.figure(figsize=(10, 5))
        plt.plot(city_data.index, city_data['New_Cases'], label='New Cases')
        plt.plot(city_data.index, city_data['Recoveries'], label='Recoveries')
        plt.plot(city_data.index, city_data['Deaths'], label='Deaths')
        plt.title(f"📊 COVID Trend - {city}")
        plt.xlabel("Date")
        plt.ylabel("Cases")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    init_file()
    while True:
        print("\n COVID Dashboard")
        print("1. Add Daily Data")
        print("2. Import CSV Data")
        print("3. Risk Zone Analysis")
        print("4. Predict Hotspots")
        print("5. Plot Trend Visualizations")
        print("6. Exit")

        choice = input("Choose option: ")
        if choice == '1':
            add_daily_data()
        elif choice == '2':
            import_csv()
        elif choice == '3':
            risk_zone_analysis()
        elif choice == '4':
            predict_hotspots()
        elif choice == '5':
            plot_trends()
        elif choice == '6':
            print("👋 Exiting Dashboard.")
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
