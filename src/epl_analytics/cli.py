@app.command(name="classer-etudiants")
def rank_students_cli(
    fichier: Annotated[
        str,
        typer.Argument(help="Chemin complet vers le fichier de données CSV contenant les notes.")
    ],
    grouper_par: Annotated[
        str,
        typer.Option("--grouper-par", "-g", help="[Obligatoire] Colonne pour grouper les étudiants (ex: 'ue_nom', 'matiere', 'departement_nom').")
    ],
    sortie: Annotated[
        str,
        typer.Option("--sortie", "-s", help="[Optionnel] Chemin pour sauvegarder les résultats du classement. Format .csv ou .xlsx.")
    ] = None
):
    """
    Classe les étudiants par note au sein de chaque groupe spécifié.
    Affiche le classement des étudiants par note décroissante à l'intérieur de chaque groupe.

    Exemple d'utilisation :

    `epl-analytics classer-etudiants data/notes_epl_simulees.csv --grouper-par ue_nom`

    Pour sauvegarder les résultats :

    `epl-analytics classer-etudiants data/notes_epl_simulees.csv -g departement_nom -s classement_departement.xlsx`
    """
    try:
        df = pd.read_csv(fichier, sep=';', decimal=',')
        df['note'] = pd.to_numeric(df['note'], errors='coerce')

        # Assurez-vous que la colonne de groupement existe
        if grouper_par not in df.columns:
            console.print(f"[bold red]Erreur :[/bold red] La colonne '{grouper_par}' n'existe pas dans le fichier de données.")
            raise typer.Exit(code=1)

        ranked_df = analysis.rank_students(df, grouper_par)

        console.print(f"\n:trophy: [bold green]Classement des étudiants par '{grouper_par}':[/bold green]")
        
        table = Table(show_header=True, header_style="bold magenta")
        for col in ranked_df.columns:
            table.add_column(col)
        
        for _, row in ranked_df.iterrows():
            table.add_row(*[str(item) for item in row.values])
        console.print(table)
        
        if sortie:
            save_df(ranked_df, sortie)

    except FileNotFoundError:
        console.print(f"[bold red]Erreur :[/bold red] Fichier non trouvé à '{fichier}'. Veuillez vérifier le chemin.")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Une erreur est survenue lors du classement des étudiants :[/bold red] {e}")
        raise typer.Exit(code=1)