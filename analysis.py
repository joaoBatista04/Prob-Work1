# https://www.kaggle.com/datasets/inductiveanks/employee-salaries-for-different-job-roles

# work_year
# experience_level
# employment_type
# job_title
# salary
# salary_currency
# salary_in_usd
# employee_residence
# remote_ratio
# company_location
# company_size

# Escolher algum problema (conjunto de dados) e fazer análise descritiva.

# Apresentar slides com gráficos, tabelas e medidas resumo.

# Pode usar o kaggle para procurar dados (mas pode ser outro dado qualquer). Necessário ter pelo menos duas variáveis quantitativas e duas qualitativas.
# quantitativa x quantitativa (salary_in_usd x remote_ratio)
# quantitativa x qualitativa (salary_in_usd x company_size, salary_in_usd x company_location, salary_in_usd X experience_level)
# qualitativa x qualitativa

#CELL 1
import pandas as pd

data = pd.read_csv("./ds_salaries.csv").drop("Unnamed: 0", axis=1)
data.head()

#CELL 2
print(data['work_year'].unique())
print(data['experience_level'].unique())
print(data['employment_type'].unique())
print(data['job_title'].unique())
#print(data['salary'].unique())
#print(data['salary_in_usd'].unique())
print(data['employee_residence'].unique())
print(data['remote_ratio'].unique())
print(data['company_location'].unique())
print(data['company_size'].unique())

#CELL 3
print("Media: $" + str(round(data['salary_in_usd'].mean(), 2)))
print("Mediana: $" + str(round(data['salary_in_usd'].median(), 2)))
print(data.mode())

#CELL 4
#salary_in_usd x remote_ratio

import plotly.express as px
import plotly.graph_objects as go
plot = px.scatter(data, x='salary_in_usd', y='remote_ratio', color='company_location', labels={
    'remote_ratio': 'Modalidade de Trabalho (Remoto)',
    'company_location': 'País de Origem da Empresa',
    'salary_in_usd': 'Salário em Dólares'
})
plot.show()

#CELL 5
# salary_in_usd x company_location

quantidade_vagas_paises = data['company_location'].value_counts()

data_graph = quantidade_vagas_paises.loc[quantidade_vagas_paises > 3]
sum = quantidade_vagas_paises.loc[quantidade_vagas_paises <= 3].sum()

data_graph['Outros'] = sum

data_graph = data_graph.to_frame()
data_graph.index

plot = px.pie(data, names=data_graph.index, values=data_graph['company_location'], title='Quantos empregados em cada país?')
#plot.update_traces(textposition='inside', textinfo='percent+label')
plot.show()

#CELL 6
fig = px.box(data, y='salary_in_usd', x='remote_ratio', color='remote_ratio',
             labels={
                'remote_ratio': 'Modalidade de Trabalho (Remoto)',
                'company_location': 'País de Origem da Empresa',
                'salary_in_usd': 'Salário em Dólares'
             })
fig.show()

#CELL 7
# salary_in_usd X experience_level



median_salaries = data.groupby('experience_level')['salary_in_usd'].median().reset_index() # pega a mediana por ser um grupo bem disperso

print(median_salaries.head())

fig = px.histogram(median_salaries, x="experience_level", y="salary_in_usd",
                   category_orders=dict(experience_level=["EN", "MI", "SE", "EX"]),
                   color="experience_level",
                   labels={
                      "salary_in_usd" : "Salários em Dólar",
                      "experience_level" : "Nível de Experiência",
                   })

fig.update_layout( yaxis_title="Salários em Dólar" )
fig.show()

#CELL 8
# salary_in_usd x company_size

median_salaries = data.groupby('company_size')['salary_in_usd'].median().reset_index() # pega a mediana por ser um grupo bem disperso

print(median_salaries.head())

fig = px.histogram(median_salaries, x="company_size", y="salary_in_usd",
                   labels={
                      "salary_in_usd" : "Salários em Dólar",
                      "company_size" : "Tamanho da Empresa"
                   },
                   color="company_size",
                   category_orders=dict(company_size=["S", "M", "L"]))

fig.update_layout( yaxis_title="Salários em Dólares" )


fig.show()

#CELL 9
# experience_level X exployment type

median_salaries = data.groupby('company_size')['salary_in_usd'].median().reset_index() # pega a mediana por ser um grupo bem disperso

print(median_salaries.head())

fig = px.histogram(median_salaries, x="company_size", y="salary_in_usd",
                   labels={
                      "salary_in_usd" : "Salários em Dólar",
                      "company_size" : "Tamanho da Empresa"
                   },
                   color="company_size",
                   category_orders=dict(company_size=["S", "M", "L"]))
fig.show()

#CELL 10
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#SERIE EN
series_aux = data.loc[(data['experience_level'] == "EN")]
serieEN = series_aux['employment_type'].value_counts()
serieEN = serieEN.to_frame()

fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=serieEN.index, values=serieEN['employment_type'], name="EN"), 1, 1)

#SERIE MI
series_aux = data.loc[(data['experience_level'] == "MI")]
serieMI = series_aux['employment_type'].value_counts()
serieMI = serieMI.to_frame()

fig.add_trace(go.Pie(labels=serieMI.index, values=serieMI['employment_type'], name="MI"), 1, 2)

#SERIE SE
series_aux = data.loc[(data['experience_level'] == "SE")]
serieSE = series_aux['employment_type'].value_counts()
serieSE = serieSE.to_frame()

fig.add_trace(go.Pie(labels=serieSE.index, values=serieSE['employment_type'], name="SE"), 1, 3)

#SERIE EX
series_aux = data.loc[(data['experience_level'] == "EX")]
serieEX = series_aux['employment_type'].value_counts()
serieEX = serieEX.to_frame()

fig.add_trace(go.Pie(labels=serieEX.index, values=serieEX['employment_type'], name="EX"), 1, 4)

fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="Nível de Experiência X Tipo de Emprego",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='EN', x=0.09, y=0.5, font_size=20, showarrow=False),
                 dict(text='MI', x=0.37, y=0.5, font_size=20, showarrow=False),
                 dict(text='SE', x=0.632, y=0.5, font_size=20, showarrow=False),
                 dict(text='EX', x=0.907, y=0.5, font_size=20, showarrow=False),
                 ])
fig.show()

#CELL 11
from ydata_profiling import ProfileReport

ProfileReport(data)