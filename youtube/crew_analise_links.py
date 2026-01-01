from crewai import Agent, Task, Crew, Process
from videos_tool_youtube import YouTubeVideoTool  # Importando a nova ferramenta

class YouTubeVideoAnalyzer:
    r"""
    Classe para configurar e executar uma análise de uma lista de vídeos do YouTube usando CrewAI.
    """

    def __init__(self):
        self.llm = "gpt-4o-mini"
        self.crew = self._setup_crew()

    def _setup_crew(self):
        r"""
        Configura o agente que analisará uma lista específica de vídeos do YouTube.
        """

        # 🔹 Agente: Analista de Vídeos do YouTube
        analista_videos = Agent(
            role=r"""Analista de Vídeos do YouTube""",
            goal=r"""Analisar uma lista de vídeos do YouTube e gerar insights detalhados sobre engajamento e tendências.""",
            backstory=r"""
                Você é um especialista em análise de vídeos do YouTube. Seu objetivo é revisar métricas como 
                visualizações, curtidas e comentários para entender padrões de engajamento e prever tendências futuras.
            """,
            tools=[YouTubeVideoTool()],  # Agora usamos a nova ferramenta
            verbose=True
        )

        # 🔹 Task: Analisar os vídeos da lista
        analise_videos_task = Task(
            description=r"""
                Analise a seguinte lista de vídeos do YouTube:
                
                {video_links}
                
                Para cada vídeo, colete as seguintes informações:
                - Título do vídeo
                - Canal
                - Número de visualizações
                - Curtidas
                - Comentários
                - Duração do vídeo
                - Se tem legendas disponíveis
                
                A partir desses dados, gere um relatório sobre padrões de engajamento e possíveis tendências emergentes.
            """,
            expected_output=r"""
                Um relatório detalhado analisando os vídeos fornecidos, destacando padrões de engajamento, 
                crescimento e previsões sobre tendências futuras.
            """,
            agent=analista_videos
        )

        # 🔹 Criando a Crew que executará a análise
        return Crew(
            agents=[analista_videos],
            tasks=[analise_videos_task],
            process=Process.sequential  # O agente executa a tarefa de forma sequencial
        )

    def kickoff(self, video_links):
        r"""
        Executa a Crew para analisar uma lista de vídeos do YouTube.

        :param video_links: Lista de URLs dos vídeos do YouTube.
        :return: Relatório textual da análise dos vídeos.
        """

        # 🔹 Extrai os IDs dos vídeos a partir dos links
        video_ids = [link.split("v=")[-1] for link in video_links]

        inputs = {"video_links": "\n".join(video_links)}

        ret = self.crew.kickoff(inputs=inputs)
        return ret.raw



# 🔹 Criando e executando a análise para uma lista de vídeos
video_analyzer = YouTubeVideoAnalyzer()
videos = [
    "https://www.youtube.com/watch?v=-fPZsngNMFs",
    "https://www.youtube.com/watch?v=m2rG6zHoxBo",
    "https://www.youtube.com/watch?v=m46tZX6vceI"
]

resultado = video_analyzer.kickoff(video_links=videos)

# 🔹 Exibir o relatório
print("📊 Análise dos vídeos fornecidos:\n", resultado)
