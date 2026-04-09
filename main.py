


from config import LOG_FILE, BRUTE_DATA_FILE, MAX_RETRIES, DELAY, BRUTE_DATA_CLEAN_FILE, EXCEL_FILE


from src import logging_file
from src import extracting_data_file_csv, cleanning_brute_data, add_features
from src import analysis_by_categories, analysis_by_city, analysis_by_status
from src import reporting_excel




logging_file(LOG_FILE)
brute_data = extracting_data_file_csv(BRUTE_DATA_FILE, MAX_RETRIES, DELAY)
clean_data = cleanning_brute_data(brute_data, BRUTE_DATA_CLEAN_FILE)
complet_data = add_features(clean_data)
analyse_category = analysis_by_categories(complet_data)
analyse_city = analysis_by_city(complet_data)
analyse_status = analysis_by_status(complet_data)


onglets = {
    'Données Brutes' : brute_data,
    'Données Néttoyées au Complet' : clean_data,
    'Données Par Catégories' : analyse_category,
    'Données Par City' : analyse_city,
    'Données Par Status' : analyse_status
}

reporting_excel(EXCEL_FILE, onglets)


