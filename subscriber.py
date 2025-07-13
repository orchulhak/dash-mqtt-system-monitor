import threading
import time
import json
from mqtt_manager.mqtt_client import MQTTClient
from dashboard.dashboard import Dashboard

# --- Constantes de Configuração ---
BROKER = "test.mosquitto.org"
TOPICO = "UFSC/DAS/sensores"

# Cria uma instância global do Dashboard para que possa ser acessada pela função de callback
dashboard = Dashboard()


def callback(client, userdata, mensagem):
    """
    Função que é executada automaticamente toda vez que uma mensagem é recebida no tópico assinado.

    Args:
        client: A instância do cliente que recebeu a mensagem.
        userdata: Dados de usuário privados (não utilizados).
        mensagem: O objeto da mensagem, contendo o tópico e o payload.
    """
    # Decodifica o payload da mensagem de bytes para uma string UTF-8
    payload = mensagem.payload.decode()
    # Imprime a mensagem recebida no console
    print(f"Recebido: {payload}")

    try:
        # Converte a string JSON em um dicionário Python
        dados = json.loads(payload)
        # Extrai o nome do sensor e o valor do dicionário
        nome_sensor = dados["sensor"]
        valor = dados["valor"]
        # Adiciona os dados extraídos ao dashboard para visualização
        dashboard.adicionar_dado(nome_sensor, valor)
    except Exception as e:
        # Em caso de erro na decodificação ou extração, imprime um aviso
        print("Erro ao processar mensagem:", e)


def main():
    """
    Função principal que configura o cliente MQTT, inicia o dashboard
    e mantém o script em execução.
    """
    # Cria uma instância do nosso cliente MQTT
    mqtt_client = MQTTClient(BROKER, TOPICO)
    # Inscreve-se no tópico e define a função 'callback' para ser chamada ao receber mensagens
    mqtt_client.assinar(callback)

    # Cria uma nova thread para executar o servidor do dashboard.
    thread_dashboard = threading.Thread(target=dashboard.rodar)
    # Inicia a execução da thread do dashboard
    thread_dashboard.start()

    # Loop infinito para manter o script rodando.
    while True:
        time.sleep(5)


# Bloco padrão que executa a função main() quando o script é chamado
if __name__ == "__main__":
    main()
