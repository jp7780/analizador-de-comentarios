import streamlit as st
import json
import time  # Para simular tempo de carregamento
from trends_crew import YouTubeTrendAnalyzer  # Importa a Crew

# Carregar os JSONs com os dados de categorias e regiões
with open("yt_categories.json", "r", encoding="utf-8") as f:
    categories_data = json.load(f)

with open("yt_regions.json", "r", encoding="utf-8") as f:
    regions_data = json.load(f)

# Criar mapeamento de ID para Nome
category_mapping = {item["id"]: item["snippet"]["title"] for item in categories_data["items"]}
region_mapping = {item["id"]: item["snippet"]["name"] for item in regions_data["items"]}

# Inverter os dicionários para mapeamento Nome -> ID
category_reverse_mapping = {v: k for k, v in category_mapping.items()}
region_reverse_mapping = {v: k for k, v in region_mapping.items()}

# Interface Streamlit
st.title("📊 YouTube Trend Analyzer")
st.header("Configuração da Análise")

# Campo de seleção para categoria
category_name = st.selectbox("Escolha a Categoria", list(category_mapping.values()))
category_id = category_reverse_mapping[category_name]  # Obter o ID correspondente

# Campo de seleção para região
region_name = st.selectbox("Escolha a Região", list(region_mapping.values()))
region_id = region_reverse_mapping[region_name]  # Obter o ID correspondente

# Parâmetros adicionais
max_results = st.number_input("Quantidade de vídeos a buscar", min_value=1, max_value=50, value=10)
num_comments = st.number_input("Quantidade de comentários a analisar por vídeo", min_value=1, max_value=100, value=5)

# Botão de análise com Loader
if st.button("🔍 Executar Análise"):
    with st.spinner("🔎 Buscando tendências... Isso pode levar alguns segundos..."):
        time.sleep(2)  # Simulação de tempo de espera

        # Criar e executar a análise
        analyzer = YouTubeTrendAnalyzer()
        inputs = {
            "category": category_id,
            "region": region_id,
            "max_results": max_results,
            "num_comments": num_comments
        }
        resultado = analyzer.kickoff(inputs=inputs)

    # Exibir o resultado
    st.success("✅ Análise concluída!")
    st.write("### 📜 Relatório de Tendências")
    st.text(resultado)  # Exibir relatório no formato de texto
