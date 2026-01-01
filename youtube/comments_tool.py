import os
import requests
from typing import List, Type, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configuração da API do YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "SUA_CHAVE_AQUI")

class CommentsInput(BaseModel):
    """ Esquema de entrada para a ferramenta de extração de comentários do YouTube """
    video_ids: List[str] = Field(..., description="Lista de IDs de vídeos do YouTube para análise")

class CommentsTool(BaseTool):
    name: str = "YouTube Comments Extractor"
    description: str = "Extrai e filtra comentários relevantes de vídeos do YouTube."
    args_schema: Type[BaseModel] = CommentsInput

    def _fetch_comments(self, video_id: str) -> List[str]:
        """
        Obtém os comentários de um vídeo e remove mensagens genéricas de felicitação.
        """
        def is_relevant_comment(comment: str) -> bool:
            """ Filtra mensagens genéricas de elogios. """
            irrelevant_phrases = ["parabéns", "ótimo vídeo", "gostei muito", "excelente trabalho", "top demais"]
            return not any(phrase in comment.lower() for phrase in irrelevant_phrases)

        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "key": YOUTUBE_API_KEY,
            "maxResults": 100
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            comments = [
                item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                for item in response.json().get("items", [])
            ]
            return [c for c in comments if is_relevant_comment(c)]
        else:
            print(f"❌ Erro ao buscar comentários do vídeo {video_id}: {response.status_code}")
            return []

    def _run(self, video_ids: List[str]) -> Dict[str, List[str]]:
        """
        Obtém e filtra comentários para uma lista de vídeos.
        """
        comments_by_video = {}

        for video_id in video_ids:
            filtered_comments = self._fetch_comments(video_id)
            if filtered_comments:
                comments_by_video[video_id] = filtered_comments

        return comments_by_video
