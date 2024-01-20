import pandas as pd
from datetime import datetime, timedelta

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def time_to_hours(time_value):
    if isinstance(time_value, float):
        return time_value  # Already a float, no need to convert
    else:
        time_parts = [int(part) for part in str(time_value).split(':')]
        return time_parts[0] + time_parts[1] / 60.0

def analyze_file(file_path):
    df = pd.read_excel(file_path)

    name_col = 'Employee Name'
    position_col = 'Position ID'
    date_col = 'Pay Cycle Start Date'
    hours_col = 'Timecard Hours (as Time)'

    df[date_col] = pd.to_datetime(df[date_col])  # Convert date column to datetime
    df[hours_col] = df[hours_col].apply(time_to_hours)  # Convert time strings to float hours

    employees = {}

    for index, row in df.iterrows():
        name = row[name_col]
        position = row[position_col]
        date = row[date_col]
        hours = row[hours_col]

        if name not in employees:
            employees[name] = {'positions': set(), 'shifts': []}

        employees[name]['positions'].add(position)
        employees[name]['shifts'].append({'date': date, 'hours': hours})

    for name, data in employees.items():
        shifts = data['shifts']

        # a) who has worked for 7 consecutive days
        for i in range(len(shifts) - 6):
            consecutive_days = [shift['date'] for shift in shifts[i:i + 7]]
            if (consecutive_days[-1] - consecutive_days[0]).days == 6:
                print(f"{name} ({', '.join(data['positions'])}) has worked for 7 consecutive days.")

        # b) who have less than 10 hours of time between shifts but greater than 1 hour
        for i in range(len(shifts) - 1):
            time_between_shifts = shifts[i + 1]['date'] - shifts[i]['date'] - timedelta(hours=shifts[i]['hours'])
            if 1 < time_between_shifts.total_seconds() / 3600 < 10:
                print(f"{name} ({', '.join(data['positions'])}) has less than 10 hours between shifts but greater than 1 hour.")

        # c) Who has worked for more than 14 hours in a single shift
        for shift in shifts:
            if shift['hours'] > 14:
                print(f"{name} ({', '.join(data['positions'])}) has worked for more than 14 hours in a single shift.")
                print(f"Shift details: Date: {shift['date']}, Hours: {shift['hours']}")

# Example usage
file_path = 'Assignment_Timecard.csv.xlsx'
analyze_file(file_path)
