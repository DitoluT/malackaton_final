# /var/www/malackaton/wsgi.py

import sys
import os

# Agrega la ruta de tu aplicación al sys.path
sys.path.insert(0, '/var/www/malackaton')

# Configura el entorno si estás utilizando un entorno virtual (opcional)
# activar_este = '/ruta/a/tu/entorno/virtual/bin/activate_this.py'
# exec(open(activar_este).read(), dict(__file__=activar_este))

# Importa la aplicación Flask desde el módulo correspondiente
from app import create_app

# Crea la aplicación
application = create_app()

# No es necesario el bloque if __name__ == "__main__" cuando se usa WSGI

