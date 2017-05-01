# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LabModule.app_models.Protocolo import Protocolo


@csrf_exempt
def cargar_protocolos(request):
    """Realiza el cargue de datos de protocolos existentes por identificador del experimento
                  Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una Maquina normal en una
                  franja de tiempo especifica para hacer uso de ella
                  Se encarga de:
                      * Cargue de datos de protocolos
                  :param request: El HttpRequest que se va a responder.
                  :type request: HttpRequest.
                  :returns: HttpResponse -- La información de protocolos existentes por identificador del experimento
              """
    if request.GET['experiment_id'] != "":
        protocols = Protocolo.objects.filter(experimento = request.GET['experiment_id'])
        protocols_dict = dict([(c.id, c.nombre) for c in protocols])
        return HttpResponse(json.dumps(protocols_dict))
    else:
        return HttpResponse()
