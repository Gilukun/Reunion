#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:58:23 2021

@author: gillesv
"""

import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import datetime as dt
import seaborn as sns

from bokeh.plotting import figure, output_notebook, show
output_notebook()

from bokeh.tile_providers import get_provider 
from  bokeh.models import ColumnDataSource, HoverTool
from  bokeh.models import LabelSet
import re

from plotly.subplots import make_subplots
import plotly.express as px
import os
import plotly.graph_objects as go

import folium

st.set_page_config(layout="wide")

covid= pd.read_csv('donnees-hospitalieres-covid19-lareunion.csv', sep=';')
tourist= pd.read_csv('frequentation-touristique-mensuelle-irtmta-lareunion.csv', sep=';')
pop_activ= pd.read_csv('population-active-de-15-ans-ou-plus-ayant-un-emploi-par-sexe-lieu-de-travail-et-.csv', sep=';')
revenu= pd.read_csv('revenus-declares-pauvrete-et-niveau-de-vie-en-2015-irispublic.csv', sep=';')
chom= pd.read_csv('nombre-de-demandeurs-demploi-par-departement-france.csv', sep=';')

Navigation = st.sidebar.radio("Navigation", ("Home","Economy","Geography","Population","Trivia") )

if Navigation == "Home":
    st.header("Let's discover Réunion Island")
    
    

if Navigation =="Economy":
    st.header("Evolution du chomage à la Réunion (1996-2021")
    
    chomdate = chom.groupby(['Date'], as_index=False).agg({'Nb moyen demandeur emploi' : 'mean'})
    chomline = px.line(chomdate, x="Date", y="Nb moyen demandeur emploi", 
                   title='Nombre Moyen de demandeur d emploi à La Réunion', 
                   width= 1600,
                   height= 500)

    chomline.update_layout(xaxis=dict(
                                showline=True,
                                showgrid=False,
                                showticklabels=True,
                                linecolor='rgb(19, 141, 117)',
                                linewidth=2,
                                ticks='outside',
                                tickfont=dict( family='Arial', size=12, color='rgb(82, 82, 82)')),
                            yaxis=dict(
                                showline=True,
                                showgrid=False,
                                zeroline=True,
                                showticklabels=True,
                            linecolor='rgb(19, 141, 117)',
                            linewidth=2),
                            autosize=True,
                            showlegend=False,
                            plot_bgcolor='White')
    st.plotly_chart(chomline)
    
        
    st.header("Répartition des personnes sans emploi")
    
    
    chomdate = chom.groupby(['Date'], as_index=False).agg({'Nb moyen demandeur emploi' : 'mean'})
    chomdate.head()
    
    popactive=331000
    chomdelta = chomdate.loc[chomdate['Date'] == "2020"]
    chomdelta["Population 2020"] = popactive
    chomdelta['Delta'] = chomdelta["Nb moyen demandeur emploi"] / chomdelta["Population 2020"]*100
    
    chomdelta=chomdelta.transpose()
    
    
    col1, col2 = st.columns((1,1))
    with col1 :
        chomdelta = px.pie(chomdelta, 
                           values=['66204', '331000'],
                           hover_name=({'66204': 'Perssonnes sans emploi',
                                        '331000': 'Population active'}),
                           hole=0.6,
                           width=700,
                           height=800)
        
        chomdelta.update_layout(title_text="Répartition des personnes sans emplois à la Réunion (2020)",
                                annotations=[dict(text='Pop Active(15-65ans): 331000', 
                                             x=0.5, y=0.5, 
                                             font_size=20,
                                             showarrow=False,
                                             opacity= 0.8)],)
        
        chomdelta.update_traces(textposition='inside', 
                                marker=dict(colors=['#F1948A', '#E9F7EF '],
                                line=dict(color='#FDFEFE', width=10)))
        
        chomdelta.add_annotation(x=0.4, y=0.9,
                    text="Pourcentage de personnes sans emploi au 1er Janvier 2021",
                    showarrow=True,
                    yshift=10)
        st.plotly_chart(chomdelta)
    
    with col2:
        chomgenres = chom.loc[chom['Date']=="2020"]
        values= list([chomgenres['Nb moyen demandeur emploi Homme'].mean(), chomgenres['Nb moyen demandeur emploi Femme'].mean()])
        
        chomgenre = px.pie(chomgenres, 
                           values= [77630.0, 83575.0],
                           hover_name=({'Nb moyen demandeur emploi Homme': 'Homme',
                                        'Nb moyen demandeur emploi Femme': 'Femme'}), 
                           hole=0.6, 
                           width=700,
                           height=800)

        chomgenre.update_layout(title_text="Répartition des personnes sans emplois à la Réunion par genre (2020)",
                                annotations=[dict(text='Pop Active(15-65ans): 331000', 
                                             x=0.5, y=0.5, 
                                             font_size=20,
                                             showarrow=False,
                                             opacity= 0.8)],)
        
        chomgenre.update_traces(textposition='inside', 
                                marker=dict(colors=['#F1948A', '#E9F7EF '],
                                line=dict(color='#FDFEFE', width=10)))


        st.plotly_chart(chomgenre)

    st.header("Revenu")
    
    medville = revenu.groupby(['Libellé de la commune'], as_index=False).agg({'Mediane(€)' : 'mean'})
    medville.sort_values(by = 'Mediane(€)', ascending = False)
    medville['Med'] = round(medville['Mediane(€)'].mean())
    
    
    med = px.scatter(medville, 
               x='Libellé de la commune', 
               y='Mediane(€)',
               size='Mediane(€)',
               color='Mediane(€)',
               hover_name='Mediane(€)',
               color_continuous_scale =px.colors.sequential.Magenta,
               width=1500,
               height=700,
                     title="Revenu médians par communes")
    med.add_hline(y=14437)
    
    med.update_layout(font=dict( family="Droid Sans Mono", size=14, color="RebeccaPurple"),
                      title_font_family="Times New Roman",
                      title_font_color="Black",
                      legend_title_font_color="green",
                      xaxis_title="Nom de la commune",
                      yaxis_title="Revenu Médian en Euro (€)")
    
    med.add_annotation(x=1, y=14437,
                text="Médiane des revenus",
                showarrow=False,
                yshift=10)
    
    med.update_layout(showlegend=False)
    
    st.plotly_chart(med)
    
    st.header("Mode de transport")
    
    st.write("Mode de transport les plus utilisés à La Réunion par commune")
    modetrans = pop_activ.groupby(['Mode de transport','Commune'], as_index=False).agg({'Nombre de personnes' : 'sum'})
    modetrans.drop(modetrans.loc[modetrans['Mode de transport']=="Pas de transport"].index, inplace=True)
    transportation = px.scatter(modetrans, 
           x='Commune', 
           y='Mode de transport',
           size='Nombre de personnes',
           color='Nombre de personnes',
           hover_name='Mode de transport',
           color_continuous_scale =px.colors.sequential.RdBu,
           width=1500,
           height=900,
          symbol = 'Mode de transport')
    transportation.update_xaxes(categoryorder='category ascending')

    transportation.update_layout(legend=dict(yanchor="top",
                                            y=1.2,
                                            xanchor="right",
                                            x=0.5))
    
    transportation.update_traces(marker_sizemin = 2) 
    
    st.plotly_chart(transportation)
        
    
#if Navigation =="Geography":
    

#if Navigation =="Population":


#if Navigation =="Transportation":