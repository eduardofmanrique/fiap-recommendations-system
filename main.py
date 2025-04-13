import streamlit as st
import os
import pandas as pd


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
    st.markdown('**Produtos Contratados**')
    for produto in produtos_usuarios[usuario_selecionado]:
        st.text(f'•  {produto}')

    st.markdown('**Produtos Recomendados**')

st.markdown('### Em alta')

df = pd.DataFrame.from_dict(produtos_count, orient='index', columns=['**Contagem**'])
df.index.name = '**Produto**'
st.table(df, )


