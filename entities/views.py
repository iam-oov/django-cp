from re import template
from django.http import Http404
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from django.core.cache import cache
from django.http import JsonResponse
import json


from entities import models
from .tasks import load_db


class CodeDetail(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, zip_code, format=None):
        entities = models.Entity.objects.filter(zip_code=zip_code)

        if not entities:
            raise Http404()

        # get cache
        data_in_redis = cache.get(zip_code)
        if data_in_redis:
            return JsonResponse(json.loads(data_in_redis))

        context = {}

        for (i, entity) in enumerate(entities):
            if i == 0:
                context['zip_code'] = entity.zip_code
                context['locality'] = entity.locality.upper()
                context['municipality'] = {
                    'key': entity.settlement.municipality.key,
                    'name': entity.settlement.municipality.name.upper(),
                }
                context['federal_entity'] = {
                    'key': entity.settlement.municipality.federal_entity.key,
                    'name': entity.settlement.municipality.federal_entity.name.upper(),
                    'code': entity.settlement.municipality.federal_entity.code,
                }
                context['settlements'] = []

            context['settlements'].append({
                'key': entity.settlement.type,
                'name': entity.settlement.name,
                'zone_type': entity.settlement.zone_type,
                'settlement_type': {
                    'name': entity.settlement.type.upper()
                }
            })

        # set in cache
        cache.set(zip_code, json.dumps(context))

        return JsonResponse(context)


class load_db(APIView):
    def get(self, request):
        email = request.query_params.get('email') or ''
        _template = request.query_params.get('template') or ''

        load_db.delay(email, _template)

        prefix = 'La operacion de cargado tarda aprox. 15 min.'
        if email:
            return JsonResponse({
                'msg': f'{prefix} Se te enviara un correo a {email} al finalizar la operacion.'
            })

        return JsonResponse({'msg': f'{prefix}'})
