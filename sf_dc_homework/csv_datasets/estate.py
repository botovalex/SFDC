from numpy import dtype, multiply
import pandas as pd
"""Данные представляют собой таблицу, в которой содержится 23 столбца:
index — номер строки
Suburb — наименование пригорода
Address — адрес
Rooms — количество комнат в помещении
Type — тип здания (h — дом, коттедж, вилла, терраса; u — блочный, дуплексный дом; t — таунхаус)
Price — цена помещения
Method — метод продажи 
SellerG — риэлторская компания
Date — дата продажи (в формате день/месяц/год)
Distance — расстояния до объекта от центра Мельбурна 
Postcode — почтовый индекс
Bedroom — количество спален
Bathroom — количество ванных комнат
Car — количество парковочных мест
Landsize — площадь прилегающей территории
BuildingArea — площадь здания
YearBuilt — год постройки
CouncilArea — региональное управление
Lattitude — географическая широта
Longitude — географическая долгота
Regionname — наименование района Мельбурна
Propertycount — количество объектов недвижимости в районе
Coordinates — широта и долгота, объединённые в кортеж
"""

melb_data = pd.read_csv('data/melb_data.csv', index_col=False)
# print(melb_data.loc[[3521, 1690], 'Landsize'])
# print(melb_data.head())
# print(melb_data.tail(7))
# print(melb_data.shape)

melb_data['Postcode'] = melb_data['Postcode'].astype('int64')
melb_data['Car'] = melb_data['Car'].astype('int64')
melb_data['Bedroom'] = melb_data['Bedroom'].astype('int64')
melb_data['Bathroom'] = melb_data['Bathroom'].astype('int64')
melb_data['Propertycount'] = melb_data['Propertycount'].astype('int64')
melb_data['YearBuilt'] = melb_data['YearBuilt'].astype('int64')

# print(melb_data.describe(include='object'))
# print(melb_data['Type'].value_counts(normalize=True))
# print(melb_data['Regionname'].mode())

# print(melb_data.loc[:,'BuildingArea'])
# print(melb_data['BuildingArea'].mean())

# area_median = melb_data['BuildingArea'].median()
# area_mean = melb_data['BuildingArea'].mean()
# print(abs(area_median - area_mean) / area_mean)

# print(melb_data[(melb_data['SellerG'] == 'Nelson') & (melb_data['Price'] > 3000000)].shape[0])
# print(melb_data[melb_data['BuildingArea'] == 0]['Price'].min())
# print(melb_data[(melb_data['Price']<1000000) & ((melb_data['YearBuilt'] > 2015) | (melb_data['Rooms'] > 5))]['Price'].mean())
# print(melb_data[(melb_data['Price'] < 3000000) & (melb_data['Type'] == 'h')]['Regionname'].mode())

melb_df = melb_data.copy()
melb_df.drop(['index', 'Coordinates'], axis=1, inplace=True)
total_rooms = melb_df['Rooms'] + melb_df['Bedroom'] + melb_df['Bathroom']
melb_df['MeanRoomsSquare'] = melb_df['BuildingArea'] / total_rooms
melb_df['Date'] = pd.to_datetime(melb_df['Date'])

#коэффициент соотношения площади здания (BuildingArea) и площади участка (Landsize)
diff_area = melb_df['BuildingArea'] - melb_df['Landsize']
sum_area = melb_df['BuildingArea'] + melb_df['Landsize']
melb_df['AreaRatio'] = diff_area/sum_area
# print(melb_df['AreaRatio'])

#Для того чтобы преобразовывать столбцы с датами, записанными в распространённых форматах, 
# в формат datetime, можно воспользоваться функцией pandas.to_datetime().
melb_df['Date'] = pd.to_datetime(melb_df['Date'])
# print(melb_df['Date'])

#обратившись по атрибуту dt.year в столбце Date, мы можем «достать» год продажи и понять, 
# за какой интервал времени (в годах) у нас представлены данные, а также на какой год приходится наибольшее число продаж:
# years_sold = melb_df['Date'].dt.year
# print(years_sold)
# print('Min year sold:', years_sold.min())
# print('Max year sold:', years_sold.max())
# print('Mode year sold:', years_sold.mode()[0])

#на какие месяцы приходится пик продаж объектов недвижимости
melb_df['MonthSale'] = melb_df['Date'].dt.month
melb_df['MonthSale'].value_counts(normalize=True)

#Дколько дней прошло с 1 января 2016 года до момента продажи объекта
# delta_days = melb_df['Date'] - pd.to_datetime('2016-01-01') 
# print(delta_days)
melb_df['AgeBuilding'] = melb_df['Date'].dt.year - melb_df['YearBuilt']
melb_df = melb_df.drop('YearBuilt', axis=1)

example = pd.to_datetime('2021-12-25 15:35:45')
melb_df['WeekdaySale'] = melb_df['Date'].dt.dayofweek

# weekend_count = melb_df[(melb_df['WeekdaySale'] == 5) | (melb_df['WeekdaySale'] == 6)]['WeekdaySale'].count()
# print(weekend_count)

def get_street_type(address):
    exclude_list = ['N', 'S', 'W', 'E']
    address_list = address.split(' ')
    street_type = address_list[-1]
    if street_type in exclude_list:
        street_type = address_list[-2]
    return street_type


# применить функцию к столбцу, возвращается Series
street_types = melb_df['Address'].apply(get_street_type)

popular_stypes = street_types.value_counts().nlargest(10).index
melb_df['StreetType'] = street_types.apply(lambda x: x if x in popular_stypes else 'other')

melb_df = melb_df.drop('Address', axis=1)

def get_weekend(weekday):
    if weekday == 5 or weekday == 6:
        return 1
    return 0

melb_df['Weekend'] = melb_df['WeekdaySale'].apply(get_weekend)
# print(round(melb_df[melb_df['Weekend'] == 1]['Price'].mean(),2))

popular_seller = melb_df['SellerG'].value_counts().nlargest(49)
melb_df['SellerG'] = melb_df['SellerG'].apply(lambda x: x if x in popular_seller else 'other')
# print(melb_df[melb_df['SellerG'] == 'Nelson']['Price'].min())
# print(melb_df[melb_df['SellerG'] == 'other']['Price'].min())
# print(melb_df[melb_df['SellerG'] == 'Nelson']['Price'].min()
#       / melb_df[melb_df['SellerG'] == 'other']['Price'].min())

unique_list = []

for col in melb_df.columns:
    item = (col, melb_df[col].nunique(), melb_df[col].dtype)
    unique_list.append(item)
    
unique_counts = pd.DataFrame(
    unique_list,
    columns=['Column_Name', 'Num_Unique', 'Type']
).sort_values(by='Num_Unique', ignore_index=True)

# преобразуем столбцы в category
cols_to_exclude = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car'] 
max_unique_count = 150
for col in melb_df.columns:
    if melb_df[col].nunique() < max_unique_count and col not in cols_to_exclude:
        melb_df[col] = melb_df[col].astype('category')

melb_df['Type'] = melb_df['Type'].cat.rename_categories({
    'u': 'unit',
    't': 'townhouse',
    'h': 'house'
})

popular_suburb = melb_df['Suburb'].value_counts().nlargest(119)
melb_df['Suburb'] = melb_df['Suburb'].apply(lambda x : x if x in popular_suburb else 'other').astype('category')

# print(melb_df['Date'].dt.quarter.value_counts())

# print(melb_df.sort_values(by='Date', ascending=False))

#вывести несколько столбцов, каждую 10 строку
# print(melb_df.sort_values(by=['Distance', 'Price']).loc[::10, ['Distance', 'Price']])

# mask1 = melb_df['AreaRatio'] < -0.8
# mask2 = melb_df['Type'] == 'townhouse'
# mask3 = melb_df['SellerG'] == 'McGrath'
# print(melb_df[mask1 & mask2 & mask3].sort_values(
#     by=['Date', 'AreaRatio'],
#     ascending=[True, False],
#     ignore_index=True
# ).loc[:, ['Date', 'AreaRatio']])

melb_df[(melb_df['Type'] == 'townhouse') & (melb_df['Rooms'] > 2)].sort_values(
    by=['Rooms', 'MeanRoomsSquare'], 
    ascending=[True, False], 
    ignore_index=True
).loc[18, 'Price']

# print(melb_df['Rooms'].describe())


# print(melb_df.groupby('Type').mean())
# print(melb_df.groupby('Regionname')['Distance'].min().sort_values(ascending=False))
# print(melb_df.groupby('MonthSale')['Price'].agg(
#     ['count', 'mean', 'max']
# ).sort_values(by='count', ascending=False))
# print(melb_df.groupby('MonthSale')['Price'].agg('describe'))
# print(melb_df.groupby('Regionname')['SellerG'].agg(
#     		['nunique', set]
# ).sort_values(by='nunique', ascending=False))

# print(melb_df.groupby('Regionname')['Lattitude'].std().sort_values())
# print(melb_df[(melb_df['Date']>='2017-05-01') & (melb_df['Date']<='2017-09-01')].groupby('SellerG')['Price'].sum().sort_values())
# print(melb_df.groupby(['Rooms', 'Type'])['Price'].mean().unstack())
# print(melb_df.pivot_table(
#     values='Price',
#     index='Rooms',
#     columns='Type',
#      fill_value = 0
# ).round(2))
# print(melb_df.pivot_table(
#     values='Price',
#     index='Regionname',
#     columns='Weekend',
#     aggfunc='count',
# ))
# print(melb_df.pivot_table(
#     values='Landsize',
#     index='Regionname',
#     columns='Type',
#     aggfunc=['median', 'mean'],
#     fill_value=0
# ).round(2))
# print(melb_df.pivot_table(
#     values='Price',
#     index=['Method','Type'],
#     columns='Regionname',
#     aggfunc='median',
#     fill_value=0
# # # ))
# pivot = melb_df.pivot_table(
#     values='Landsize',
#     index='Regionname',
#     columns='Type',
#     aggfunc=['median', 'mean'],
#     fill_value=0
# )
# print(pivot)
# mask = pivot['mean']['house'] < pivot['median']['house']
# filtered_pivot = pivot[mask]
# print(filtered_pivot)
# print(list(filtered_pivot.index))

ex_pivot = melb_df.pivot_table(
    values='Price',
    index='SellerG',
    columns='Type',
    aggfunc='mean'
)
print(ex_pivot[ex_pivot['unit'] == ex_pivot['unit'].max()])