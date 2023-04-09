import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#создаём копию исходной таблицы
combine_data = sber_data.copy()

#отбрасываем столбцы с числом пропусков более 30% (100-70)
n = combine_data.shape[0] #число строк в таблице
thresh = n*0.7
combine_data = combine_data.dropna(how='any', thresh=thresh, axis=1)

#отбрасываем строки с числом пропусков более 2 в строке
m = combine_data.shape[1] #число признаков после удаления столбцов
combine_data = combine_data.dropna(how='any', thresh=m-2, axis=0)

#создаём словарь 'имя_столбца': число (признак), на который надо заменить пропуски 
values = {
    'life_sq': combine_data['full_sq'],
    'metro_min_walk': combine_data['metro_min_walk'].median(),
    'metro_km_walk': combine_data['metro_km_walk'].median(),
    'railroad_station_walk_km': combine_data['railroad_station_walk_km'].median(),
    'railroad_station_walk_min': combine_data['railroad_station_walk_min'].median(),
    'preschool_quota': combine_data['preschool_quota'].mode()[0],
    'school_quota': combine_data['school_quota'].mode()[0],
    'floor': combine_data['floor'].mode()[0]
}
#заполняем оставшиеся записи константами в соответствии со словарем values
combine_data = combine_data.fillna(values)
#выводим результирующую долю пропусков
display(combine_data.isnull().mean())



import pandas as pd
"""
Ваша задача очистить данную таблицу от пропусков следующим образом:
- Если признак имеет больше 50% пропущенных значений - удалите его
- Если в строке 3 и более пропусков - удалите строку
- Для оставшихся данных: числовые признаки заполните средним значением, а категориальные - модой
"""
df = pd.read_csv('./Root/data/test_data.csv')

# Если признак имеет больше 50% пропущенных значений - удалите его
df = df.dropna(how='any', thresh=df.shape[0]*0.5, axis=1)

# Если в строке 3 и более пропусков - удалите строку
df = df.dropna(how='any', thresh=df.shape[1]-2, axis=0)

# Для оставшихся данных: числовые признаки заполните средним значением, а категориальные - модой
df = df.fillna({
    'one':df['one'].mean(),
    'two':df['two'].mean(),
    'three':df['three'].mean(),
    'four':df['four'].mode()[0]
})

print(df)