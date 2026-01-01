from crewai import Agent, Task, Crew, Process
from trends_tool import TrendTool  # Importando a ferramenta de busca de tendências

class YouTubeTrendAnalyzer:
    r"""
    Classe para configurar e executar a análise de tendências do YouTube usando CrewAI.
    """

    def __init__(self):
        self.llm = "gpt-4o-mini"
        self.crew = self._setup_crew()

    def _setup_crew(self):
        r"""
        Configura os agentes e as tarefas para uma análise avançada de tendências.
        """

        # 🔹 Agente 1: Analista de Tendências
        analista_tendencias = Agent(
            role=r"""Analista de Tendências do YouTube""",
            goal=r"""Analisar os vídeos mais populares do YouTube e gerar insights sobre as tendências.""",
            backstory=r"""
                Você é um especialista em análise de dados e tendências digitais. Seu foco é ajudar criadores de conteúdo a 
                entenderem o que está viralizando no YouTube e como podem aproveitar essas tendências.
            """,
            tools=[TrendTool()],  # Usando a ferramenta personalizada
            verbose=True
        )

        # 🔹 Agente 2: Especialista em Engajamento
        especialista_engajamento = Agent(
            role=r"""Especialista em Engajamento Digital""",
            goal=r"""Interpretar os padrões de engajamento e prever futuras tendências do YouTube.""",
            backstory=r"""
                Você é um analista de redes sociais que entende profundamente o comportamento dos usuários no YouTube.
                Seu objetivo é interpretar métricas como curtidas, comentários e crescimento de visualizações para prever 
                quais tipos de vídeos e conteúdos continuarão em alta.
            """,
            tools=[],  # Esse agente não usa ferramentas, só interpreta os dados coletados
            verbose=True
        )

        # 🔹 Task 1: Buscar vídeos populares
        analise_tendencias_task = Task(
            description=r"""
                Pesquise os {max_results} vídeos mais populares 
                no YouTube na categoria {category}, 
                dentro da região {region}.
                
                Analise os {num_comments} primeiros comentários 
                de cada vídeo para entender o engajamento do público. 
                Identifique os temas mais recorrentes, 
                os padrões de engajamento e os canais influentes.
                
                Destaque vídeos com alta taxa de crescimento e 
                faça previsões sobre o que pode continuar em alta.
            """,
            expected_output=r"""
                Um relatório textual sobre as tendências 
                atuais do YouTube na categoria {category}, 
                na região {region}. O relatório deve 
                destacar os principais vídeos virais, 
                análises de engajamento e previsões sobre 
                futuras tendências.
            """,
            agent=analista_tendencias,
            verbose=True
        )

        # 🔹 Task 2: Analisar padrões de engajamento
        analise_engajamento_task = Task(
            description=r"""
                Com base nos dados coletados sobre tendências do YouTube, analise os padrões de engajamento. 
                Considere a quantidade de curtidas, comentários e a velocidade de crescimento dos vídeos.
                
                Identifique quais formatos de vídeos estão gerando mais interação e destaque quais criadores estão crescendo 
                rapidamente na plataforma.
                
                No final, forneça uma previsão sobre quais tipos de vídeos provavelmente continuarão em alta.
            """,
            expected_output=r"""
                Um relatório detalhado sobre o engajamento dos vídeos, incluindo previsões sobre tendências futuras e quais 
                formatos de vídeos estão em ascensão.
            """,
            agent=especialista_engajamento
        )

        # 🔹 Criando a Crew que executará a análise
        return Crew(
            agents=[analista_tendencias, especialista_engajamento],
            tasks=[analise_tendencias_task, analise_engajamento_task],
            process=Process.sequential  # O agente executa a tarefa de forma sequencial
        )

    def kickoff(self, inputs):
        r"""
        Executa a Crew para analisar as tendências do YouTube.

        :param inputs: Dicionário com valores opcionais para sobrescrever os padrões.
        :return: Relatório textual da análise.
        """

        ret = self.crew.kickoff(inputs=inputs)
        return ret.raw


# 🔹 Criando e executando a Crew
crew = YouTubeTrendAnalyzer()
inputs = {
    "category": "28",  # Ciência e Tecnologia
    "region": "US",  # Estados Unidos
    "max_results": 10,  # Buscar 10 vídeos
    "num_comments": 5  # Analisar 5 comentários por vídeo
}

retorno = crew.kickoff(inputs=inputs)
print(retorno)
