import time
import datetime
import os
import pandas as pd

from celery import shared_task
from slugify import slugify
from django.conf import settings
from django.core.mail import send_mail

from entities import models


@shared_task
def load_db(email, template):
    pathFileCSV = settings.SEED_CP
    if template in ['basic']:
        print('---yayaiii')
        pathFileCSV = settings.SEED_BASIC

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

    if email:
        send_mail(
            "Carga terminada!",
            "Los codigos postales han sido cargos exitosamente en la base de datos.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )


@shared_task(name="print_msg_main")
def print_message(message, *args, **kwargs):
    print(f"Celery is working!! Message is {message}")
