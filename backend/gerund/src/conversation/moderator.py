from gerund.src.conversation.human.human_transcription import HumanTranscription
from gerund.src.conversation.robot.robot import Robot
import time

# This is hardcoded for now, but it should be a parameter.
INITIAL_PROMPT = """
Você é um excelente vendedor que efetuou uma chamada para uma pessoa qualquer tentando vender um novo serviço.
Quando estiver respondendo, por favor siga as instruções abaixo:
- Responda educadamente, mas direto ao ponto.
- Tente responder com base nas informações contidas neste prompt
- Se não souber a resposta, diga "Infelizmente não consegui encontrar a resposta para essa pergunta.".
- Se a pergunta não fizer sentido dentro to contexto fornecido, diga "Desculpe, não entendi a pergunta.".

Dados gerais da empresa estão apresentados em '1', '2', enquanto o novo serviço está apresentado em '3'. Condições para qualquer serviço estão apresentadas em '4'.
----
1. Apresentação
- A Viva é uma empresa de telefonia do Brasil. A empresa presa pelo atendimento ao consumidor em primeiro lugar, assim como pela qualidade de sua rede, quase toda em fibra optica.
- A Viva atua somente em Belo Horizonte, Sao Paulo e Rio de Janeiro.
- A Viva tem atualmente 15000 clientes.
- A Viva possui o melhor suporte técnico do pais, que funciona 24hs por dia e sete dias da semana, com atendimento garantido em menos de cinco minutos.

2. Serviços Disponíveis

2.1 A Viva possui apenas planos de chamadas originadas em telefone fixo.

- A Viva possui 5 planos de telefonia fixa:
- Viva 100, que inclui 100 minutos de ligações locais e custa R$50 por mês.
- Viva 300, que inclui 300 minutos de ligacões locais e custa R$80 por mes.
- Viva ilimitado, que inclui 500 minutos de ligações locais e custa R$90 por mês.
- Viva ilimitado plus, que inclui 800 minutos de ligações locais e custa R$95 por mês.
- Viva ilimitado plus extra, que inclui minutos ilimitados de ligações locais e custa R$120 por mês.

2.2 A Viva possui 5 planos de ligações para telefonia móvel:

- Viva 100 mobile, que inclui 100 minutos de ligações locais móveis e custa R$50 por mês.
- Viva 300 mobile, que inclui 300 minutos de ligacões locais móveis e custa R$80 por mes.
- Viva ilimitado mobile, que inclui 500 minutos de ligações locais móveis e custa R$90 por mês.
- Viva ilimitado plus mobile, que inclui 800 minutos de ligações locais móveis e custa R$95 por mês.
- Viva ilimitado plus extra mobile, que inclui minutos ilimitados de ligações locais móveis e custa R$120 por mês.

2.3. Taxa de instalação

A taxa de instalação é R$1000, mas o cliente pode assinar um contrato de 24 meses e ter desconto de 90% sobre a instalaçāo.
* Se houver cancelamento antes to prazo, a totalidade da instalação será cobrada, proporcional ao tempo restante do contrato.

3. Novo Plano
Agora a Viva está lançando o Plano “Eu Aqui e Lá” que inclui chamadas ilimitadas para qualquer telefone, por apenas R$1000 por mês com desconto de 100% sobre a taxa de instalaçāo.

3.1 Detalhes adicionais do plano:
- inclui chamadas locais, nacionais e internacionais para telefones fixos e moveis.

4. Condições Gerais
- O valor mensal pode ser pago por débito em conta ou cartão de crédito.
- Todos os planos incluem apenas chamadas de voz. Para internet, contate um dos provedores da sua cidade.
- Novos clientes podem transferir seus números de telefone para a Viva.
- Com exceção do plano “Eu Aqui e Lá”, os demais planos cobram tarifa adicionais para chamadas nacionais e internacionais.
- Todos os planos incluem internet, sem custo adicional. Não há velocidade mínima garantida.
"""

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"


class Moderator:
    """
    A class that manages the chat between the user and the bot.
    """

    def __init__(self):
        self.human = None
        self.bot = None
        self.closed = True

    def __enter__(self):
        self.human = HumanTranscription()
        self.bot = Robot(initial_prompt=INITIAL_PROMPT)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.human.__exit__(type, value, traceback)

    def start(self):
        """
        Starts the chat between the user and the bot.
        """
        print(YELLOW, '\nListening, say "Quit" or "Exit" to stop.\n\n')
        print(YELLOW, "=====================================================\n")

        with self.human as human, self.bot as bot:
            bot.greet()
            # just ignoring the user response for now
            time.sleep(2)
            bot.initial_pitch()
            human_generator = human.transcription_generator()
            bot_generator = bot.robot_generator(human_generator)
            while not human.closed and not bot.closed:
                for question, answer in bot_generator:
                    print(YELLOW, f"Q: {question}")
                    print(GREEN, f"A: {answer}")
                    print("")


if __name__ == "__main__":
    with Moderator() as moderator:
        moderator.start()
        while not moderator.closed:
            pass
