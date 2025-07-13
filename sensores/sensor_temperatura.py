import psutil
import random
from .sensor_base import SensorBase


class SensorTemperatura(SensorBase):
    """
    Sensor para monitorar a temperatura do hardware.

    Herda de SensorBase e implementa um método 'ler' que:
    1. Verifica se a função de leitura de temperatura é suportada pelo sistema.
    2. Usa um bloco try-except para capturar erros durante a leitura.
    3. Retorna um valor aleatório caso a leitura falhe ou não seja possível.
    """
    def __init__(self):
        """
        Inicializa o sensor de Temperatura.
        Define o nome do sensor.
        """
        super().__init__("Sensor Temperatura")

    def ler(self):
        """
        Lê a temperatura do hardware.

        Tenta obter a primeira leitura de temperatura disponível no sistema.
        Se ocorrer qualquer erro ou se a função não for suportada, um aviso
        é impresso e um valor de fallback aleatório é retornado.

        Returns:
            float: A temperatura lida ou um valor simulado.
        """
        if hasattr(psutil, "sensors_temperatures"):
            try:
                temperaturas = psutil.sensors_temperatures()
                if temperaturas:
                    for nome_sensor in temperaturas:
                        if temperaturas[nome_sensor]:
                            return temperaturas[nome_sensor][0].current
            except Exception as e:
                print(f"AVISO: Ocorreu um erro ao ler a temperatura do hardware: {e}")

        return round(random.uniform(40.0, 65.0), 2)
