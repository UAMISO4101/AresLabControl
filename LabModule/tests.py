# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.http import Http404
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from LabModule.models import LaboratorioProfile
from LabModule.models import MaquinaEnLab
from LabModule.models import MaquinaProfile
from .views import listarMaquinas
from .views import maquina_create
from .views import maquina_update

c = Client(HTTP_USER_AGENT = 'Mozilla/5.0')
CONTRASENA = getattr(settings, "CONTRASENA")


class AddMaquinasTest(TestCase):
    """Prueba los servicios de agregar y editar máquinas
        Se encarga de:
            * Probar la autorización de servicios
            * Probar los servicios de agregar
    """

    def setUp(self):
        """Inicia el estado del test
            Se encarga de :
                * Crear un usario y darle los permisos de agregar y editar
                * Crear un laboratorio
                * Definir varias máquinas que serviran para probar la lógica del negocio
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username = 'john',
                                             email = 'jlennon@beatles.com',
                                             password = CONTRASENA)
        c.login(username = self.user.username, password = CONTRASENA)

        agregar = Permission.objects.get(name = 'maquina||agregar')
        editar = Permission.objects.get(name = 'maquina||editar')
        self.user.user_permissions.add(agregar, editar)
        self.LaboratorioPrueba = LaboratorioProfile.objects.create(nombre = "Laboratorio genetica", id = "LAB_101")

        self.maquinaPrueba = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_010",
            "con_reserva"  : False,
            "posX"         : 0,
            "posY"         : 0,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina1 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_001",
            "con_reserva"  : False,
            "posX"         : 10,
            "posY"         : 10,
            "idLaboratorio": self.LaboratorioPrueba.id
        }
        self.maquina2 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_002",
            "con_reserva"  : False,
            "posX"         : 0,
            "posY"         : 0,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina3 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_010",
            "con_reserva"  : False,
            "posX"         : 1,
            "posY"         : 1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina4 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_004",
            "con_reserva"  : False,
            "posX"         : 2,
            "posY"         : 2,
            "idLaboratorio": "No existente"
        }

        self.maquina5 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_005",
            "con_reserva"  : False,
            "posX"         : -1,
            "posY"         : -1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina6 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_005",
            "con_reserva"  : False,
            "posX"         : 100,
            "posY"         : 3,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        self.maquina7 = {
            "nombre"       : "Autoclave Portátil",
            "descripcion"  : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_005",
            "con_reserva"  : False,
            "posX"         : 3,
            "posY"         : 100,
            "idLaboratorio": self.LaboratorioPrueba.id
        }
        self.maquina8 = {
            "nombres"      : "Autoclave Portátil",
            "descripcions" : "Un autoclave es un recipiente de presión metálico de paredes gruesas con un cierre hermético que permite trabajar a alta presión para realizar una reacción industrial, una cocción o una esterilización con vapor de agua",
            "idSistema"    : "AUTO_008",
            "con_reserva"  : False,
            "posX"         : 1,
            "posY"         : 1,
            "idLaboratorio": self.LaboratorioPrueba.id
        }

        request = self.factory.post('/maquina/add', data = self.maquinaPrueba)
        request.user = self.user
        maquina_create(request)

    def test_PermisoAgregar(self):
        """Comprueba que un usario no autenticado no pueda agregar máquinas.
           También comprueba con un usario con el permiso de agregar máquinas pueda hacerlo
        """
        request = self.factory.get('/maquina/add', follow = True)
        request.user = AnonymousUser()
        response = maquina_create(request)
        self.assertEqual(response.status_code, 401, "No debe estar autorizado")

        request.user = self.user

        response = maquina_create(request)
        self.assertEqual(response.status_code, 200, "Debe estar autorizado")

    def test_ModificarMaquina(self):
        """ Comprueba que un usario no autenticado no pueda editar una máquinas
            tabmíen comprueba que un usuario autenticado pueda hacerlo
        """
        request = self.factory.get('/maquina/', follow = True)
        request.user = AnonymousUser()
        response = maquina_update(request, 1)
        self.assertEqual(response.status_code, 401, "No debe estar autorizado")
        request.user = self.user
        try:
            response = maquina_update(request, 1)
            self.fail("No deberia existir la maquina")
        except Http404:
            pass

    def test_agregarMaquina(self):
        """ Comprueba que el servicio REST de agregar máquinas sea correcto para un usuario autorizado,
            también comprueba que un usario autorizado pueda editar una máquina existente
        """
        request = self.factory.post('/maquina/add', data = self.maquina1)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_001").exists()
        self.assertEqual(eMaquina, True, "El cientifico debe poder agregar máquinas")

        request = self.factory.get('/maquina/')

        request.user = self.user
        response = maquina_update(request, 'AUTO_001')
        self.assertEqual(response.status_code, 200, "El cientifico debe estar autorizado y la máquina existir")

    def test_agregarOcupado(self):
        """Agregar una nueva máquina en un lugar ya ocupado
        """
        request = self.factory.post('/maquina/add', data = self.maquina2)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_002").exists()
        self.assertEqual(eMaquina, False, "El campo ya esta ocupado")

    def test_AgregarIdRepetido(self):
        """Agregar una máquina con un ID ya existente
        """
        request = self.factory.post('/maquina/add', data = self.maquina3)
        request.user = self.user
        response = maquina_create(request)
        con = MaquinaProfile.objects.filter(con_reserva = False).count()
        eMaquina = con == 1
        self.assertEqual(eMaquina, True, "Deberia solo haber una maquia pero hay " + str(con))

    def test_AgregarLaboratorioInexistente(self):
        """Agregar una máquina a un aboratorio inexistente
        """

        request = self.factory.post('/maquina/add', data = self.maquina4)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_004").exists()
        self.assertEqual(eMaquina, False, "El laboratorio no es valido")

    def test_AgregarPosicionNegativa(self):
        """
        Agregar una máquina en una posición invalidad en el laboratorio
        """

        request = self.factory.post('/maquina/add', data = self.maquina5)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")

    def test_AgregarxSuperior(self):
        """Agregar una máquina en una posición x mayor a la capacidad del laboratorio
        """

        request = self.factory.post('/maquina/add', data = self.maquina6)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")

    def test_AgregarySuperior(self):
        """Agregar una máquina en una posición y mayor a la capacidad del laboratorio
        """

        request = self.factory.post('/maquina/add', data = self.maquina7)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_005").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")

    def test_AgregarCamposInvalidos(self):
        """Prueba los campos obligatorios del servicio REST
        """

        request = self.factory.post('/maquina/add', data = self.maquina8)
        request.user = self.user
        response = maquina_create(request)
        eMaquina = MaquinaProfile.objects.filter(pk = "AUTO_008").exists()
        self.assertEqual(eMaquina, False, "La posicion es invalida")


class listMaquinasTest(TestCase):
    """ Se encarga de probar los permissos de listar máquinas
         Se encarga de:
            * Crear usurios y agregarles sus permisos
            * Probar los servicios con cada usuario
    """

    def setUp(self):
        """"Crea un cientifico, un asistente y un jefe para probar sus permisos
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.cientifico = User.objects.create_user(username = 'john',
                                                   email = 'jlennon@beatles.com',
                                                   password = CONTRASENA)
        c.login(username = self.cientifico.username, password = CONTRASENA)

        ver = Permission.objects.get(name = 'maquina||ver')
        self.cientifico.user_permissions.add(ver)
        self.LaboratorioPrueba = LaboratorioProfile.objects.create(nombre = "Laboratorio genetica", id = "LAB_101")
        self.MaquinaPrueba = MaquinaProfile.objects.create(nombre = "prueba",
                                                           descripcion = "Maquina de prueba",
                                                           idSistema = "MAQ001")
        MaquinaEnLab.objects.get_or_create(idLaboratorio = self.LaboratorioPrueba, idMaquina = self.MaquinaPrueba,
                                           posX = 0, posY = 0)

        self.MaquinaPrueba = MaquinaProfile.objects.create(nombre = "Autoclave",
                                                           descripcion = "prueba",
                                                           idSistema = "MAQ002")
        MaquinaEnLab.objects.get_or_create(idLaboratorio = self.LaboratorioPrueba, idMaquina = self.MaquinaPrueba,
                                           posX = 1, posY = 1)

    def test_PermisoVer(self):
        """Comprueba que solo los usarios autorizados puedan ver la lista de máquinas
        """
        request = self.factory.get('/maquina', follow = True)
        request.user = AnonymousUser()
        response = listarMaquinas(request)
        self.assertEqual(response.status_code, 401, "No debe estar autorizado")
        request.user = self.cientifico
        response = listarMaquinas(request)
        self.assertEqual(response.status_code, 200, "El cientifico debe estar autorizado")

    def test_Filtro(self):
        """Comrprueba que el filtro funcione
        """
        request = self.factory.get('/maquina?que=blabla', follow = True)
        request.user = self.cientifico
        response = listarMaquinas(request)
        self.assertEqual(response.status_code, 200, "El cientifico debe estar autorizado")
        self.assertEqual("MAQ001" in response.content, False, "No debe encontrar la máquinas")

        request = self.factory.get('/maquina?que=auto', follow = True)
        request.user = self.cientifico
        response = listarMaquinas(request)
        self.assertEqual("MAQ002" in response.content, True, "Debe encontrar la máquinas")


class LoginTest(TestCase):
    """Prueba el servicio de autenticación 
        Se encarga de:
            * Probar que el servicio REST de autenicación funcione
            * Autenticar varios usarios
    """

    def setUp(self):
        """"Registra un usuario en la aplicación
        """
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.cientifico = User.objects.create_user(username = 'john',
                                                   email = 'jlennon@beatles.com',
                                                   password = CONTRASENA)
        # c.login(username=self.cientifico.username, password=CONTRASENA)

        ver = Permission.objects.get(name = 'usuario||agregar')
        self.cientifico.user_permissions.add(ver)

    def testLogin(self):
        """ Prueba que el usario registrado en la base de datos pueda inciar sesión"""
        postData = {"username": "john", "password": CONTRASENA}
        response = c.post('/accounts/login/', postData, follow = True)
        self.assertEqual(response.content, 200, "Debe poder inciar sesion")

        self.assertEqual(not "correct username" in response.content, True, "Debe poder inciar sesion")

    def testLogin(self):
        """ Prueba que no se pueda inicar sesión con un contraseña incorrecta"""
        postData = {"username": "john", "password": "estamal"}
        response = c.post('/accounts/login/', postData, follow = True)
        self.assertEqual("correct username" in response.content, True, "No debe poder inciar sesións")

    def testLogin(self):
        """ Prueba que no se pueda inicar sesión con un usario incorrecto"""
        postData = {"username": "incorrecto", "password": "estamal"}
        response = c.post('/accounts/login/', postData, follow = True)
        self.assertEqual("correct username" in response.content, True, "No debe poder inciar sesións")
