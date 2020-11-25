"""Une visualisation des écoles en france: Primaire et secondaire"""
import os
import streamlit as st
import pandas as pd 
import pydeck as pdk

#LOADING DATA

ECOLES_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/ecoles_data.csv'
ECOLE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/ecole.csv'
COLLEGE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/college.csv'
LYCEE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/lycee.csv'

@st.cache
def load_data(url):
    df = pd.read_csv(url)
    return df

@st.cache
def filter_data(df, county):
    data = pd.DataFrame()
    frames = []
    for c in county:
        if len(c) == 1:
            c = "0" + c
        frames.append(df[df['Code_departement'] == str(c)])
        data = pd.concat(frames)
    return data

# LAYER 
def mapp(data):    
    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=2.415,
        latitude=46,
        zoom=5,
        min_zoom=1,
        max_zoom=20,
        pitch=40.5,
        bearing=-27.36,
    )    
    # Define a layer to display on a map
    ecoles=pdk.Layer(
        "HexagonLayer",
        data,
        get_position=["longitude", "latitude"],
        #get_position=["longitude", "latitude"],
        auto_highlight=True,
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
        tooltip={
            "text": "Number of schools: {elevationValue}"
        },
        )        
    )

if __name__ == '__main__':
    
    st.title('Ecoles en france ⬇️')
    # SIDEBAR
    expander_data = st.sidebar.beta_expander("Data")
    with expander_data:
        url = ''
        school_name = st.radio(
            'DataSet', 
            ('All schools - (Toutes les écoles)', 'Primary schools - (Écoles primaires)', 'Middle School - (Collèges)', 'High school - (Lycées)')
        )
        if school_name == 'All schools - (Toutes les écoles)':
            url = ECOLES_DATA
        elif school_name == 'Primary schools - (Écoles primaires)':
            url = ECOLE_DATA
        elif school_name == 'Middle School - (Collèges)':
            url = COLLEGE_DATA
        elif school_name == 'High school - (Lycées)':
            url = LYCEE_DATA
        
        county = [str(c) for c in st.multiselect(
            'County - (Département)',
            range(1, 96)
        )]
        
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

    
    f"""**Infos**: chaque colonne fait {radius*2}m de largeur !"""
    if county:
        df = load_data(url)
        data = filter_data(df, county)
        mapp(data)
    else:
        mapp(url)

