# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import Http404
from django.test import Client
from django.test import TestCase, RequestFactory

from LabModule.models import MaquinaProfile, LaboratorioProfile
from .views import maquina_create, maquina_update

c = Client(HTTP_USER_AGENT='Mozilla/5.0')

User = get_user_model()

class MaquinasTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        with transaction.atomic():
                self.user = User.objects.create_superuser(
                    username='jacob',
                    email='j@a.com',
                    user_code='fsfwef',
                    first_name='hola',
                    last_name='hola',
                    user_phone=43535,
                    password='top_secret')
        c.login(username=self.user.username, password='top_secret')

        self.LaboratorioPrueba = LaboratorioProfile.objects.create(nombre="Laboratorio genetica", id="LAB_101")

        self.maquinaPrueba = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_010",
            "con_reserva": False,
            "xPos": 0,
            "yPos": 0,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina1 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_001",
            "con_reserva": False,
            "xPos": 10,
            "yPos": 10,
            "idLaboratorio": self.LaboratorioPrueba.id
        }
        self.maquina2 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_002",
            "con_reserva": False,
            "xPos": 0,
            "yPos": 0,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina3 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_010",
            "con_reserva": False,
            "xPos": 1,
            "yPos": 1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina4 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_004",
            "con_reserva": False,
            "xPos": 2,
            "yPos": 2,
            "idLaboratorio": "No existente"
        }

        self.maquina5 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_005",
            "con_reserva": False,
            "xPos": -1,
            "yPos": -1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina6 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_005",
            "con_reserva": False,
            "xPos": 100,
            "yPos": 3,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina7 = {
            "nombre": "Autoclave Portátil",
            "descripcion": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_005",
            "con_reserva": False,
            "xPos": 3,
            "yPos": 100,
            "idLaboratorio": self.LaboratorioPrueba.id
        }
        self.maquina8 = {
            "nombres": "Autoclave Portátil",
            "descripcions": "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema": "AUTO_008",
            "con_reserva": False,
            "xPos": 1,
            "yPos": 1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        request = self.factory.post('/maquina/add', data=self.maquinaPrueba)
        request.user = self.user
        maquina_create(request)

    def test_PermisoAgregar(self):
        request = self.factory.get('/maquina/add', follow=True)
        request.user = AnonymousUser()
        response = maquina_create(request)
        self.assertEqual(response.status_code, 401, "No debe estar autorizado")

        request.user = self.user

        response = maquina_create(request)
        self.assertEqual(response.status_code, 200, "Debe estar autorizado")

