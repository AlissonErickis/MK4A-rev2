
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inspeção Visual - MK4A", layout="wide")

st.title("Checklist de Inspeção Visual - MK4A")

tipos_defeitos = [
    "Arranhões", "Bolhas", "Escorrimento", "Falha de Pintura", "Marca de Rolo",
    "Olho de Peixe", "Ondulação", "Poros", "Rugosidade", "Sujeira", "Outros"
]

# Definir regiões e seus respectivos raios
regioes = {
    "CASCA WW": list(range(1, 18)),
    "CASCA LW": list(range(18, 35)),
    "BORDA DE ATAQUE": list(range(35, 52)),
    "BORDA DE FUGA": list(range(52, 69)),
    "OUTROS": list(range(69, 82))
}

# Inicializar dicionário de respostas
respostas = []

with st.form("formulario_inspecao"):
    st.subheader("Dados Gerais")
    numero_pa = st.text_input("Número da Pá")
    molde = st.text_input("Molde")
    modelo = st.text_input("Modelo")
    responsavel = st.text_input("Responsável")
    data = st.date_input("Data")

    st.markdown("---")
    st.subheader("Checklist de Inspeção por Raio")

    for regiao, raios in regioes.items():
        st.markdown(f"### {regiao}")
        for raio in raios:
            cols = st.columns([1, 1, 2])
            nok = cols[0].checkbox("NOK", key=f"nok_{raio}")
            tipo_defeito = ""
            observacao = ""
            if nok:
                tipo_defeito = cols[1].selectbox("Tipo de Defeito", tipos_defeitos, key=f"defeito_{raio}")
                observacao = cols[2].text_input("Observações", key=f"obs_{raio}")
            respostas.append({
                "Raio": raio,
                "Região": regiao,
                "Status": "NOK" if nok else "OK",
                "Tipo de Defeito": tipo_defeito,
                "Observações": observacao
            })

    submitted = st.form_submit_button("Salvar Checklist")
    if submitted:
        df = pd.DataFrame(respostas)
        df.insert(0, "Número da Pá", numero_pa)
        df.insert(1, "Molde", molde)
        df.insert(2, "Modelo", modelo)
        df.insert(3, "Responsável", responsavel)
        df.insert(4, "Data", data)
        df.to_csv("checklist_inspecao_mk4a.csv", index=False)
        st.success("Checklist salvo com sucesso!")
        st.download_button("📥 Baixar CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="checklist_inspecao_mk4a.csv", mime="text/csv")
