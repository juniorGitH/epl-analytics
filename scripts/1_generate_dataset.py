# scripts/1_generate_dataset.py
"""
Génère un jeu de données simulé de notes d'étudiants pour l'EPL et l'enregistre dans un fichier CSV.
Le jeu de données inclut des scénarios complexes comme plusieurs enseignants pour une seule unité d'enseignement (UE).
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

# --- Définitions des données ---
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
    """Assigne un ou deux enseignants à chaque UE."""
    ue_teachers = {}
    for dept_ues in UES.values():
        for ue_code, _ in dept_ues:
            num_teachers = random.choices([1, 2], weights=[0.7, 0.3], k=1)[0]
            assigned_teachers = random.sample(TEACHERS, k=num_teachers)
            ue_teachers[ue_code] = ";".join(assigned_teachers) # Utiliser un séparateur pour les UE à plusieurs enseignants
    return ue_teachers

def generate_dataset(ue_teachers):
    """Génère l'ensemble complet des données."""
    print("Génération du jeu de données...")
    data = []
    student_ids = [f"etu_{2024000 + i}" for i in range(NUM_STUDENTS)]

    for student_id in student_ids:
        # Assigner un département aléatoire à chaque étudiant
        student_dept_code = random.choice(list(DEPARTMENTS.keys()))

        # Chaque étudiant suit toutes les UE de son département
        for ue_code, ue_name in UES[student_dept_code]:
            # Simuler une distribution de notes réaliste (moyenne autour de 12, écart-type autour de 3)
            # Ajouter un peu d'aléatoire à la moyenne pour chaque UE
            base_mean = random.uniform(9, 14)
            note = np.random.normal(loc=base_mean, scale=3.5)
            note = np.clip(round(note, 2), 0, 20) # Limiter les notes entre 0 et 20

            # 10% de chance d'être absent (note NaN)
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

    print(f"Généré {len(data)} enregistrements.")
    return pd.DataFrame(data)

def main():
    """Fonction principale pour exécuter le script."""
    print("--- Début du script de simulation de données ---")
    
    # S'assurer que le répertoire de sortie existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Répertoire créé : {OUTPUT_DIR}")

    # Générer et enregistrer le jeu de données
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