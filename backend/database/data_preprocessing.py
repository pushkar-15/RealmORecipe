import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

"""
Desription:
    this file just contains the rough scripts used for preprocessing the dataset
    it does not run with rest of the program
    dataset taken from https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions

Files:
    this script assumes that you have these files in your /database folder
    RAW_recipes.csv
    RAW_interactions.csv

"""

df = pd.read_csv('RAW_recipes.csv')

# splitting nutrition values into separate coloumns, for filtering based on calorie 
df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']] = df.nutrition.str.split(",",expand=True) 
df['calories'] =  df['calories'].apply(lambda x: x.replace('[','')) 
df['carbohydrates (PDV)'] =  df['carbohydrates (PDV)'].apply(lambda x: x.replace(']','')) 
df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']] = df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']].astype('float')

# for making food types
df['food types'] = np.nan
df['food types'] = df['food types'].astype('str')

# classification of veg and non-veg dessert
for i in df['ingredients'].index:
    if('eggs' not in df['ingredients'][i] or 'egg' in df['ingredients'][i]):
         if('ice-cream' in df['ingredients'][i] or 'chocolate' in df['ingredients'][i] or 'cookies' in df['ingredients'][i] or 'sugar' in df['ingredients'][i]):
                df['food types'][i]='Veg dessert'
    elif('eggs' in df['ingredients'][i] or 'egg' in df['ingredients'][i]):
        if('ice-cream' in df['ingredients'][i] or 'chocolate' in df['ingredients'][i] or 'cookies' in df['ingredients'][i] or 'sugar' in df['ingredients'][i]):
                df['food types'][i]='Non-Veg dessert'

# assuming healthy > 300 calories
for i in df.index:
    if(df['food types'][i]!='Veg dessert' and df['food types'][i]!='Non-Veg dessert' and 20<df['calories'][i]<300):
        df['food types'][i]='Healthy'

# classifying as non-veg food
for i in df.index:
    if(df['food types'][i]!='Veg dessert' and df['food types'][i]!='Non-Veg dessert' and df['food types'][i]!='Healthy'):
        if('chicken' in df['ingredients'][i] or 'eggs' in df['ingredients'][i] or'ham' in df['ingredients'][i] or 'pepperoni' in df['ingredients'][i]  or'ground beef'  in df['ingredients'][i]  or 'ground lamb' in df['ingredients'][i]  or 'lamb chops' in df['ingredients'][i]  or'bacon' in df['ingredients'][i]  or'egg' in df['ingredients'][i]  or 'pork chops' in df['ingredients'][i]  or 'beef' in df['ingredients'][i]  ):
            df['food types'][i]='Non-veg'

# classifying as veg food
for i in df.index:
    if(df['food types'][i]!='Veg dessert' and df['food types'][i]!='Non-Veg dessert' and df['food types'][i]!='Healthy' and df['food types'][i]!='Non-veg'):
        df['food types'][i]='Veg'

"""
    User Interactions Data
""" 

# Taking dataset of ratings and reviews and adding to main
df2=pd.read_csv('RAW_interactions.csv')

df2=df2.drop(['user_id','date','review'],axis=1)

df3=df2.groupby(['recipe_id'])['rating'].agg(['mean','count'])
df3.reset_index(inplace=True)

df3.rename(columns={'mean':'average_rating','count':'votes'},inplace=True)

food_df = pd.merge(df, df3, left_on='id',right_on='recipe_id')

metadata=food_df

C = metadata['average_rating'].mean()   # avg rating
print(C)

m = metadata['votes'].quantile(0.75)    # the minimum number of votes required to be in the chart
print(m)

# filtering by dropping out all unqualified recipes
scored_recipes = metadata.copy().loc[metadata['votes'] >= m]

def weighted_score(x, m=m, C=C):
    v = x['votes']
    R = x['average_rating']
    # Calculation formula weighted average
    return (v/(v+m) * R) + (m/(m+v) * C)

scored_recipes['score'] = scored_recipes.apply(weighted_score, axis=1)
scored_recipes = scored_recipes.sort_values('score', ascending=False)

metadata['score'] = metadata.apply(weighted_score, axis=1)

# removing data with 0, 1, 2, 3 votes to check file sizes and remove junk recipes

df = metadata
print(df.shape[0])

df = df[df.votes != 0]
print(df.shape[0])

df = df[df.votes != 1]
print(df.shape[0])

df = df[df.votes != 2]
print(df.shape[0])

df = df[df.votes != 3]
print(df.shape[0])


df=df.drop(['id','contributor_id','recipe_id','calories','total fat (PDV)','sugar (PDV)','sodium (PDV)','protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)'],axis=1)
df.to_csv('recipeData.csv')

final_df = pd.read_csv('recipeData.csv')