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

covid_df.to_csv('data/covid_df.csv')