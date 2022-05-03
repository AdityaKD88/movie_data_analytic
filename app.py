import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

df=pd.read_csv('IMDB-Movie-Data.csv')

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
def index():
  return render_template('year.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 