import os
import requests
from typing import List, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from video_youtube import YouTubeVideo  # Classe que estrutura os dados do vídeo

# Carregar variáveis do .env
load_dotenv()

# Configuração da API do YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "SUA_CHAVE_AQUI")


# 🔹 Classe de entrada da ferramenta
class VideoDetailsInput(BaseModel):
    r"""
    Esquema de entrada para a ferramenta de extração de dados de vídeos do YouTube.
    """
    video_ids: List[str] = Field(..., description="Lista de IDs de vídeos do YouTube para análise")


# 🔹 Classe da ferramenta para buscar detalhes dos vídeos
class YouTubeVideoTool(BaseTool):
    name: str = "YouTube Video Details Extractor"
    description: str = "Busca informações detalhadas de uma lista de vídeos do YouTube."
    args_schema: Type[BaseModel] = VideoDetailsInput

    def _fetch_video_details(self, video_id: str) -> YouTubeVideo:
        r"""
        Busca as informações detalhadas de um único vídeo do YouTube pelo seu ID.
        """

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": YOUTUBE_API_KEY,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            video_data = response.json().get("items", [])
            if video_data:
                return YouTubeVideo.from_api_response(video_data)[0]  # Retorna o primeiro vídeo encontrado
            else:
                print(f"⚠️ Nenhum dado encontrado para o vídeo ID: {video_id}")
        else:
            print(f"❌ Erro na requisição do vídeo {video_id}: {response.status_code} - {response.text}")

        return None  # Retorna None se o vídeo não foi encontrado ou houve erro

    def _run(self, video_ids: List[str]) -> List[YouTubeVideo]:
        r"""
        Obtém detalhes de uma lista de vídeos do YouTube processando um por um.
        """
        videos = []

        for video_id in video_ids:
            video_info = self._fetch_video_details(video_id)
            if video_info:
                videos.append(video_info)

        return videos  # Retorna a lista de vídeos analisados
