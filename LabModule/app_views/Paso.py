# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LabModule.app_models.Paso import Paso


@csrf_exempt
def cargar_pasos(request):
    """Realiza el cargue de datos de pasos existentes por identificador del protocolo
                    Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una Maquina normal en
                    una franja de tiempo especifica para hacer uso de ella
                    Se encarga de:
                        * Cargue de datos de pasos
                    :param request: El HttpRequest que se va a responder.
                    :type request: HttpRequest.
                    :returns: HttpResponse -- La información de pasos existentes por identificador del protocolo
                """
    if request.GET['protocol_id'] != "":
        steps = Paso.objects.filter(protocolo = request.GET['protocol_id'])
        steps_dict = dict([(c.id, c.nombre) for c in steps])
        return HttpResponse(json.dumps(steps_dict))
    else:
        return HttpResponse()
