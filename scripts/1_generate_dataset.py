# scripts/1_generate_dataset.py
"""
Generates a simulated dataset of student grades for EPL and saves it to a CSV file.
The dataset includes complex scenarios like multiple teachers for a single course unit (UE).
"""
import pandas as pd
import numpy as np
import random
import os

# --- Configuration ---
NUM_STUDENTS = 1200
ACADEMIC_YEAR = "2024-2025"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "notes_epl_simulees.csv")

# --- Data Definitions ---
DEPARTMENTS = {
    "INFO": "Informatique",
    "MECA": "Mécanique",
    "ELEC": "Électricité",
    "GC": "Génie Civil",
    "MAP": "Mathématiques Appliquées",
}

TEACHERS = [
    "Prof. Dubois", "Prof. Lambert", "Prof. Martin", "Prof. Bernard",
    "Prof. Petit", "Prof. Durand", "Prof. Leroy", "Prof. Moreau",
    "Prof. Simon", "Prof. Laurent"
]

UES = {
    "INFO": [
        ("LINFO1101", "Introduction à la programmation"),
        ("LINFO1102", "Architecture des ordinateurs"),
        ("LINFO1252", "Projet de programmation"),
    ],
    "MECA": [
        ("LMECA1120", "Mécanique des fluides"),
        ("LMECA1510", "Conception des machines"),
        ("LMECA1901", "Projet de conception mécanique"),
    ],
    "ELEC": [
        ("LELEC1370", "Circuits électriques"),
        ("LELEC1755", "Électronique analogique"),
    ],
    "GC": [
        ("LGCIV1071", "Stabilité des constructions"),
        ("LGCIV1022", "Matériaux de construction"),
    ],
    "MAP": [
        ("LMAPR1015", "Analyse mathématique"),
        ("LMAPR1016", "Algèbre linéaire"),
    ],
}

def generate_teachers():
    """Assigns one or two teachers to each UE."""
    ue_teachers = {}
    for dept_ues in UES.values():
        for ue_code, _ in dept_ues:
            num_teachers = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
            assigned_teachers = random.sample(TEACHERS, k=num_teachers)
            ue_teachers[ue_code] = ";".join(assigned_teachers) # Use a separator for multi-teacher UEs
    return ue_teachers

def generate_dataset(ue_teachers):
    """Generates the full dataset."""
    print("Generating dataset...")
    data = []
    student_ids = [f"etu_{2024000 + i}" for i in range(NUM_STUDENTS)]

    for student_id in student_ids:
        # Assign a random department to each student
        student_dept_code = random.choice(list(DEPARTMENTS.keys()))

        # Each student takes all UEs from their department
        for ue_code, ue_name in UES[student_dept_code]:
            # Simulate a realistic grade distribution (mean around 12, std dev around 3)
            # Add some randomness to the mean for each UE
            base_mean = random.uniform(9, 14)
            note = np.random.normal(loc=base_mean, scale=3.5)
            note = np.clip(round(note, 2), 0, 20) # Clip notes to be between 0 and 20

            # 10% chance of being absent (NaN grade)
            if random.random() < 0.1:
                note = np.nan

            data.append({
                "student_id": student_id,
                "annee_academique": ACADEMIC_YEAR,
                "departement_code": student_dept_code,
                "departement_nom": DEPARTMENTS[student_dept_code],
                "ue_code": ue_code,
                "ue_nom": ue_name,
                "note": note,
                "enseignants": ue_teachers.get(ue_code, "")
            })

    print(f"Generated {len(data)} records.")
    return pd.DataFrame(data)

def main():
    """Main function to run the script."""
    print("--- Starting Data Simulation Script ---")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    # Generate and save the dataset
    ue_teachers_mapping = generate_teachers()
    df = generate_dataset(ue_teachers_mapping)

    try:
        df.to_csv(OUTPUT_FILE, index=False, sep=';', decimal=',')
        print(f"Successfully saved dataset to: {OUTPUT_FILE}")
    except IOError as e:
        print(f"Error saving file: {e}")

    print("--- Data Simulation Script Finished ---")

if __name__ == "__main__":
    main()