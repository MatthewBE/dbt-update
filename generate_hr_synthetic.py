"""Generate two synthetic HR Analytics CSV files with same columns and types as original, half size each."""
import csv
import random

# Original row count 1470 -> 735 per file
ROWS_PER_FILE = 735
HEADER = [
    "Age", "Attrition", "BusinessTravel", "DailyRate", "Department", "DistanceFromHome",
    "Education", "EducationField", "EmployeeCount", "EmployeeNumber", "EnvironmentSatisfaction",
    "Gender", "HourlyRate", "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction",
    "MaritalStatus", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "Over18", "OverTime",
    "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction", "StandardHours",
    "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "WorkLifeBalance",
    "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
]

CATEGORICAL = {
    "Attrition": ["No", "Yes"],
    "BusinessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
    "Department": ["Human Resources", "Research & Development", "Sales"],
    "EducationField": ["Human Resources", "Life Sciences", "Marketing", "Medical", "Other", "Technical Degree"],
    "Gender": ["Female", "Male"],
    "JobRole": [
        "Healthcare Representative", "Human Resources", "Laboratory Technician", "Manager",
        "Manufacturing Director", "Research Director", "Research Scientist", "Sales Executive",
        "Sales Representative",
    ],
    "MaritalStatus": ["Divorced", "Married", "Single"],
    "Over18": ["Y"],
    "OverTime": ["No", "Yes"],
}

INT_RANGES = {
    "Age": (18, 60),
    "DailyRate": (102, 1499),
    "DistanceFromHome": (1, 29),
    "Education": (1, 5),
    "EmployeeCount": (1, 1),
    "EmployeeNumber": (1, 9999),  # unique per synthetic file
    "EnvironmentSatisfaction": (1, 4),
    "HourlyRate": (30, 100),
    "JobInvolvement": (1, 4),
    "JobLevel": (1, 5),
    "JobSatisfaction": (1, 4),
    "MonthlyIncome": (1009, 19999),
    "MonthlyRate": (2094, 26999),
    "NumCompaniesWorked": (0, 9),
    "PercentSalaryHike": (11, 25),
    "PerformanceRating": (3, 4),
    "RelationshipSatisfaction": (1, 4),
    "StandardHours": (80, 80),
    "StockOptionLevel": (0, 3),
    "TotalWorkingYears": (0, 40),
    "TrainingTimesLastYear": (0, 6),
    "WorkLifeBalance": (1, 4),
    "YearsAtCompany": (0, 40),
    "YearsInCurrentRole": (0, 18),
    "YearsSinceLastPromotion": (0, 15),
    "YearsWithCurrManager": (0, 17),
}


def generate_row(employee_number: int) -> dict:
    row = {}
    for col in HEADER:
        if col in CATEGORICAL:
            row[col] = random.choice(CATEGORICAL[col])
        elif col in INT_RANGES:
            lo, hi = INT_RANGES[col]
            if col == "EmployeeNumber":
                row[col] = employee_number
            else:
                row[col] = random.randint(lo, hi)
        else:
            raise KeyError(col)
    return row


def main():
    random.seed(42)
    for file_num in (1, 2):
        path = f"/home/anon/Project/dbt/HR-Employee-Attrition-synthetic-{file_num}.csv"
        start_emp = (file_num - 1) * ROWS_PER_FILE + 1
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADER)
            w.writeheader()
            for i in range(ROWS_PER_FILE):
                w.writerow(generate_row(start_emp + i))
        print(f"Wrote {path} ({ROWS_PER_FILE} rows)")


if __name__ == "__main__":
    main()
