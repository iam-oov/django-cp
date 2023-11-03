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
        settlements = []

        # context.zip_code =

        for entity in entities:
            federal_entity = entity.federal_entity_r
            municipality = federal_entity.municipality_r
            settlement = municipality.settlement_r
            settlements.append(settlement)

        serialized_settlements = []

        for settlement in settlements:
            settlement_data = {
                'slug': settlement.slug,
                'key': settlement.key,
                'name': settlement.name,
                'zone_type': settlement.zone_type,
                'type': settlement.type,
            }
            serialized_settlements.append(settlement_data)

        return JsonResponse(context)
