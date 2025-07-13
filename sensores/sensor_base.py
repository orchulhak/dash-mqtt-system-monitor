class SensorBase:
    """
    Define o atributo 'nome' e o método 'ler' para ser sobrescrito pelas subclasses.
    Esta classe funciona como um "contrato", garantindo que todos os sensores
    tenham uma estrutura mínima consistente.
    """

    def __init__(self, nome: str = "Sensor Genérico"):
        """
        Inicializa o objeto do sensor, definindo seu nome.

        Args:
            nome (str): O nome específico para o sensor (ex: "Sensor CPU").
                        Se nenhum nome for passado, utiliza "Sensor Genérico".
        """
        self.nome = nome

    def ler(self) -> float | None:
        """
        Método placeholder para a leitura de dados do sensor.

        Este método deve ser obrigatoriamente sobrescrito nas subclasses
        com a lógica específica para ler o valor daquele sensor.
        Se chamado a partir da classe base, apenas emite um aviso.

        Returns:
            None: Retorna None pois a implementação real pertence à subclasse.
        """

        print(f"método 'ler' do sensor '{self.nome}' não implementado")
        return None

    def __str__(self):
        """
        Define a representação em string do objeto.

        Este método é chamado quando usamos a função print() em uma instância
        desta classe.

        Returns:
            str: Uma string formatada contendo o nome do sensor.
        """

        return f"Sensor: {self.nome}"
