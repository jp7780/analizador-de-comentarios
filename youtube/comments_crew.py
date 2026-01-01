from crewai import Agent, Task, Crew, Process
from comments_tool import CommentsTool  # Importando a ferramenta

class YouTubeCommentsAnalyzer:
    """
    Classe para configurar e executar a análise de comentários do YouTube usando CrewAI.
    """

    def __init__(self):
        self.crew = self._setup_crew()

    def _setup_crew(self):
        """
        Configura os agentes que realizarão a extração e análise dos comentários.
        """

        # 🔹 Agente Extrator de Comentários
        extrator_comentarios = Agent(
            role="Especialista em Extração de Comentários",
            goal="Coletar e filtrar comentários relevantes de vídeos do YouTube.",
            backstory="Você é um expert em análise de feedback de usuários e sabe identificar comentários relevantes.",
            tools=[CommentsTool()],  # Usando a ferramenta CommentsTool
            verbose=True
        )

        # 🔹 Agente Analista de Necessidades
        analista_necessidades = Agent(
            role="Analista de Necessidades do Usuário",
            goal="Identificar padrões e necessidades dos usuários a partir dos comentários dos vídeos.",
            backstory="Você é um especialista em entender os desejos e dificuldades dos usuários, transformando feedback em insights valiosos.",
            verbose=True
        )

        # 🔹 Tarefa: Extrair Comentários
        extracao_task = Task(
            description="""
                Extraia todos os comentários dos seguintes vídeos do YouTube:
                
                {video_links}
                
                Filtre os comentários removendo mensagens genéricas de parabéns e elogios.
                Retorne uma lista de comentários relevantes para análise.
            """,
            expected_output="Uma lista de comentários úteis e relevantes para análise.",
            agent=extrator_comentarios
        )

        # 🔹 Tarefa: Analisar Necessidades
        analise_task = Task(
            description="""
                Analise os comentários extraídos dos vídeos abaixo:
                
                {video_links}
                
                Identifique padrões e principais necessidades dos usuários.
                Classifique as necessidades em categorias como: sugestões de melhoria, dúvidas frequentes, problemas relatados.
            """,
            expected_output="Um relatório com insights sobre as principais necessidades dos usuários.",
            agent=analista_necessidades
        )

        # 🔹 Criando a Crew
        return Crew(
            agents=[extrator_comentarios, analista_necessidades],
            tasks=[extracao_task, analise_task],
            process=Process.sequential  # O primeiro agente extrai, o segundo analisa
        )

    def kickoff(self, video_links):
        """
        Executa a Crew para analisar comentários dos vídeos do YouTube.

        :param video_links: Lista de URLs dos vídeos do YouTube.
        :return: Relatório textual da análise.
        """

        video_ids = [link.split("v=")[-1] for link in video_links]

        inputs = {"video_links": "\n".join(video_links)}

        resultado = self.crew.kickoff(inputs=inputs)
        return resultado.raw


"""
# 🔹 Criando e executando a análise
video_analyzer = YouTubeCommentsAnalyzer()
videos = [
    "https://www.youtube.com/watch?v=-fPZsngNMFs",
    "https://www.youtube.com/watch?v=m2rG6zHoxBo",
    "https://www.youtube.com/watch?v=m46tZX6vceI"
]

resultado = video_analyzer.kickoff(video_links=videos)

# 🔹 Exibir o relatório
print("📊 Análise dos Comentários:\n", resultado)
"""