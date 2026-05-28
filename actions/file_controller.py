import os, shutil, glob

SHORTCUTS = {
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "home": os.path.expanduser("~"),
}

def _resolve(path):
    if not path:
        return os.path.expanduser("~")
    return SHORTCUTS.get(path.lower().strip(), os.path.expandvars(path))

def file_controller(parameters=None, player=None, **kwargs):
    if not parameters:
        return "No se especificó la acción."
    action = parameters.get("action", "list")
    path   = _resolve(parameters.get("path", ""))

    if action == "list":
        try:
            items = os.listdir(path)
            return f"Contenido de {path}:\n" + "\n".join(items[:30])
        except Exception as e:
            return f"Error al listar: {e}"

    if action == "create_file":
        name    = parameters.get("name", "nuevo.txt")
        content = parameters.get("content", "")
        full    = os.path.join(path, name)
        try:
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Archivo creado: {full}"
        except Exception as e:
            return f"Error al crear archivo: {e}"

    if action == "create_folder":
        name = parameters.get("name", "nueva_carpeta")
        full = os.path.join(path, name)
        try:
            os.makedirs(full, exist_ok=True)
            return f"Carpeta creada: {full}"
        except Exception as e:
            return f"Error al crear carpeta: {e}"

    if action == "delete":
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return f"Eliminado: {path}"
        except Exception as e:
            return f"Error al eliminar: {e}"

    if action == "move":
        dest = _resolve(parameters.get("destination", ""))
        try:
            shutil.move(path, dest)
            return f"Movido a: {dest}"
        except Exception as e:
            return f"Error al mover: {e}"

    if action == "copy":
        dest = _resolve(parameters.get("destination", ""))
        try:
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(dest, os.path.basename(path)))
            else:
                shutil.copy2(path, dest)
            return f"Copiado a: {dest}"
        except Exception as e:
            return f"Error al copiar: {e}"

    if action == "rename":
        new_name = parameters.get("new_name", "")
        new_path = os.path.join(os.path.dirname(path), new_name)
        try:
            os.rename(path, new_path)
            return f"Renombrado a: {new_name}"
        except Exception as e:
            return f"Error al renombrar: {e}"

    if action == "read":
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(3000)
            return content
        except Exception as e:
            return f"Error al leer: {e}"

    if action == "write":
        content = parameters.get("content", "")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Escrito en: {path}"
        except Exception as e:
            return f"Error al escribir: {e}"

    if action == "find":
        name = parameters.get("name", "")
        ext  = parameters.get("extension", "")
        pattern = f"**/*{name}*{ext}" if name else f"**/*{ext}"
        try:
            results = glob.glob(os.path.join(path, pattern), recursive=True)[:10]
            return "\n".join(results) if results else "No se encontraron archivos."
        except Exception as e:
            return f"Error al buscar: {e}"

    if action == "disk_usage":
        try:
            usage = shutil.disk_usage(path)
            total = usage.total // (1024**3)
            used  = usage.used  // (1024**3)
            free  = usage.free  // (1024**3)
            return f"Disco: Total={total}GB | Usado={used}GB | Libre={free}GB"
        except Exception as e:
            return f"Error al obtener uso de disco: {e}"

    if action == "info":
        try:
            stat = os.stat(path)
            return (f"Ruta: {path}\nTamaño: {stat.st_size} bytes\n"
                    f"Es directorio: {os.path.isdir(path)}")
        except Exception as e:
            return f"Error: {e}"

    return f"Acción '{action}' no reconocida."
