"""Une visualisation des écoles en france: Primaire et secondaire"""
import os
import time
import streamlit as st
import pandas as pd 
import pydeck as pdk

#LOADING DATA

ECOLES_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/ecoles_data.csv'
ECOLE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/ecole.csv'
COLLEGE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/college.csv'
LYCEE_DATA = 'https://raw.githubusercontent.com/MassDo/Ecoles/master/jupyter/data/lycee.csv'
start = 1

lg = {    
    "demo": ['Vidéo de démonstration', 'Demo video'],
    "title":['Écoles en France ⬇️', 'Schools in France ⬇️'],
    "lang":['Choisissez votre langue', 'Choose your language'],
    "dimension": ['Voir en 2D ?', 'See in 2D ?'],
    "legende_with": ["Largeur d'une cononne", 'Cell width'],
    "sidebar_data": ["Données", 'Data'],
    "sidebar_data_raw": ["Voir les données brutes", 'See raw data'],
    "sidebar_data1": ["Toutes les écoles", 'All schools'],
    "sidebar_data2": ["Écoles primaires", 'Primary schools'],
    "sidebar_data3": ["Collèges", 'Middle School'],
    "sidebar_data4": ["Lycées", 'High school'],
    "sidebar_county": ["Département", 'County'],
    "sidebar_radius": ["Diamètre d'un ⬡ (mètres)", 'Diameter of ⬡ (meters)'],
    "sidebar_height": ["Hauteur", 'Height'],
    "sidebar_opacity": ["Transparence", 'Opacity'],
}
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
        extruded=extruded,
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
    
    # HEAD    
    with st.beta_expander("Language"):
        language = st.radio('',('En', 'Fr'))
        if language == 'En':
            language = 1
        else:
            language = 0
    video_file = open('video/demo.webm', 'rb')
    video_bytes = video_file.read()
    with st.beta_expander(lg['demo'][language]):
        st.video(video_bytes)
    st.title(lg['title'][language])
    extruded_cb = st.checkbox(lg['dimension'][language])
    extruded = True
    if extruded_cb:
        extruded = False
                   
    # SIDEBAR
    with st.sidebar.beta_expander(lg['sidebar_data'][language]):
        url = ''
        f"""[{lg['sidebar_data_raw'][language]}](https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/export/?disjunctive.nom_etablissement&disjunctive.type_etablissement&disjunctive.appartenance_education_prioritaire&disjunctive.type_contrat_prive&disjunctive.code_type_contrat_prive&disjunctive.pial)"""
        school_name = st.radio(
            '', 
            (lg['sidebar_data1'][language], lg['sidebar_data2'][language], lg['sidebar_data3'][language], lg['sidebar_data4'][language])
        )
        if school_name == lg['sidebar_data1'][language]:
            url = ECOLES_DATA
        elif school_name == lg['sidebar_data2'][language]:
            url = ECOLE_DATA
        elif school_name == lg['sidebar_data3'][language]:
            url = COLLEGE_DATA
        elif school_name == lg['sidebar_data4'][language]:
            url = LYCEE_DATA
        
        county = [str(c) for c in st.multiselect(
            lg['sidebar_county'][language],
            range(1, 96)
        )]
        
    with st.sidebar.beta_expander(lg['sidebar_radius'][language]):
        radius = st.slider("", 100, 20000, 10000, 100) // 2

    with st.sidebar.beta_expander(lg['sidebar_height'][language]):
        hauteur = st.slider("",1, 200, 100, 10)

    with st.sidebar.beta_expander(lg['sidebar_opacity'][language]):
        opacity = st.slider('', 0.01, 1.0, 1.0, 0.01)  

    # MAP
    f"""{lg['sidebar_radius'][language]}: **{radius*2}m** - {lg['sidebar_data'][language]}: **{school_name}**"""
    if county:
        df = load_data(url)
        data = filter_data(df, county)
        mapp(data)
    else:
        mapp(url)

