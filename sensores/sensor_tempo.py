import psutil
import time
from .sensor_base import SensorBase


class SensorTempo(SensorBase):
    """
    Sensor especializado para monitorar o tempo de atividade (uptime) do sistema.

    Esta classe herda de SensorBase e implementa o método 'ler' para calcular
    há quantos segundos o sistema está ligado.
    """
    def __init__(self):
        """
        Inicializa o sensor de Tempo de Atividade.

        Chama o construtor da classe pai (SensorBase) para definir
        o nome deste sensor como "Sensor Uptime (segundos)".
        """
        super().__init__("Sensor Uptime (segundos)")

    def ler(self):
        """
        Calcula e retorna o tempo de atividade total do sistema em segundos.

        O cálculo é feito subtraindo o momento em que o sistema foi iniciado
        (boot time) do momento atual.

        Returns:
            float: O tempo total de atividade do sistema em segundos.
        """
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        return uptime
