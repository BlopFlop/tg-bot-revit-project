import sys

from google_tab import get_backup_paths
from models_revit_server import start_load_models

if __name__ == '__main__':
    start_load_models(get_backup_paths())
    sys.exit()
