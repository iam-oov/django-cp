from django.http import Http404
from rest_framework.views import APIView
from django.http import JsonResponse
import json

from entities import models
from .utils import get_redis
from .tasks import loadDb


class CodeDetail(APIView):
    def get(self, request, zip_code, format=None):
        entities = models.Entity.objects.filter(zip_code=zip_code)

        if not entities:
            raise Http404()

        # get cache
        data_in_redis = get_redis().get(zip_code)
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

        # save in cache
        get_redis().set(zip_code, json.dumps(context))

        return JsonResponse(context)


class LoadDb(APIView):
    def get(self, request):
        email = request.query_params.get('email') or ''
        loadDb.delay(email)

        prefix = 'La operacion de cargado tarda aprox. 15 min.'
        if email:
            return JsonResponse({
                'msg': f'{prefix} Se te enviara un correo a {email} al finalizar la operacion.'
            })

        return JsonResponse({'msg': f'{prefix}'})
