from django.http import Http404
from rest_framework.views import APIView
from django.http import JsonResponse


from entities import models


class CodeDetail(APIView):
    def get(self, request, zip_code, format=None):
        entities = models.Entity.objects.filter(zip_code=zip_code)

        if not entities:
            raise Http404()

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

        return JsonResponse(context)
