import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 

df = pd.read_csv ('data.csv', encoding = 'windows-1251')

user_df = df[['tc', 'art_sp']] #создаю новый датафрейм с нужными колонками tc(id пользователя), art_sp(название бренда) 
user_df = user_df.rename(columns = {'tc':'user_id', 'art_sp':'brand_info'})#переименовываю колонки для удобства

user_df['brand_name'] = user_df.brand_info.apply(lambda x: x.split(' ')[-1])#достаю имена брендов из строк колонки "brand_info"

users_purchases = user_df.groupby('user_id', as_index = False)\
                        .agg({'brand_name': 'count'})\
                        .rename(columns = {'brand_name':'purchases'})\
                        .query('purchases >= 5') #пользователи, которые совершили 5 и более покупок

users_purchases.purchases.median()#медиана по количеству покупок для пользователей

lovely_brand_purchases_df = user_df.groupby(['user_id', 'brand_name'],as_index = False)\
                                    .agg({'brand_info': 'count'})\
                                    .sort_values(['user_id', 'brand_info'], ascending = [False, False])\
                                    .groupby('user_id')\
                                    .head(1)\
                                    .rename(columns = {'brand_name': 'lovely_brand_name', 'brand_info': 'lovely_brand_purchases'}) #количество покупок любимого бренда по каждому пользователю

users_unique_brands = user_df.groupby('user_id', as_index = False)\
                            .agg({'brand_name': pd.Series.nunique})\
                            .rename (columns = {'brand_name': 'unique_brands'})#число уникальных брендов для каждого пользователя
                            
loyalty_df = users_purchases\
    .merge(users_unique_brands, on = 'user_id')\
    .merge(lovely_brand_purchases_df, on = 'user_id')#объединяю 3 датафрейма в один 
    
loyalty_df['loyalty_score'] = loyalty_df.lovely_brand_purchases/loyalty_df.purchases #коэффициент лояльности пользователей к любимому бренду

# ax = sns.displot(loyalty_df.loyalty_score) #распределение коэффициента лояльности пользователей
# plt.show()

brands_loyalty = loyalty_df.groupby('lovely_brand_name', as_index = False)\
    .agg({'loyalty_score': 'median', 'user_id':'count'}) #количество лояльных пользователей по каждому бренду
    

# ax = sns.barplot(x="lovely_brand_name", y="user_id", data=brands_loyalty) #сравнение лояльности каждого бренда
# plt.show()

Brand_1_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_1"').sort_values('loyalty_score') #пользователи с коэффициентом лояльности более 0.8 для бренда Brand_1
Brand_1_loyal_users.to_csv('Brand_1_loyal_users', index = False) #сохраняю датафрейм в файл c расширением .csv

#делаю то же самое для остальных брендов

Brand_2_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_2"').sort_values('loyalty_score')
Brand_2_loyal_users.to_csv('Brand_2_loyal_users', index = False)

Brand_3_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_3"').sort_values('loyalty_score')
Brand_3_loyal_users.to_csv('Brand_3_loyal_users', index = False)

Brand_4_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_4"').sort_values('loyalty_score')
Brand_4_loyal_users.to_csv('Brand_4_loyal_users', index = False)

Brand_5_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_5"').sort_values('loyalty_score')
Brand_5_loyal_users.to_csv('Brand_5_loyal_users', index = False)

Brand_7_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Brand_7"').sort_values('loyalty_score')
Brand_7_loyal_users.to_csv('Brand_7_loyal_users', index = False)

Store_Brand_loyal_users = loyalty_df.query('loyalty_score > 0.8 and lovely_brand_name == "Store_Brand"').sort_values('loyalty_score')
Store_Brand_loyal_users.to_csv('Store_Brand_loyal_users', index = False)

