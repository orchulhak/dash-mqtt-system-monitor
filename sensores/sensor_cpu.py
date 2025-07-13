import psutil
from .sensor_base import SensorBase


class SensorCPU(SensorBase):
    """
    Sensor especializado para monitorar o uso da CPU.

    Esta classe herda de SensorBase e fornece uma implementação concreta
    do método 'ler' para obter a porcentagem de uso da CPU.
    """
    def __init__(self):
        """
        Inicializa o sensor de CPU.

        Chama o construtor da classe pai (SensorBase) para definir
        o nome deste sensor especificamente como "Sensor CPU".
        """
        super().__init__("Sensor CPU")

    def ler(self):
        """
        Lê e retorna a porcentagem de uso atual da CPU.

        Este método sobrescreve o método 'ler' da classe base.
        A medição é feita durante um intervalo de 1 segundo para
        garantir uma leitura mais precisa.

        Returns:
            float: A porcentagem de uso da CPU (um valor de 0.0 a 100.0).
        """
        return psutil.cpu_percent(interval=1)
