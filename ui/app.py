import json
import streamlit as st
from pathlib import Path
from core.generator import generate_copies

st.set_page_config(page_title="JSON Generator", layout="centered")

# Logo (como estava antes)
st.image("assets/Bemol_logo.png", width=160)

st.title("Gerador de JSON")

st.markdown("Cole o JSON base abaixo, escolha as opções e gere cópias automaticamente.")

# JSON base
base_json_text = st.text_area("JSON base", height=300)

# Quantidade
quantity = st.number_input("Quantidade de cópias", min_value=1, max_value=100, value=10)

# Mês de criação
month = st.selectbox(
    "Mês do CreatedAt",
    ["Janeiro"]
)

# Faixa de valor
value_range = st.selectbox(
    "Faixa do TotalValue",
    ["50 a 100", "100 a 150", "150 a 300"]
)

# 👉 NOVO: seller_uuid
st.subheader("Seller UUID")

manter_seller = st.checkbox(
    "Manter seller_uuid original",
    value=True
)

novo_seller_uuid = None
if not manter_seller:
    novo_seller_uuid = st.text_input("Novo seller_uuid")

# Botão
if st.button("Gerar JSONs"):
    try:
        base_json = json.loads(base_json_text)

        result = generate_copies(
            base_json=base_json,
            quantity=quantity,
            month=month,
            value_range=value_range,
            seller_uuid_override=novo_seller_uuid
        )

        st.success("JSONs gerados com sucesso!")
        st.code(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        st.error(f"Erro: {e}")
