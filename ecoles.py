"""Une visualisation des écoles en france: Primaire et secondaire"""

import streamlit as st
import pandas as pd 
import pydeck as pdk

#LOADING DATA
ECOLE_DATA = 'https://raw.githubusercontent.com/MassDo/test/main/ecoles_data.csv'


@st.cache
def load_data():
    data = pd.read_csv(ECOLE_DATA).dropna()
    # data.to_csv('./ec.csv', index=False)
    # data = pd.read_csv('./ec.csv') 
    # data = data.to_dict('records')
    return data


"""
    # Visualisations des écoles en France, données publiques
"""

if st.checkbox('see data ? ⬇️'):
    data
    f"""### Vous pouvez trouvez la source des données [ici]({ECOLE_DATA})""" 


# LAYER 
def map(data):
    f"""**Infos**: chaque colonne fait {radius*2}m de largeur !"""
    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=2.415,
        latitude=46,
        zoom=5,
        min_zoom=1,
        max_zoom=20,
        pitch=40.5,
        bearing=-27.36,)
    
    # Define a layer to display on a map
    ecoles=pdk.Layer(
        "HexagonLayer",
        data,
        get_position=["longitude", "latitude"],
        #get_position=["longitude", "latitude"],
        auto_highlight=False,
        elevation_scale=hauteur,
        pickable=True,
        elevation_range=[0, 2000],
        extruded=True,
        coverage=1,
        radius= radius,
        opacity=opacity
    )

    st.pydeck_chart(pdk.Deck(
        layers=[ecoles],
        initial_view_state=view_state, 
        tooltip=True,
        )        
    )
    

st.title('Ecoles en france ⬇️')
expander_rayon = st.sidebar.beta_expander("Rayons Hexagones en metres")
with expander_rayon:
    """Le territoire est maillé en **hexagone ⬡**,\
    toutes les écoles à l'intérieur d'un hexagones\
     sont cumulés et donne la hauteur de la colonne ⬆️"""
    radius = st.slider("Diamètre d'un ⬡ en mètres ", 100, 20000, 10000, 100) // 2

expander_hauteur = st.sidebar.beta_expander("Hauteur")
with expander_hauteur:
    """Multiplication par un coeficient des hauteur des colonnes,\
        pour un soucis de visibilitée ⬆️"""
    hauteur = st.slider("Hauteur d'un  ⬡",1, 200, 100, 10)

expander_transparence = st.sidebar.beta_expander("Transparence")
with expander_transparence:
    """Transparence des colonnes"""
    opacity = st.slider('Transparence', 0.01, 1.0, 1.0, 0.01)


if __name__ == '__main__':
    data = load_data()
    map(DATA_URL)
