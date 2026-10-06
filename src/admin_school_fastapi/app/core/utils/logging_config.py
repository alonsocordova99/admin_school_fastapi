import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Crear carpeta de logs si no existe
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Ruta del archivo de log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configurar logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Handler rotativo (un archivo por día, guarda 7 días)
handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",    # "S" segundos, "M" minutos, "H" horas, "D" días, "midnight"
    interval=1,
    backupCount=7,      # cantidad de archivos antiguos que conserva
    encoding="utf-8"
)

# Formato del log
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
handler.setFormatter(formatter)

# Agregar handler al logger
logger.addHandler(handler)