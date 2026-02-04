import streamlit as st
import json
from core.generator import generate_copies
from datetime import datetime

# ---------------- CONFIG DA PÁGINA ----------------
st.set_page_config(
    page_title="JSON Generator Pro",
    page_icon="🧾",
    layout="centered"
)

# ---------------- HEADER COM LOGO ----------------
st.image("assets/logo.png", width=160)
st.title("JSON Generator Pro")
st.caption("Gerador inteligente de JSON para testes e simulações")

st.divider()

# ---------------- UPLOAD JSON ----------------
uploaded_file = st.file_uploader(
    "Upload do JSON base",
    type=["json"]
)

if uploaded_file:
    try:
        base_json = json.load(uploaded_file)
        st.success("JSON carregado com sucesso ✅")
    except Exception as e:
        st.error("Erro ao ler o JSON")
        st.stop()

    st.divider()

    # ---------------- CONFIGURAÇÕES ----------------
    st.subheader("Configurações de geração")

    quantity = st.number_input(
        "Quantidade de cópias",
        min_value=1,
        max_value=1000,
        value=10
    )

    # Escolha do mês
    selected_month = st.selectbox(
        "Mês para gerar o createAt",
        [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
    )

    # Range de valores
    value_range = st.selectbox(
        "Faixa de Total Value",
        [
            (50, 100),
            (100, 150),
            (150, 200),
            (200, 300)
        ],
        format_func=lambda x: f"R$ {x[0]} - R$ {x[1]}"
    )

    st.divider()

    # ---------------- SELLER UUID ----------------
    st.subheader("Seller UUID")

    manter_seller = st.checkbox(
        "Manter seller_uuid original do JSON",
        value=True
    )

    novo_seller_uuid = None

    if not manter_seller:
        novo_seller_uuid = st.text_input(
            "Novo seller_uuid",
            placeholder="Ex: 8f3a2c1d-1234-5678-9abc-abcdef123456"
        )

    st.divider()

    # ---------------- GERAR ----------------
    if st.button("🚀 Gerar JSONs"):
        result = generate_copies(
            base_json=base_json,
            quantity=quantity,
            month=selected_month,
            value_range=value_range,
            seller_uuid_override=novo_seller_uuid
        )

        output = json.dumps(result, indent=2, ensure_ascii=False)

        st.success("JSONs gerados com sucesso 🎉")

        st.download_button(
            label="📥 Baixar JSON",
            data=output,
            file_name="jsons_gerados.json",
            mime="application/json"
        )
