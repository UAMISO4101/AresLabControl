from .Almacenamiento import Almacenamiento
from .Bandeja import Bandeja
from .Experimento import Experimento
from .Laboratorio import Laboratorio
from .Maquina import Maquina
from .Mueble import Mueble
from .MuebleEnLab import MuebleEnLab
from .Muestra import Muestra
from .Paso import Paso
from .Protocolo import Protocolo
from .Proyecto import Proyecto
from .Solicitud import Solicitud
from .SolicitudMaquina import SolicitudMaquina
from .SolicitudMuestra import SolicitudMuestra
from .TipoDocumento import TipoDocumento
from .Usuario import Usuario

permissions_storage = (
    ('can_addStorage', 'almacenamiento||agregar'),
    ('can_editStorage', 'almacenamiento||editar'),
    ('can_listStorage', 'almacenamiento||listar'),
    ('can_viewStorage', 'almacenamiento||ver'),
    ('can_requestStorage', 'almacenamiento||solicitar'),
)

permissions_tray = (
    ('can_addTray', 'bandeja||agregar'),
    ('can_editTray', 'bandeja||editar'),
    ('can_listTray', 'bandeja||listar'),
    ('can_viewTray', 'bandeja||ver'),
)

permissions_experiment = (
    ('can_addExperiment', 'experimento||agregar'),
    ('can_editExperiment', 'experimento||editar'),
    ('can_listExperiment', 'experimento||listar'),
    ('can_viewExperiment', 'experimento||ver'),
)

permissions_lab = (
    ('can_addLab', 'laboratorio||agregar'),
    ('can_editLab', 'laboratorio||editar'),
    ('can_listLab', 'laboratorio||listar'),
    ('can_viewLab', 'laboratorio||ver'),
)

permissions_machine = (
    ('can_addMachine', 'maquina||agregar'),
    ('can_editMachine', 'maquina||editar'),
    ('can_listMachine', 'maquina||listar'),
    ('can_viewMachine', 'maquina||ver'),
    ('can_requestMachine', 'maquina||solicitar'),
)

permissions_sample = (
    ('can_addSample', 'muestra||agregar'),
    ('can_editSample', 'muestra||editar'),
    ('can_listSample', 'muestra||listar'),
    ('can_viewSample', 'muestra||ver'),
    ('can_requestSample', 'muestra||solicitar'),
)

permissions_step = (
    ('can_addStep', 'paso||agregar'),
    ('can_editStep', 'paso||editar'),
    ('can_listStep', 'paso||listar'),
    ('can_viewStep', 'paso||ver'),
)

permissions_protocol = (
    ('can_addProtocol', 'protocolo||agregar'),
    ('can_editProtocol', 'protocolo||editar'),
    ('can_listProtocol', 'protocolo||listar'),
    ('can_viewProtocol', 'protocolo||ver'),
)

permissions_project = (
    ('can_addProject', 'proyecto||agregar'),
    ('can_editProject', 'proyecto||editar'),
    ('can_listProject', 'proyecto||listar'),
    ('can_viewProject', 'proyecto||ver'),
)

permissions_request = (
    ('can_listRequest', 'solicitud||listar'),
    ('can_viewRequest', 'solicitud||ver'),
    ('can_manageRequest', 'solicitud||admin'),
)

permissions_user = (
    ('can_addUser', 'usuario||agregar'),
    ('can_editUser', 'usuario||editar'),
    ('can_listUser', 'usuario||listar'),
    ('can_viewUser', 'usuario||ver'),
)
