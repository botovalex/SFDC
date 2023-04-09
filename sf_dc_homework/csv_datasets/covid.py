import pandas as pd

covid_data = pd.read_csv('data/covid/covid_data.csv')
""" date — дата наблюдения;
    province/state — наименование провинции/штата;
    country — наименование страны;
    confirmed — общее число зафиксированных случаев на указанный день;
    deaths — общее число зафиксированных смертей на указанный день;
    recovered — общее число выздоровлений на указанный день."""
vaccinations_data = pd.read_csv('data/covid/country_vaccinations.csv')
vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations', 
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]
""" country — наименование страны;
    date — дата наблюдения;
    total_vaccinations — общее число введённых вакцин в стране на указанный день;
    people_vaccinated — общее число привитых первым компонентом в стране на указанный день;
    people_vaccinated_per_hundred — процент привитых первым компонентом в стране на указанный день (рассчитывается как );
    people_fully_vaccinated — общее число привитых вторым компонентом в стране на указанный день;
    people_fully_vaccinated_per_hundred — процент привитых вторым компонентом в стране на указанный день (рассчитывается как );
    daily_vaccination — ежедневная вакцинация (число вакцинированных в указанный день);
    vaccines — комбинации вакцин, используемые в стране."""

covid_data = covid_data.groupby(
    ['date','country'],
    as_index=False
)['confirmed','deaths','recovered'].sum()
covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']
covid_data = covid_data.sort_values(by=['country', 'date'])
covid_data['daily_confirmed'] = covid_data.groupby('country')['confirmed'].diff()
covid_data['daily_deaths'] = covid_data.groupby('country')['deaths'].diff()
covid_data['daily_recovered'] = covid_data.groupby('country')['recovered'].diff()

vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])

covid_df = covid_data.merge(vaccinations_data,how='left',on=['date','country'])
covid_df['death_rate'] = covid_df['deaths'] / covid_df['confirmed'] * 100
covid_df['recover_rate'] = covid_df['recovered'] / covid_df['confirmed'] * 100


# print(covid_df[covid_df['country'] == 'Russia'].groupby('country')['recover_rate'].mean())

# grouped_cases = covid_data.groupby('date')['daily_confirmed'].sum()
# grouped_cases.plot(
#     kind='line',
#     figsize=(12, 4),
#     title='Ежедневная заболеваемость по всем странам',
#     grid = True,
#     lw=3
# );

"""
#matplotlib

fig = plt.figure(figsize=(8, 4))
axes = fig.add_axes([0, 0, 1, 1])

us_data = covid_df[covid_df['country'] == 'United States']

fig = plt.figure(figsize=(8, 4))
axes = fig.add_axes([0, 0, 1, 1])
axes.scatter(
    x=us_data['people_fully_vaccinated'], 
    y=us_data['daily_confirmed'], 
    s=100,
    marker='o',
    c = 'blue'
);

vaccine_combinations = covid_df['vaccines'].value_counts()[:10]
fig = plt.figure(figsize=(5, 5))
axes = fig.add_axes([0, 0, 1, 1])
axes.pie(
    vaccine_combinations,
    labels=vaccine_combinations.index,
    autopct='%.1f%%',
    explode = [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
);


china_data = covid_df[covid_df['country'] == 'China']
china_grouped = china_data.groupby(['date'])[['confirmed', 'active', 'deaths', 'recovered']].sum()

#визуализация графиков
fig = plt.figure(figsize=(10, 4))
axes = fig.add_axes([0, 0, 1, 1])
axes.plot(china_grouped['confirmed'], label='Общее число зафиксированных случаев', lw=3)
axes.plot(china_grouped['deaths'], label='Общее число смертей', lw=3)
axes.plot(china_grouped['recovered'], label='Общее число выздоровевших пациентов', lw=3)
axes.plot(china_grouped['active'], label='Общее число активных случаев', lw=3, linestyle='dashed')

#установка параметров отображения
axes.set_title('Статистика Covid-19 в Китае', fontsize=16)
axes.set_xlabel('Даты')
axes.set_ylabel('Число случаев')
axes.set_yticks(range(0, 100000, 10000))
axes.xaxis.set_tick_params(rotation=30)
axes.grid()
axes.legend();
"""