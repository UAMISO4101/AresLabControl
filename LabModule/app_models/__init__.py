from . import Almacenamiento
from . import AlmacenamientoEnLab
from . import Bandeja
from . import Experimento
from . import Laboratorio
from . import Maquina
from . import MaquinaEnLab
from . import Muestra
from . import Paso
from . import Protocolo
from . import Proyecto
from . import Solicitud
from . import SolicitudMaquina
from . import SolicitudMuestra
from . import TipoDocumento
from . import Usuario

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
    ('can_addMachine', 'Maquina||agregar'),
    ('can_editMachine', 'Maquina||editar'),
    ('can_listMachine', 'Maquina||listar'),
    ('can_viewMachine', 'Maquina||ver'),
    ('can_requestMachine', 'Maquina||solicitar'),
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
