import psutil
from .sensor_base import SensorBase


class SensorDisco(SensorBase):
    """
    Sensor especializado para monitorar o uso do disco rígido.

    Esta classe herda de SensorBase e implementa o método 'ler'
    para obter a porcentagem de uso do disco principal (root).
    """
    def __init__(self):
        """
        Inicializa o sensor de Disco.

        Chama o construtor da classe pai (SensorBase) para definir
        o nome deste sensor especificamente como "Sensor Disco".
        """
        super().__init__("Sensor Disco")

    def ler(self):
        """
        Lê e retorna a porcentagem de uso atual do disco.

        Este método sobrescreve o método 'ler' da classe base.
        Ele verifica o uso do disco no diretório raiz ('/').

        Returns:
            float: A porcentagem de uso do disco (um valor de 0.0 a 100.0).
        """
        disco = psutil.disk_usage('/')
        return disco.percent
