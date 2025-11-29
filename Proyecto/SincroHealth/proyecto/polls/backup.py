import os
import shutil
from datetime import datetime, timedelta
from django.conf import settings

def generar_backup():
    base_path = settings.BASE_DIR
    db_path = os.path.join(base_path, "db.sqlite3")
    backups_dir = os.path.join(base_path, "backups")

    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{fecha}.sqlite3"

    destino = os.path.join(backups_dir, backup_name)

    shutil.copy2(db_path, destino)
    print(f"Backup generado: {destino}")

    limite = datetime.now() - timedelta(days=30)

    for archivo in os.listdir(backups_dir):
        ruta_archivo = os.path.join(backups_dir, archivo)

        if os.path.isfile(ruta_archivo):
            fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            if fecha_mod < limite:
                os.remove(ruta_archivo)
                print(f"Backup eliminado por antigüedad: {archivo}")
