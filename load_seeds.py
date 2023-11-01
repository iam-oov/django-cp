# -*- coding: utf-8 -*-

import os, sys
import pandas as pd

from django.core.wsgi import get_wsgi_application


# directual actual
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ruta a nuestro proyecto de django
# =====================================================
djangoproject_home = os.path.join(BASE_DIR, 'setup')

# configuracion de arranque de django
# =====================================================
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = get_wsgi_application()

# importamos modelos
# =====================================================
from entities import models

# CODE
# =====================================================
pathFileCSV = os.path.join(BASE_DIR, 'seeds/1-cp.txt')
SAVE_DATABASE = True

data = pd.read_csv(pathFileCSV, sep='|')

for row in data.itertuples():
  print(row.d_tipo_asenta)