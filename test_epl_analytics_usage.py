from epl_analytics import EPLAnalytics, analysis
import os

# Ensure the data directory exists and the CSV is present
# This assumes the '1_generate_dataset.py' script has been run
data_file_path = 'data/notes_epl_simulees.csv'

if not os.path.exists(data_file_path):
    print(f"Error: Data file not found at {data_file_path}")
    print("Please run 'python scripts/1_generate_dataset.py' first to generate the data.")
else:
    print(f"Loading data from {data_file_path}...")
    epl_data = EPLAnalytics.from_csv(data_file_path)

    if epl_data:
        print("\n--- EPLAnalytics Object loaded ---")
        print(f"Data loaded successfully! DataFrame shape: {epl_data.data.shape}")

        # In a script, the __repr__ method is called
        print(repr(epl_data))

        print("\n--- Displaying head of the DataFrame directly ---")
        print(epl_data.data.head())

        print("\n--- Performing analyses ---")

        # Calculate statistics by department
        print("\nCalculating statistics by department:")
        stats_departement = analysis.calculate_stats_by_group(epl_data.data, 'departement_nom')
        print(stats_departement)

        # Calculate statistics by teacher
        print("\nCalculating statistics by teacher:")
        stats_enseignant = analysis.calculate_teacher_stats(epl_data.data)
        print(stats_enseignant)

    else:
        print("Failed to load EPLAnalytics data.")
