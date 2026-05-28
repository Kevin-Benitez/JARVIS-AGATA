import subprocess, sys

def terminal(parameters=None, player=None, speak=None, **kwargs):
    if not parameters:
        return "No se especificó el comando."
    cmd = parameters.get("command", "").strip()
    timeout = parameters.get("timeout", 30)
    cwd = parameters.get("cwd", None)
    if not cmd:
        return "Comando vacío."
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=cwd, encoding="utf-8", errors="replace"
        )
        output = (result.stdout + result.stderr).strip()
        return output[:2000] if output else "Comando ejecutado sin salida."
    except subprocess.TimeoutExpired:
        return f"El comando superó el tiempo límite de {timeout}s."
    except Exception as e:
        return f"Error al ejecutar comando: {e}"
