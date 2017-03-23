# Create your tests here.
# -*- coding: utf-8 -*-
#from __future__ import absolute_import
from django.test import Client

from django.http import Http404
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .views import maquina_create,maquina_update, crear_solicitud_muestra
from LabModule.models import MaquinaEnLab,MaquinaProfile,LaboratorioProfile


c = Client(HTTP_USER_AGENT='Mozilla/5.0')

class MaquinasTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='jacob', email='jacob@…', password='top_secret')
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

        self.maquina1= {
            "nombre":"Autoclave Portátil",
            "descripcion":"Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema":"AUTO_001",
            "con_reserva":False,
            "xPos":10,
            "yPos":10,
            "idLaboratorio":self.LaboratorioPrueba.id
        }
        self.maquina2= {
            "nombre":"Autoclave Portátil",
            "descripcion":"Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema":"AUTO_002",
            "con_reserva":False,
            "xPos":0,
            "yPos":0,
            "idLaboratorio":self.LaboratorioPrueba.id
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
        self.maquina8= {
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
        request = self.factory.get('/maquina/add',follow=True)
        request.user = AnonymousUser()
        response = maquina_create(request)
        self.assertEqual(response.status_code,401,"No debe estar autorizado")

        request.user = self.user

        response = maquina_create(request)
        self.assertEqual(response.status_code, 200, "Debe estar autorizado")


    def test_ModificarMaquina(self):
        request = self.factory.get('/maquina/1',follow=True)
        request.user = AnonymousUser()
        response = maquina_update(request,1)
        self.assertEqual(response.status_code, 401, "No debe estar autorizado")
        request.user = self.user
        try:
            response = maquina_update(request,1)
            self.fail("No deberia existir la maquina")
        except Http404:
            pass



    def test_agregarMaquina(self):

        request = self.factory.post('/maquina/add', data=self.maquina1)
        request.user = self.user
        response = maquina_create(request)
        eMaquina=MaquinaProfile.objects.filter(pk="AUTO_001").exists()
        self.assertEqual(eMaquina, True, "Debe añadirlo")

    def test_agregarOcupado(self):
        request = self.factory.post('/maquina/add', data=self.maquina2)
        request.user = self.user
        response = maquina_create(request)
        eMaquina=MaquinaProfile.objects.filter(pk="AUTO_002").exists()
        self.assertEqual(eMaquina, False, "El campo ya esta ocupado")

    def  test_AgregarIdRepetido(self):

        request = self.factory.post('/maquina/add', data=self.maquina3)
        request.user = self.user
        response = maquina_create(request)
        con=MaquinaProfile.objects.filter(con_reserva=False).count()
        eMaquina = con==1
        self.assertEqual(eMaquina, True, "Deberia solo haber una maquia pero hay "+str(con))


    def  test_AgregarLaboratorioInexistente(self):

        request = self.factory.post('/maquina/add', data=self.maquina4)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk="AUTO_004").exists()
        self.assertEqual(eMaquina, False, "El laboratorio no es valido")


    def  test_AgregarPosicionNegativa(self):

        request = self.factory.post('/maquina/add', data=self.maquina5)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk="AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")


    def  test_AgregarxSuperior(self):

        request = self.factory.post('/maquina/add', data=self.maquina6)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk="AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")


    def  test_AgregarySuperior(self):

        request = self.factory.post('/maquina/add', data=self.maquina7)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk="AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")


    def  test_AgregarCamposInvalidos(self):

        request = self.factory.post('/maquina/add', data=self.maquina8)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk="AUTO_008").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")











