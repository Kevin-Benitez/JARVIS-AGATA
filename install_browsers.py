#!/usr/bin/env python
import subprocess
import sys

# Instalar los navegadores de Playwright
subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
print("✓ Navegadores de Playwright instalados correctamente")
