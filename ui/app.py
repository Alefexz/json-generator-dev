import sys
import os
import json
import streamlit as st

# -------------------------------------------------
# Garante que a pasta raiz esteja no PYTHONPATH
# -------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from core.generator import generate_copies


# -------------------------------------------------
# Configuração da página
# -------------------------------------------------
st.set_page_config(
    page_title="Bemol | Gerador de JSON DEV",
    page_icon="🧩",
    layout="wide"
)

# -------------------------------------------------
# Header com logo e título
# -------------------------------------------------
col_logo, col_title = st.columns([1, 6])

with col_logo:
    st.image("assets/Bemol_logo.png", width=160)

with col_title:
    st.markdown(
        """
        <h2 style="margin-bottom:0;">Gerador de JSON para Testes (DEV)</h2>
        <p style="color:gray; margin-top:4px;">
            Ferramenta interna para geração de arquivos .JSON fictícios para testes.
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------
# Entrada do JSON base
# -------------------------------------------------
json_text = st.text_area(
    "📋 Cole o JSON base",
    height=380,
    placeholder="Cole aqui o JSON completo que servirá como base"
)

# -------------------------------------------------
# Configurações principais
# -------------------------------------------------
st.subheader("⚙️ Configurações de Geração")

col1, col2, col3 = st.columns(3)

with col1:
    qty = st.number_input(
        "Quantidade de cópias",
        min_value=1,
        max_value=100,
        value=10
    )

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

# -------------------------------------------------
# Faixa customizada
# -------------------------------------------------
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

# -------------------------------------------------
# Campos a serem alterados
# -------------------------------------------------
st.subheader("🧩 Campos que serão alterados automaticamente")

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

# -------------------------------------------------
# Geração dos JSONs
# -------------------------------------------------
if st.button("🚀 Gerar JSONs"):
    if not json_text.strip():
        st.error("❌ Cole um JSON válido antes de gerar.")
    else:
        try:
            base_json = json.loads(json_text)

            month_map = {
                "Janeiro": 1,
                "Fevereiro": 2,
                "Março": 3,
                "Abril": 4,
                "Maio": 5,
                "Junho": 6,
                "Julho": 7,
                "Agosto": 8,
                "Setembro": 9,
                "Outubro": 10,
                "Novembro": 11,
                "Dezembro": 12
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

            results = generate_copies(
                base_json=base_json,
                quantity=qty,
                options=options
            )

            st.success(f"✅ {qty} JSONs gerados com sucesso")

            for i, item in enumerate(results, start=1):
                st.subheader(f"📄 JSON #{i}")
                st.code(
                    json.dumps(item, indent=2, ensure_ascii=False),
                    language="json"
                )

        except json.JSONDecodeError:
            st.error("❌ O conteúdo colado não é um JSON válido.")
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
