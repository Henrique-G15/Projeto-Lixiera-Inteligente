from .iot.atuador import Atuador
from .iot.sensor import Sensor
from .history.sensor_historico import SensorHistorico
from .history.atuador_historico import AtuadorHistorico
from .history.registro_historico import RegistroHistorico
from .user.user import Usuario
from .admin import Admin
from .iot.lixeira import Lixeira

__all__ = ["Atuador", "Sensor", "SensorHistorico", "AtuadorHistorico", "RegistroHistorico", "Lixeira"]