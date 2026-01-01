import yaml
from pydantic import BaseModel, Field
from typing import List, Optional


class YouTubeVideo(BaseModel):
    """Estrutura de retorno para vídeos populares do YouTube."""

    videoId: str = Field(..., description="ID único do vídeo no YouTube")
    title: str = Field(..., description="Título do vídeo")
    description: str = Field(..., description="Descrição do vídeo")
    channelTitle: str = Field(..., description="Nome do canal")
    channelId: str = Field(..., description="ID único do canal")
    publishedAt: str = Field(..., description="Data e hora da publicação")
    thumbnails: str = Field(..., description="URL da miniatura padrão do vídeo")
    tags: Optional[List[str]] = Field(None, description="Palavras-chave associadas ao vídeo")
    categoryId: str = Field(..., description="ID da categoria do vídeo")
    viewCount: int = Field(..., description="Número de visualizações")
    likeCount: Optional[int] = Field(None, description="Número de curtidas")
    commentCount: Optional[int] = Field(None, description="Número de comentários")
    favoriteCount: Optional[int] = Field(None, description="Número de vezes adicionado aos favoritos (sempre 0)")
    duration: str = Field(..., description="Duração do vídeo no formato ISO 8601 (ex: PT5M30S)")
    caption: bool = Field(..., description="Se o vídeo tem legendas disponíveis (true ou false)")
    top_comments: Optional[List[str]] = Field(None, description="Lista com os primeiros comentários do vídeo")

    @classmethod
    def from_api_response(cls, videos: List[dict]) -> List["YouTubeVideo"]:
        """Cria uma lista de objetos YouTubeVideo a partir da resposta da API do YouTube."""
        video_objects = []
        for video in videos:
            video_objects.append(cls(
                videoId=video["id"],
                title=video["snippet"]["title"],
                description=video["snippet"].get("description", "Sem descrição disponível"),
                channelTitle=video["snippet"]["channelTitle"],
                channelId=video["snippet"]["channelId"],
                publishedAt=video["snippet"]["publishedAt"],
                thumbnails=video["snippet"]["thumbnails"]["default"]["url"],
                tags=video["snippet"].get("tags", []),
                categoryId=video["snippet"]["categoryId"],
                viewCount=int(video["statistics"].get("viewCount", 0)),
                likeCount=int(video["statistics"].get("likeCount", 0)) if "likeCount" in video["statistics"] else None,
                commentCount=int(video["statistics"].get("commentCount", 0)) if "commentCount" in video["statistics"] else None,
                favoriteCount=int(video["statistics"].get("favoriteCount", 0)),
                duration=video["contentDetails"]["duration"],
                caption=video["contentDetails"]["caption"] == "true",
                top_comments=[]  # Inicialmente vazio, será preenchido depois pelo TrendTool
            ))
        return video_objects

    def to_yaml(self) -> str:
        """Converte os dados do vídeo para o formato YAML."""
        return yaml.dump(self.dict(), allow_unicode=True, default_flow_style=False)



"""
# Suponha que tenhamos um vídeo do YouTube convertido em objeto
video = YouTubeVideo(
    title="Aprenda Python do Zero",
    description="Um curso completo para iniciantes!",
    channelTitle="Canal Tech",
    channelId="UC12345678",
    publishedAt="2024-03-10",
    thumbnails="https://img.youtube.com/vi/abc123/default.jpg",
    tags=["Python", "Programação", "Curso"],
    categoryId="27",
    viewCount=120000,
    likeCount=5000,
    commentCount=300,
    favoriteCount=0,
    duration="PT10M30S",
    caption=True,
    top_comments=["Ótima aula!", "Muito bem explicado!", "Python é incrível!"]
)

# Exibir o resumo formatado do vídeo
print(str(video))
"""