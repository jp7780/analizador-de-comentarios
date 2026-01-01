import os
import requests
from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from video_youtube import YouTubeVideo  # Importando a classe estruturada

# Carregar variáveis do .env
load_dotenv()

# Configuração da API do YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# 🔹 Classe de entrada para a ferramenta
class TrendInput(BaseModel):
    """Esquema de entrada para a ferramenta de busca de tendências no YouTube."""
    category: str = Field(..., description="ID da categoria do YouTube")
    region: str = Field(..., description="Código da região (ex: BR, US)")
    max_results: int = Field(5, description="Número máximo de vídeos a buscar")
    num_comments: int = Field(10, description="Número máximo de comentários a buscar por vídeo")


# 🔹 Classe da ferramenta TrendTool
class TrendTool(BaseTool):
    name: str = "YouTube Trends Finder"
    description: str = "Busca vídeos populares no YouTube com base em categoria e região e coleta informações relevantes."
    args_schema: Type[BaseModel] = TrendInput
    last_results: List[YouTubeVideo] = []  # Armazena os últimos resultados

    def _fetch_comments(self, video_id: str, num_comments: int) -> List[str]:
        """Busca os primeiros comentários de um vídeo, ajustando a quantidade conforme solicitado."""
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": num_comments,
            "textFormat": "plainText",
            "key": YOUTUBE_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            comments = response.json().get("items", [])
            return [comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for comment in comments]
        return ["Nenhum comentário disponível."]

    def _run(
        self,
        category: str = "28",  # Ciência e Tecnologia
        region: str = "BR", #brasil
        max_results: int = 5, #top 5
        num_comments: int = 10 #comentários 10
        ) -> str:
        """Executa a busca por vídeos populares no YouTube e retorna um relatório textual."""
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "chart": "mostPopular",
            "regionCode": region,
            "videoCategoryId": category,
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            videos = response.json().get("items", [])
            self.last_results = YouTubeVideo.from_api_response(videos)  # Converte os dados para objetos estruturados
            
            # Buscando os comentários com a quantidade ajustável
            for video in self.last_results:
                video.top_comments = self._fetch_comments(video_id=video.videoId, num_comments=num_comments)

            return self._generate_report()  # 🔥 Usamos um método separado para gerar o relatório
        else:
            raise ValueError(f"Erro na requisição: {response.status_code} - {response.text}")

    def _generate_report(self) -> str:
        """Gera um relatório de tendências baseado nos vídeos coletados."""
        if not self.last_results:
            return "Nenhuma tendência encontrada no YouTube."

        return "\n\n".join(str(video) for video in self.last_results)  # 🔥 Agora usa `__str__()` de YouTubeVideo


#trend = TrendTool()
#resultado = trend._run()  # Vai buscar tendências de Tecnologia no Brasil com 10 comentários
#print(resultado)  # Exibe o relatório gerado
