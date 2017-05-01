# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LabModule.app_models.Experimento import Experimento


@csrf_exempt
def cargar_experimentos(request):
    """Realiza el cargue de datos de experimentos existentes por identificador del proyecto
                Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una Maquina normal en una
                franja de tiempo especifica para hacer uso de ella
                Se encarga de:
                    * Cargue de datos de experimentos
                :param request: El HttpRequest que se va a responder.
                :type request: HttpRequest.
                :returns: HttpResponse -- La información de experimentos existentes por identificador del proyecto
            """
    if request.GET['project_id'] != "":
        experiments = Experimento.objects.filter(projecto = request.GET['project_id'])
        experiments_dict = dict([(c.id, c.nombre) for c in experiments])
        return HttpResponse(json.dumps(experiments_dict))
    else:
        return HttpResponse()
