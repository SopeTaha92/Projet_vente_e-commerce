📊 Pipeline d'Analyse E-commerce (1M+ lignes)
Ce projet implémente un pipeline ETL (Extract, Transform, Load) robuste capable de traiter des volumes de données importants (jusqu'à 1 000 000 de lignes) pour générer des tableaux de bord décisionnels automatisés sous Excel.

🎯 Objectifs du Projet
Automatisation : Réduire le temps de reporting de plusieurs heures à quelques secondes.

Fiabilité : Gestion des erreurs d'extraction avec un système de "Retry".

Visualisation : Création de graphiques complexes (combinés Column/Line et Pie charts) directement via Python.

🛠️ Stack Technique
Langage : Python 3.13

Manipulation de données : Pandas

Reporting : XlsxWriter (Gestion des formats, graphiques et axes secondaires)

Logging : Loguru (Tracer chaque étape du processus)

📁 Structure du Rapport 

ExcelLe pipeline génère un fichier .xlsx multi-onglets structuré comme suit 

Onglet                    Contenu                                                Type de Visualisation
Données Brutes	            Extraction initiale	                                     Tableau brut
Données Nettoyées	        Données formatées et typées	                             Data propre
Par Catégories	            Analyse de performance	                                 Combiné : Colonnes (Ventes) + Ligne (Prix moyen)
Par City	                Répartition géographique	                             Pie Chart (Part de marché par ville)
Par Status	                Suivi logistique	                                     Multi-Series : Comparaison CA Net vs Remises + Quantités

🚀 Installation & Utilisation
1 - Cloner le dépôt :

Bash    git clone https://github.com/SopeTaha92/Projet_vente_e-commerce.git 
        cd Projet_vente_e-commerce

2 - Installer les dépendances :

Bash

pip install -r requirements.txt

3 - Lancer le pipeline :

Bash

python main.py


📈 Perspectives d'évolution

[ ] Phase 2 : Migration du stockage local (CSV) vers une base de données PostgreSQL.

[ ] Phase 3 : Connexion du pipeline à un outil de BI (Power BI / Tableau).

[ ] Phase 4 : Adaptation des indicateurs pour les différentes secteurs.


Développé par Mahmoud At-Tidiane - Passionné par l'ingénierie des données et l'analyse décisionnelle.
