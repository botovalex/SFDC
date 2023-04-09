from numpy import int64
import pandas as pd
import re

from pandas.core.reshape.pivot import pivot_table 

ratings1 = pd.read_csv('data/movies_data/ratings1.csv')
ratings2 = pd.read_csv('data/movies_data/ratings2.csv')
""" userId — уникальный идентификатор пользователя, который выставил оценку;
    movieId — уникальный идентификатор фильма;
    rating — рейтинг фильма."""
    
dates = pd.read_csv('data/movies_data/dates.csv')
""" date — дата и время выставления оценки фильму."""
dates['date'] = pd.to_datetime(dates['date'])

movies = pd.read_csv('data/movies_data/movies.csv')
""" movieId — уникальный идентификатор фильма;
    title — название фильма и год его выхода;
    genres — жанры фильма."""
    
ratings_movies = pd.read_csv('data/movies_data/ratings_movies.csv')

    
ratings = pd.concat(
    [ratings1, ratings2],
    ignore_index=True
)
ratings.drop_duplicates(ignore_index=True, inplace=True)

df = pd.DataFrame()

# path = ['users2.csv', 'users1.csv', 'users3.csv']
# path = list(map(lambda s : pd.read_csv('users/' + s, sorted(path))))
# result_df = pd.concat(path, ignore_index=True)
# result_df.drop_duplicates(ignore_index=True, inplace=True)

ratings_dates = pd.concat([ratings, dates], axis=1)

# print(df)
# df_e = pd.concat([df, ratings])
# print(df_e)

merged = ratings_dates.merge(
    movies,
    on='movieId',
    how='left'
)
# print(merged.head())


def get_year_release(arg):
    #находим все слова по шаблону "(DDDD)"
    candidates = re.findall(r'\(\d{4}\)', arg) 
    # проверяем число вхождений
    if len(candidates) > 0:
        #если число вхождений больше 0,
	#очищаем строку от знаков "(" и ")"
        year = candidates[0].replace('(', '')
        year = year.replace(')', '')
        return int(year)
    else:
        #если год не указан, возвращаем None
        return None
    

ratings_movies['year_release'] = ratings_movies['title'].apply(get_year_release)
"""'Unnamed: 0', 'userId', 'movieId', 'rating', 'date', 'title', 'genres','year_release'"""
mask_year = ratings_movies['year_release'] == 2018
mask_rating_min = ratings_movies['rating'] == ratings_movies['rating'].min()
# print(ratings_movies[mask1].groupby(by='title')['rating'].mean().sort_values())
# print(ratings_movies[mask_year].groupby(by='genres')['rating'].mean().sort_values())


# print(ratings_movies.groupby('userId')['genres'].nunique().sort_values(ascending=False))
# print(ratings_movies.groupby('userId')['rating'].agg(['count','mean']).sort_values(by=['count','mean'], ascending=[True, False]))
# print(ratings_movies[mask_year].groupby('genres')['rating'].agg(['count','mean']))
ratings_movies['date'] = pd.to_datetime(ratings_movies['date'])
ratings_movies['year_rating'] = ratings_movies['date'].dt.year
pivot_year_rating = pivot_table(
    ratings_movies,
    values='rating',
    index='year_rating',
    columns='genres'
)
# mask_pivot = pivot_year_rating['Comedy'] == 5
print(pivot_year_rating['Comedy'].sort_values(ascending=False))
# print(pivot_year_rating['Action|Adventure|Animation|Children|Comedy|IMAX'].sort_values())