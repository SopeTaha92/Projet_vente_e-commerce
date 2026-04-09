


import sys
import time
import pandas as pd 
from loguru import logger


def extracting_data_file_csv(file : str, max_retries : int, delay : int):
    """La fonction qui recupére les données depuis la source ici un fichier csv"""
    logger.info("Début de l'extraction des données brutes")

    for retry in range(max_retries):
        try:
            df_brute = pd.read_csv(file)
            logger.success("Extraction des données brutes effectués avec succée")
            return df_brute
        except FileNotFoundError as e:
            logger.error(f"Erreur lors de l'extraction fichier {file} introuvable : {e}")
            if retry < max_retries - 1:
                logger.info(f"Echec de la tentative {retry+1} / {max_retries}. Nouvelle tentative dans {delay} secondes")
                time.sleep(delay)
                delay *= 2


    logger.critical(f"Echec total aprés {max_retries} tentatives")
    sys.exit("Arret du programme :  impossible de chargé la source de donnée")


