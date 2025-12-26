from epl_analytics import EPLAnalytics, analysis
import os

# S'assurer que le répertoire de données existe et que le CSV est présent
# Ceci suppose que le script '1_generate_dataset.py' a été exécuté
data_file_path = 'data/notes_epl_simulees.csv'

if not os.path.exists(data_file_path):
    print(f"Erreur : Fichier de données non trouvé à l'adresse {data_file_path}")
    print("Veuillez d'abord exécuter 'python scripts/1_generate_dataset.py' pour générer les données.")
else:
    print(f"Chargement des données depuis {data_file_path}...")
    epl_data = EPLAnalytics.from_csv(data_file_path)

    if epl_data:
        print("\n--- Objet EPLAnalytics chargé ---")
        print(f"Données chargées avec succès ! Forme du DataFrame : {epl_data.data.shape}")

        # Dans un script, la méthode __repr__ est appelée
        print(repr(epl_data))

        print("\n--- Affichage direct de l'en-tête du DataFrame ---")
        print(epl_data.data.head())

        # --- Exécution des analyses ---

        # Calculer les statistiques par département
        print("\nCalcul des statistiques par département :")
        stats_departement = analysis.calculate_stats_by_group(epl_data.data, 'departement_nom')
        print(stats_departement)

        # Calculer les statistiques par enseignant
        print("\nCalcul des statistiques par enseignant :")
        stats_enseignant = analysis.calculate_teacher_stats(epl_data.data)
        print(stats_enseignant)

    else:
        print("Échec du chargement des données EPLAnalytics.")
