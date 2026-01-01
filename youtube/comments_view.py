import streamlit as st
from comments_crew import YouTubeCommentsAnalyzer  # Importa a classe
import time  # Para simular tempo de processamento

# --- INTERFACE STREAMLIT ---

st.title("📊 YouTube Comments Analyzer")
st.write("Cole os links dos vídeos do YouTube para analisar os comentários.")

# Caixa de entrada para URLs dos vídeos
video_links_input = st.text_area(
    "Insira os links dos vídeos do YouTube (um por linha)",
    height=150,
    placeholder="https://www.youtube.com/watch?v=xxxxxxx\nhttps://www.youtube.com/watch?v=yyyyyyy"
)

# Converter a entrada para uma lista de links
video_links = [link.strip() for link in video_links_input.split("\n") if link.strip()]

# Botão para iniciar análise
if st.button("🔍 Analisar Comentários"):
    if not video_links:
        st.warning("⚠️ Por favor, insira pelo menos um link de vídeo do YouTube.")
    else:
        st.info("🔄 Processando análise, aguarde...")

        # Adicionando um Loader
        with st.spinner("🔎 Extraindo e analisando comentários... Isso pode levar alguns segundos..."):
            time.sleep(2)  # Simulação de tempo de espera
            analyzer = YouTubeCommentsAnalyzer()
            resultado = analyzer.kickoff(video_links=video_links)

        st.success("✅ Análise concluída!")
        st.write("### 📜 Relatório de Insights")
        st.text(resultado)  # Exibir relatório no formato de texto
