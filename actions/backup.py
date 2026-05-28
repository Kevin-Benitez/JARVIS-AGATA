import os, shutil
from datetime import datetime

def backup(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action  = parameters.get("action", "run")
    source  = parameters.get("source", "")
    destination = parameters.get("destination", "")

    if not source or not os.path.exists(source):
        return f"Origen no encontrado: {source}"

    if action == "run":
        if not destination:
            destination = os.path.join(os.path.expanduser("~"), "Desktop", "Backups")
        os.makedirs(destination, exist_ok=True)
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = os.path.basename(source.rstrip("\\/"))
        dest_path = os.path.join(destination, f"{name}_{ts}")
        try:
            if os.path.isdir(source):
                shutil.copytree(source, dest_path)
            else:
                shutil.copy2(source, dest_path)
            return f"Backup completado: {dest_path}"
        except Exception as e:
            return f"Error al hacer backup: {e}"

    return f"Acción de backup '{action}' no reconocida."
