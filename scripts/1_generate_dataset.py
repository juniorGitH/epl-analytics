# scripts/1_generate_dataset.py
"""
Génère un jeu de données simulé de notes d'étudiants pour l'EPL et l'enregistre dans un fichier CSV.
Le jeu de données inclut des scénarios complexes comme plusieurs enseignants pour une seule unité d'enseignement (UE).
"""
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# --- Configuration ---
NUM_STUDENTS = 80
ACADEMIC_YEAR = "2024-2025"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "notes_epl_simulees.csv")

# --- Définitions des données ---
DEPARTMENTS = {
    "INFO": "Informatique",
    "MECA": "Mécanique",
    "ELEC": "Électricité",
    "GC": "Génie Civil",
    "MAP": "Mathématiques Appliquées",
}

# Données pour la génération de noms et de genres
FIRST_NAMES_MALE = ["Jean", "Pierre", "Michel", "André", "Louis", "Paul", "Nicolas", "Julien", "Antoine", "Frédéric"]
FIRST_NAMES_FEMALE = ["Marie", "Sophie", "Isabelle", "Nathalie", "Catherine", "Anne", "Chantal", "Céline", "Émilie", "Sandrine"]
LAST_NAMES = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]

TEACHERS = [
    {"nom": "Dubois", "prénom": "Alain", "sex": "M", "date_de_naissance": "1975-05-10"},
    {"nom": "Lambert", "prénom": "Sophie", "sex": "F", "date_de_naissance": "1982-11-23"},
    {"nom": "Martin", "prénom": "Bernard", "sex": "M", "date_de_naissance": "1968-01-15"},
    {"nom": "Bernard", "prénom": "Isabelle", "sex": "F", "date_de_naissance": "1985-07-02"},
    {"nom": "Petit", "prénom": "Gérard", "sex": "M", "date_de_naissance": "1970-09-18"},
    {"nom": "Durand", "prénom": "Nicole", "sex": "F", "date_de_naissance": "1978-03-30"},
    {"nom": "Leroy", "prénom": "Patrick", "sex": "M", "date_de_naissance": "1980-12-05"},
    {"nom": "Moreau", "prénom": "Valérie", "sex": "F", "date_de_naissance": "1988-06-21"},
    {"nom": "Simon", "prénom": "Christophe", "sex": "M", "date_de_naissance": "1972-08-11"},
    {"nom": "Laurent", "prénom": "Martine", "sex": "F", "date_de_naissance": "1983-04-14"},
]

# Définition des matières et de leur lien avec les UEs
MATIERES = {
    "Programmation et Algorithmique": ["LINFO1101", "LINFO1252"],
    "Systèmes et Architecture": ["LINFO1102"],
    "Mécanique des Structures et des Fluides": ["LMECA1120", "LGCIV1071"],
    "Conception et Fabrication": ["LMECA1510", "LMECA1901"],
    "Électronique et Circuits": ["LELEC1370", "LELEC1755"],
    "Sciences des Matériaux": ["LGCIV1022"],
    "Analyse et Algèbre": ["LMAPR1015", "LMAPR1016"],
}

# Créer un mapping inversé de UE -> Matière
UE_TO_MATIERE = {ue: matiere for matiere, ues in MATIERES.items() for ue in ues}

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
    """Assigne un ou deux enseignants à chaque UE."""
    ue_teachers = {}
    teacher_full_names = [f"{t['prénom']} {t['nom']}" for t in TEACHERS]
    for dept_ues in UES.values():
        for ue_code, _ in dept_ues:
            num_teachers = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
            assigned_teachers = random.sample(teacher_full_names, k=num_teachers)
            ue_teachers[ue_code] = ";".join(assigned_teachers)
    return ue_teachers

def generate_dataset(ue_teachers):
    """Génère l'ensemble complet des données."""
    print("Génération du jeu de données...")
    data = []
    student_ids = [f"etu_{2024000 + i}" for i in range(NUM_STUDENTS)]

    for student_id in student_ids:
        sex = random.choice(["M", "F"])
        if sex == "M":
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)
        last_name = random.choice(LAST_NAMES)
        
        # Générer une date de naissance aléatoire (entre 18 et 25 ans)
        birth_date = datetime.now() - timedelta(days=random.randint(18*365, 25*365))
        
        student_dept_code = random.choice(list(DEPARTMENTS.keys()))

        for ue_code, ue_name in UES[student_dept_code]:
            base_mean = random.uniform(9, 14)
            note = np.random.normal(loc=base_mean, scale=3.5)
            note = np.clip(round(note, 2), 0, 20)

            if random.random() < 0.1:
                note = np.nan

            data.append({
                "student_id": student_id,
                "nom": last_name,
                "prénom": first_name,
                "date_de_naissance": birth_date.strftime('%Y-%m-%d'),
                "sex": sex,
                "annee_academique": ACADEMIC_YEAR,
                "departement_code": student_dept_code,
                "departement_nom": DEPARTMENTS[student_dept_code],
                "matiere": UE_TO_MATIERE.get(ue_code, "N/A"),
                "ue_code": ue_code,
                "ue_nom": ue_name,
                "note": note,
                "enseignants": ue_teachers.get(ue_code, "")
            })

    print(f"Généré {len(data)} enregistrements.")
    return pd.DataFrame(data)

def main():
    """Fonction principale pour exécuter le script."""
    print("--- Début du script de simulation de données ---")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Répertoire créé : {OUTPUT_DIR}")

    ue_teachers_mapping = generate_teachers()
    df = generate_dataset(ue_teachers_mapping)

    try:
        df.to_csv(OUTPUT_FILE, index=False, sep=';', decimal=',')
        print(f"Jeu de données enregistré avec succès dans : {OUTPUT_FILE}")
    except IOError as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")

    print("--- Fin du script de simulation de données ---")

if __name__ == "__main__":
    main()
