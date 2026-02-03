import sys
import os
import json
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from core.generator import generate_copies


st.set_page_config(page_title="Gerador de JSON DEV", layout="wide")

st.title("🔁 Gerador de JSON para testes (DEV)")

json_text = st.text_area(
    "📋 Cole o JSON base",
    height=380
)

st.subheader("⚙️ Configurações")

col1, col2, col3 = st.columns(3)

with col1:
    qty = st.number_input("Quantidade de cópias", 1, 100, 10)

with col2:
    month_name = st.selectbox(
        "Mês do CreatedAt",
        [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
    )

with col3:
    value_range = st.selectbox(
        "Faixa do TotalValue",
        [
            "50 a 100",
            "100 a 150",
            "150 a 300",
            "Valor livre"
        ]
    )

if value_range == "Valor livre":
    min_val = st.number_input("Valor mínimo", value=50.0)
    max_val = st.number_input("Valor máximo", value=100.0)
else:
    ranges = {
        "50 a 100": (50, 100),
        "100 a 150": (100, 150),
        "150 a 300": (150, 300)
    }
    min_val, max_val = ranges[value_range]

st.subheader("🧩 Campos que serão alterados aleatóriamente")

c1, c2, c3 = st.columns(3)

with c1:
    change_oid = st.checkbox("_id.$oid", True)
    change_transaction = st.checkbox("TransactionId", True)

with c2:
    change_contract = st.checkbox("ContractNumber", True)
    change_mdr = st.checkbox("FinancialInfos.MDRPercent", True)

with c3:
    change_total_value = st.checkbox("FinancialInfos.TotalValue", True)
    change_created_at = st.checkbox("CreatedAt", True)

if st.button("🚀 Gerar JSONs"):
    try:
        base_json = json.loads(json_text)

        month_map = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
            "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
            "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }

        options = {
            "oid": change_oid,
            "transaction": change_transaction,
            "contract": change_contract,
            "mdr": change_mdr,
            "total_value": change_total_value,
            "total_value_range": (min_val, max_val),
            "created_at": change_created_at,
            "month": month_map[month_name],
            "year": 2026
        }

        results = generate_copies(base_json, qty, options)

        st.success(f"✅ {qty} JSONs gerados")

        for i, item in enumerate(results, 1):
            st.subheader(f"JSON #{i}")
            st.code(json.dumps(item, indent=2, ensure_ascii=False), "json")

    except Exception as e:
        st.error(f"Erro: {e}")
