# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, dependencies

import plotly.express as px
import pandas as pd
from dash import dash_table
from datetime import timedelta
from datetime import datetime


lines=[]
tables=[]
table=[]
makespan=[]
with open(r'ResultatSolution.txt', 'r') as f:
    for line in f:
        lines.append(line)
        if line[0]==' ':
            table.append(line.strip("\n"))
        elif line[0]=='M':
            makespan.append(line.split()[-1])
        else :
            if len(table)>1:
                tables.append(table)
                table=[]
    tables.append(table)
dataframes=[]
for Table in tables:
    rows = [line.split(maxsplit=5) for i,line in enumerate(Table) if i!=1 and i!=len(Table)-1]
    df = pd.DataFrame(rows[1:],columns=rows[0])
    df.iloc[:,:-1]=df.iloc[:,:-1].astype(int)
    dataframes.append(df)
    
def gantt (df,makespan):
    start_time = (df['Start'] / 1440).apply(timedelta).apply(lambda x: datetime.today() + x).apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
    finish_time = (df['Finish'] / 1440).apply(timedelta).apply(lambda x: datetime.today() + x).apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))

    df_timeline = df[['Task', 'Start', 'Finish', 'Ressource ']].copy()
    df_timeline.loc[:,"Start"]=start_time.copy()
    df_timeline.loc[:,"Finish"]=finish_time.copy()


    fig = px.timeline(df_timeline, x_start='Start', y='Task',x_end='Finish',color='Ressource ',
                      title= f'Task Schedule: makespan = {makespan}', height=600)
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(width=0.7)
    return fig

app = Dash()

app.layout = html.Div([
    dcc.Graph(id='gantt-chart'),
    dcc.Slider(id='dataframe-slider', min=0, max=len(dataframes)-1, value=0, marks={i: str(i) for i in range(len(dataframes))},step=1),
    html.Div([
        dash_table.DataTable(id='table')
    ], style={'width': '50%', 'display': 'inline-block'})
])

@app.callback(
    [dependencies.Output('gantt-chart', 'figure'),dependencies.Output('table', 'data')],
    [dependencies.Input('dataframe-slider', 'value')]
)
def update_figure(value):
    return gantt(dataframes[value],makespan[value]),dataframes[value].to_dict('records')
if __name__ == '__main__':
    app.run_server()
