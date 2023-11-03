# -*- coding: utf-8 -*-

import os, sys
import pandas as pd
from slugify import slugify

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
pathFileCSV = os.path.join(BASE_DIR, 'seeds/CPdescarga.txt')

SAVE_DATABASE = True

data = pd.read_csv(
  pathFileCSV,
  sep='|',
  encoding='utf8',
  na_filter=False,  # empty fields as empty strings
  dtype={
    'id_asenta_cpcons': str,
    'c_mnpio': str,
    'c_estado': str,
    'd_codigo': str
  }
)

print('Loading...')

for row in data.itertuples():
  # initialize variables
  config = {
    'settlement': {
      'slug': slugify(f'{row.d_asenta} {row.id_asenta_cpcons}'),
      'key': row.id_asenta_cpcons,
      'name': row.d_asenta,
      'zone_type': row.d_asenta,
      'type': row.d_zona
    },
    'municipality': {
      'slug': slugify(f'{row.c_mnpio} {row.D_mnpio}'),
      'key': row.c_mnpio,
      'name': row.D_mnpio
    },
    'federal_entity': {
      'slug': slugify(f'{row.c_estado} {row.d_estado}'),
      'key': row.c_estado,
      'name': row.d_estado
    },
    'entity': {
      'slug': slugify('{0} {1} {2} {3}'.format(
        row.d_codigo,
        row.d_ciudad,
        row.id_asenta_cpcons,
        row.D_mnpio
      )),
      'zip_code': row.d_codigo,
      'locality': row.d_ciudad
    }
  }

  if SAVE_DATABASE:
        # get or create: FederalEntity
        federal_entity, created = models.FederalEntity.objects.get_or_create(
            slug=config['federal_entity']['slug'],
            defaults={
                'key': config['federal_entity']['key'],
                'name': config['federal_entity']['name'],
            }
        )

        # get or create: Municipality
        municipality, created = models.Municipality.objects.get_or_create(
            slug=config['municipality']['slug'],
            defaults={
                'key': config['municipality']['key'],
                'name': config['municipality']['name'],
                'federal_entity': federal_entity
            }
        )

        if (not created):
            municipality.federal_entity = federal_entity
            municipality.save()

        # get or create: Settlement
        settlement, created = models.Settlement.objects.get_or_create(
            slug=config['settlement']['slug'],
            defaults={
                'key': config['settlement']['key'],
                'name': config['settlement']['name'],
                'zone_type': config['settlement']['zone_type'],
                'type': config['settlement']['type'],
                'municipality': municipality
            }
        )

        if (not created):
            settlement.municipality = municipality
            settlement.save()

        # get or create: Entity
        entity, created = models.Entity.objects.get_or_create(
            slug=config['entity']['slug'],
            defaults={
                'zip_code': config['entity']['zip_code'],
                'locality': config['entity']['locality'] or '',
                'settlement': settlement
            }
        )

        if (not created):
            entity.settlement = settlement
            entity.save()

print('Ready!')
