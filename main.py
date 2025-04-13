import streamlit as st
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_produtos_por_similaridade(cliente_id, matriz, top_n=5):
    if cliente_id not in matriz.index:
        st.error(f"🚫 Cliente **{cliente_id}** não encontrado na matriz.")
        return

    produtos_do_cliente = matriz.loc[cliente_id]
    produtos_contratados = produtos_do_cliente[produtos_do_cliente == 1].index.tolist()

    st.subheader("📦 Produtos já contratados")
    if produtos_contratados:
        for p in produtos_contratados:
            st.markdown(f"- **{p}**")
    else:
        st.info("Nenhum produto contratado.")

    st.markdown("---")

    # Similaridade entre produtos
    matriz_transposta = matriz.T
    similaridade_produtos = pd.DataFrame(
        cosine_similarity(matriz_transposta),
        index=matriz_transposta.index,
        columns=matriz_transposta.index
    )

    similaridade_total = similaridade_produtos[produtos_contratados].mean(axis=1)
    top_recomendacoes = similaridade_total.sort_values(ascending=False).head(top_n)

    st.subheader(f"🔍 Top {top_n} recomendações para o cliente **{cliente_id}**")

    for produto, score in top_recomendacoes.items():
        status = "Já contratado" if produto in produtos_contratados else "Novo"
        cor = "green" if produto in produtos_contratados else "blue"
        st.markdown(
            f"""
            <div style="padding: 8px; border-radius: 8px; background-color: #f0f2f6; margin-bottom: 8px;">
                <strong>{produto}</strong><br>
                Similaridade: <span style="color:{cor}; font-weight: bold;">{score:.4f}</span> &nbsp;|&nbsp; {status}
            </div>
            """,
            unsafe_allow_html=True
        )

    return top_recomendacoes

matriz = pd.read_csv('matriz.csv', index_col='cliente')

base_folder = 'produtos'
folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
produtos_usuarios = {}
produtos_count = {}
for folder in folders:
    usuarios = [u.replace('.json', '') for u in os.listdir(os.path.join(base_folder, folder))]
    produtos_count[folder] = len(usuarios)
    for u in usuarios:
        user, cpf = u.split('_')
        produtos_usuarios[f"cliente: {user} - CPF: {cpf}"] = produtos_usuarios.get(f"cliente: {user} - CPF: {cpf}", []) + [folder]


st.title('🧠 Quantum Finance')
st.markdown('## Recomendação de Produtos')

st.markdown('### Usuário')
usuario_selecionado = st.selectbox('*Selecione um cliente*', sorted(produtos_usuarios.keys()))

if usuario_selecionado:
    recomendar_produtos_por_similaridade(usuario_selecionado.replace('cliente: ','').split(' -')[0], matriz)

st.markdown('### Em alta')

df = pd.DataFrame.from_dict(produtos_count, orient='index', columns=['**Contagem**'])
df.index.name = '**Produto**'
st.table(df.sort_values('**Contagem**',ascending = False))


