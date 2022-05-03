import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

df=pd.read_csv('IMDB-Movie-Data.csv')

def count_genre(x):
    data_plot = df[x].str.cat(sep = ',')
    data = pd.Series(data_plot.split(','))
    info = data.value_counts(ascending=False)
    return info

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/top')
def top():
  info1 = pd.DataFrame(df['Revenue (Millions)'].sort_values(ascending = False))
  info1['title'] = df['Title']
  data = list(map(str,(info1['title'])))
  x = list(info1['Revenue (Millions)'][:10])
  y = list(data[:10])
  x.reverse(), y.reverse()
  fig1 = px.line(df,x=x,y=y, title='Top 10 Highest Revenue Movies',
              labels={
                  'x':'Revenue (in Millions)',
                  'y':'Movie Name'
              }, markers=True)
  graph1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

  info2 = pd.DataFrame(df['Runtime (Minutes)'].sort_values(ascending = False))
  info2['title'] = df['Title']
  data = list(map(str,(info2['title'])))
  x = list(info2['Runtime (Minutes)'][:10])
  y = list(data[:10])
  x.reverse(), y.reverse()
  fig2 = px.line(df,x=x,y=y, title='Top 10 Longest Movies',
                labels={
                    'x':'Revenue (in Millions)',
                    'y':'Movie Name'
                }, markers=True)
  graph2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

  info3 = pd.DataFrame(df['Votes'].sort_values(ascending = False))
  info3['title'] = df['Title']
  data = list(map(str,(info3['title'])))
  x = list(info3['Votes'][:10])
  y = list(data[:10])
  x.reverse(), y.reverse()
  fig3 =px.line(df,x=x,y=y, title='Top 10 Movies with highest votes',
                labels={
                    'x':'Total Vote',
                    'y':'Movie Name'
                }, markers=True)
  graph3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

  info4 = pd.DataFrame(df['Rating'].sort_values(ascending = False))
  info4['title'] = df['Title']
  data = list(map(str,(info4['title'])))
  x = list(info4['Rating'][:10])
  y = list(data[:10])
  x.reverse(), y.reverse()
  fig4 = px.line(df,x=x,y=y, title='Top 10 highest rating Movies',
                labels={
                    'x':'Rating',
                    'y':'Movie Name'
                }, markers=True)
  graph4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('top.html',graph1=graph1,graph2=graph2,graph3=graph3,graph4=graph4)

@app.route('/year')
def year():
  x=df['Year'].sort_values().unique()
  y=df.groupby('Year').count()['Title']
  fig5 = px.bar(df, x=x, y=y, color=x, title='Year Vs Movie Release',
                  labels={
                            'x':'Year',
                            'y':'Count'
                        })
  graph5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

  yr = df['Year'].value_counts()
  fig6 = px.pie(df,names=yr.index,values=yr.values,title='Percentage of movies released per year')
  graph6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

  x=df['Year'].sort_values().unique()
  y=df.groupby('Year').mean()['Revenue (Millions)']
  fig7 =px.bar(df, x=x, y=y, color=x, title='Year Vs Mean Revenue',
                labels={
                          'x':'Year',
                          'y':'Average Revenue'
                      })
  graph7 = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('year.html',graph5=graph5,graph6=graph6,graph7=graph7)

@app.route('/rate')
def rate():
  rating = df['Rating'].value_counts()
  fig8 = px.bar(df, x=rating.index.values, y=rating.values, color=rating.index.values,
                title='Rating count of movies',
                labels={'x':'Rating',
                        'y':'No. of Movies'})
  graph8 = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)

  m_score = df['Metascore'].value_counts()
  fig9 = px.bar(df, x=m_score.index.values, y=m_score.values, color=m_score.index.values,
                title='Metascore count of movies',
                labels={'x':'Metascore',
                        'y':'No. of Movies'})
  graph9 = json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder)

  fig10 = px.scatter(df,x=df['Rating'].values,y=df['Title'].values,
            title='Rating of different movies',color=df['Rating'].values,
            height=1600, labels={
                'x':'Rating',
                'y':'Movie Name'
            })
  graph10 = json.dumps(fig10, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('rate.html',graph8=graph8,graph9=graph9,graph10=graph10)

@app.route('/genre')
def genre():
  gen=count_genre('Genre')
  fig11 = px.bar(df, x=gen.values, y=gen.index, orientation='h',color=gen.index,
              title='Genre with Highest release',
              labels={'x':'No. of Movies',
                      'y':'Genre'})
  graph11 = json.dumps(fig11, cls=plotly.utils.PlotlyJSONEncoder)

  fig12 = px.pie(df, names=gen.index, values=gen.values, title='Percentage of genre of movies')
  graph12 = json.dumps(fig12, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('genre.html',graph11=graph11,graph12=graph12)

@app.route('/act')
def act():
  actors = count_genre('Actors')
  n=actors.iloc[:20]
  fig13 = px.bar(df,y=n.values, x=n.index,color=n.index,
          title='Most Frequent Actor',
          labels={'x':'Actor Name',
                  'y':'No. of Movies'})
  graph13 = json.dumps(fig13, cls=plotly.utils.PlotlyJSONEncoder)

  director = count_genre('Director')
  n=director.iloc[:20]
  fig14 = px.bar(df,y=n.values, x=n.index,color=n.index,
          title='Most Frequent Director',
          labels={'x':'Director Name',
                  'y':'No. of Movies'})
  graph14 = json.dumps(fig14, cls=plotly.utils.PlotlyJSONEncoder)

  return render_template('act.html',graph13=graph13,graph14=graph14)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 