import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pandas as pd
import requests
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

CHESSCOM_PROFILE = 'https://www.chess.com/member/mikeredfox'
df = pd.read_feather('chess_clean.feather')
CHESS_ANIM = 'https://assets1.lottiefiles.com/packages/lf20_pusTlimrh3.json'
MAIL_ANIM = 'https://assets2.lottiefiles.com/packages/lf20_u25cckyh.json'

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.experimental_memo
def data_viz():
    st.write(f'## Here are some graphs')
    a,b = st.columns(2)


    with a:
        fig = px.bar(df['result'].value_counts(), labels={
            'value':'count',
            'index':'result'
        })
        st.plotly_chart(fig)

    with b:
        fig = px.scatter(df,x='date',y='avg_score',color='result',trendline='ols')
        st.plotly_chart(fig)
    



    fig = px.scatter(df,x='date',y='my_elo',color='result',symbol='rated',labels={
        'date':'Date',
        'my_elo': 'My elo value'
    })

    fig = px.scatter(df,x='date',y='my_elo',
                    color='result',
                    symbol='rated',
                    symbol_sequence= ['circle-dot', 'square'],
                    width=1700, height=700,labels={
        'date':'Date',
        'my_elo': 'My elo value'
    })

    st.plotly_chart(fig)

# Title
st.set_page_config(page_title='Analysis of my chess games ♟️', page_icon=':white_circle:',layout='wide')

st.write(f"""

# MikeRedfox's games analysis

Data on my games on chess.com, [here]({CHESSCOM_PROFILE}) is my profile!


""")

selected = option_menu(
    menu_title=None,
    options=["Data", "Data Visualization", "Contact me"],
    icons=["pencil-fill", "bar-chart-fill", "envelope"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
    styles={
        "nav-link-selected": {"background-color": "#5B98EF"},
    }
)

if selected == 'Data':

    st.write('The dataframe has this form')
    st.write(df.head())
    
    info, anim = st.columns(2)
    with info:
        st.write('''
        ## Some info about the columns

        - date : Self-explanatory
        - white: Name of white player
        - black : Name of black player
        - resut : Self-explanatory
        - game : The pgn for that game as a string
        - my_elo : My chess.com elo value during that game
        - opp_elo : My opponent's chess.com elo value during that game
        - rated : If that game was rated or not
        - avg_score: The average score for that game in [centipawns](https://chess.fandom.com/wiki/Centipawn) (positive = my advantage)


        ''')
    with anim:
        st_lottie(load_lottie_url(CHESS_ANIM), height=400, speed=0.5)
    s ='''$ \mu_{elo} = $''' + rf'''{round(df['my_elo'].mean(),2)}'''
    st.write(f'### My average  elo')
    st.write(s)

    st.download_button(label='Download dataframe', data='chess_clean.feather',file_name='MikeRedfox_games.feather')

if selected == 'Data Visualization':

    data_viz()

token = 'c86aff13d413ddd50e7d9265c9c61e5d'

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if selected == 'Contact me':

    contact, anim = st.columns((3,1))

    with contact:
        st.write(f'''

        
        <form action="https://formsubmit.co/{token}" method="POST">
        <input type="email" name="email" placeholder='Your email address' required>
        <input type="text" name="name" placeholder='Your name' required>
        <br />
        <textarea id="subject" name="subject" placeholder='Your message' ></textarea>
        <br />
        <button type="submit">Send</button>
    </form>
        ''', unsafe_allow_html=True)

    with anim:
        st_lottie(load_lottie_url(MAIL_ANIM), height=350, speed=0.5)