import paho.mqtt.client as mqtt


class MQTTClient:
    """
    Uma classe de wrapper para simplificar a interação com um broker MQTT.

    Esta classe gerencia a conexão, publicação e assinatura de tópicos,
    """

    def __init__(self, broker, topic):
        """
        Inicializa o cliente MQTT.

        Args:
            broker (str): O endereço do broker MQTT (ex: "test.mosquitto.org").
            topic (str): O tópico MQTT no qual o cliente irá publicar ou assinar.
        """
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client()

    def conectar(self):
        """
        Conecta o cliente ao broker MQTT.

        Este método é usado principalmente para clientes que apenas publicam mensagens.
        """
        self.client.connect(self.broker)

    def publicar(self, mensagem):
        """
        Publica uma mensagem no tópico MQTT configurado.

        Args:
            mensagem (str): A mensagem a ser enviada. Geralmente uma string JSON.
        """
        self.client.publish(self.topic, mensagem)

    def assinar(self, callback):
        """
        Inscreve o cliente em um tópico para receber mensagens e inicia o loop de escuta.

        Args:
            callback (function): A função que será chamada quando uma nova mensagem for recebida.
            A função de callback deve ter a assinatura: callback(client, userdata, message).
        """
        # Define qual função será executada quando uma mensagem chegar
        self.client.on_message = callback

        # Conecta-se ao broker
        self.client.connect(self.broker)

        # Inscreve-se no tópico para começar a receber mensagens
        self.client.subscribe(self.topic)

        # Inicia um loop em uma thread separada para escutar por mensagens.
        # Isso não bloqueia o fluxo principal do programa.
        self.client.loop_start()
