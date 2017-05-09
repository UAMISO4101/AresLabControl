# -*- coding: utf-8 -*-
from django.shortcuts import render


def home(request, template_name = "home.html"):
    """Metodo inicial de la aplicación
               Se encarga de:
                   * Mostrar el inicio de la aplicación
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :returns: HttpResponse -- La respuesta redirigiendo a la página home inicial de la aplicación
        """
    context = {}
    return render(request, template_name, context)
