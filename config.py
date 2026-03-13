

from datetime import datetime
from pathlib import Path



TODAY = datetime.now().strftime('%d-%m-%Y_%H-%M')
BASE_DIR_EXCEL = Path('output')
BASE_DIR_EXCEL.mkdir(parents=True, exist_ok=True)

FILE_EXCEL = BASE_DIR_EXCEL / f"donnée_vente_E-commerce_{TODAY}.xlsx"