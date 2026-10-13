from youtube_data import YoutubeData # Nacitam YoutubeData model

import pandas as pd # Nacitanie, filtrovanie, triedenie a nalyzovanie dat z CSV
import plotly.express as px # Vytvaranie interaktivnych grafov
import matplotlib.pyplot as plt # Vytvaranie statickych grafov a ich prisposobovanie

#csv_path = YoutubeData("@PPPiter_Official").download_csv() # Nacita path csv suboru pomocou method v youtube_data.py
csv_path = "data/pppiter_official(08-10-26).csv" # Docasna path nech neminam API tokeny pri kazdom calle

df = pd.read_csv(csv_path) # Otvori CSV a nacita jeho obsah do objektu nazyvaneho DataFrame
df['published_at'] = pd.to_datetime(df['published_at']) # Prevedie hodnotu datumu z textoveho formatu na datumovy typ
df = df.sort_values('published_at') # Zoradi riadky v CSV chronologicky od najstarsieho videa po najnovsie,
                                    #  ak by som pridal 'ascending=False', otocim poradie

x_value = 'title' # Nazov a hodnota X, netreba pisat x_values = df['title'],
                  #  pretoze plotly.express si vie nazvy vyhladat automaticky
y_value = 'views' # Nazov a hodnota Y

fig = px.area( # fig=Figure, jadro grafu, konfigurujem tu graf
    df,        # px.area vytvori graf s vyplnou, 'filled area chart'
    x=x_value,
    y=y_value,
    title="PPPiter_Official videos, 2026",
    template='plotly_dark',
    width=1400,
    height=700,
    markers=True,
    line_shape='linear',
    hover_name='title',
    hover_data=['published_at'],
    labels={
              'title': "Video",
              'views': "Views",
              'published_at': "Published",
              },
    category_orders={
              'title': df['title'].tolist(),
              },
)
fig.update_traces(
    line=dict(
        color="#22D3EE",
        width=3,
    ),
    fillcolor="rgba(34, 211, 238, 0.20)",
    marker=dict(
        size=8,
        color="#FFFFFF",
    ),
)


fig.show() # Zobrazi graf
