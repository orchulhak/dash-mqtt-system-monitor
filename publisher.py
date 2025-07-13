import time
import json
from mqtt_manager.mqtt_client import MQTTClient
from sensores.sensor_cpu import SensorCPU
from sensores.sensor_disco import SensorDisco
from sensores.sensor_temperatura import SensorTemperatura
from sensores.sensor_tempo import SensorTempo

# --- Constantes de Configuração ---
BROKER = "test.mosquitto.org"
TOPICO = "UFSC/DAS/sensores"

def main():
    """
    Função principal que inicializa os sensores, conecta ao broker MQTT
    e entra em um loop para publicar os dados continuamente.
    """
    sensores = [
        SensorCPU(),
        SensorDisco(),
        SensorTemperatura(),
        SensorTempo()
    ]

    # Cria uma instância do nosso cliente MQTT com as configurações de broker e tópico
    mqtt_client = MQTTClient(BROKER, TOPICO)
    # Estabelece a conexão com o broker MQTT
    mqtt_client.conectar()

    # Loop infinito para manter o publisher em execução
    while True:
        # Itera sobre cada sensor na lista de sensores
        for sensor in sensores:
            # Chama o método 'ler()' de cada sensor para obter o valor atual
            valor = sensor.ler()
            # Cria um dicionário (payload) com o nome do sensor e o valor lido
            payload = {
                "sensor": sensor.nome,
                "valor": valor
            }
            # Converte o dicionário para uma string no formato JSON e publica no tópico
            mqtt_client.publicar(json.dumps(payload))
            # Imprime no console o dado que foi publicado para fins de depuração
            print(f"Publicado: {payload}")

        # Pausa a execução por 5 segundos antes de iniciar um novo ciclo de leituras
        time.sleep(5)


if __name__ == "__main__":
    main()
