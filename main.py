import streamlit as st
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recomendar_produtos_por_similaridade(cliente_id, matriz, top_n=5):
    if cliente_id not in matriz.index:
        st.text(f"Cliente '{cliente_id}' não encontrado na matriz.")
        return

    # Produtos que o cliente já possui
    produtos_do_cliente = matriz.loc[cliente_id]
    produtos_contratados = produtos_do_cliente[produtos_do_cliente == 1].index.tolist()

    st.text(f"\nProdutos já contratados por {cliente_id}:")
    if produtos_contratados:
        for p in produtos_contratados:
            st.text(f"{p}")
    else:
        st.text("  (nenhum produto contratado)")

    st.text('\n\n\n')

    # Calcular similaridade entre produtos (item-based)
    matriz_transposta = matriz.T
    similaridade_produtos = pd.DataFrame(
        cosine_similarity(matriz_transposta),
        index=matriz_transposta.index,
        columns=matriz_transposta.index
    )

    # Somar similaridades com os produtos que o cliente tem
    similaridade_total = similaridade_produtos[produtos_contratados].sum(axis=1)

    # Top produtos similares (inclusive os que o cliente já tem). Deixamos assim apenas pra visualização.
    top_recomendacoes = similaridade_total.sort_values(ascending=False).head(top_n)

    st.text(f"\nTop {top_n} produtos mais similares aos que {cliente_id} possui:")
    for produto, score in top_recomendacoes.items():
        status = "Já contratado" if produto in produtos_contratados else "Novo"
        st.text(f"  - Produto: {produto}\n     Similaridade: {score:.4f} | {status}\n")

    return top_recomendacoes

matriz = pd.read_csv('matriz.csv', index_col='cliente')

base_folder = 'produtos'
folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
produtos_usuarios = {}
produtos_count = {}
for folder in folders:
    usuarios = [u.replace('.json', '') for u in os.listdir(os.path.join(base_folder, folder))]
    produtos_count[folder] = len(usuarios)
    for usuario in usuarios:
        produtos_usuarios[usuario] = produtos_usuarios.get(usuario, []) + [folder]


st.title('🧠 Quantum Finance')
st.markdown('## Recomendação de Produtos')

st.markdown('### Usuário')
usuario_selecionado = st.selectbox('*Selecione um cliente*', produtos_usuarios.keys())

if usuario_selecionado:
    recomendar_produtos_por_similaridade(usuario_selecionado.split('_')[0], matriz)

st.markdown('### Em alta')

df = pd.DataFrame.from_dict(produtos_count, orient='index', columns=['**Contagem**'])
df.index.name = '**Produto**'
st.table(df, )


