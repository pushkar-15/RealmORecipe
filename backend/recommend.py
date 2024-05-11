import pandas as pd
from pathlib import Path

"""

    Description:
        This file defines a function for recommendation from database according to input.

    Functions:
        filter_database([array])

"""


database_file = Path.cwd() / "database" / "recipeData.csv"          # for getting path in docker

df = pd.read_csv(database_file)     # Main data frame


def filter_database(userData):
    """

    Description:
        This function filters dataset according to input and gives recommendation in (dict) format for easy jsonify.
      
    Parameters:
        userData (array): The user input data recived from app.py.
    
    Returns:
        df_final (dict): Recipe recommendation.

    Used by:
        Only called by app.py.

    Requires:
        Main database in recipeData.csv file in /database folder.

    """

    df_filtered = df

    # Filter data by type of food
    match userData[0]:
        case 'Healthy':
            th = df['food types'].isin(['Healthy'])
            df_filtered = df[th]
        case 'Veg':
            tv = df['food types'].isin(['Veg'])
            df_filtered = df[tv]
        case 'Non-Veg':
            tnv = df['food types'].isin(['Non-veg'])
            df_filtered = df[tnv]
        case 'Veg_Dessert':
            tdv = df['food types'].isin(['Veg dessert'])
            df_filtered = df[tdv]
        case 'Non-Veg_Dessert':
            tdnv = df['food types'].isin(['Non-Veg dessert'])
            df_filtered = df[tdnv]



    # if unfilled data, set no filter
    if (userData[1] == '' or int(userData[1]) < 0) : userData[1] = '999'
    if (userData[2] == '' or int(userData[2]) < 0) : userData[2] = '99'
    if (userData[3] == '' or int(userData[3]) < 0) : userData[3] = '99'

    # coverting to int for range
    userData[1] = int(userData[1])
    userData[2] = int(userData[2])
    userData[3] = int(userData[3])

    # incrementing by 1 for proper range()
    userData[1]+=1
    userData[2]+=1
    userData[3]+=1

    # Filtering data by time (in minutes) in range (userInput-10,userInput) required to prepare
    m = df_filtered['minutes'].isin(range(max(userData[1]-10,0), userData[1])) 
    df_filtered = df_filtered[m]

    # Filtering data by number of steps in range (userInput-5,userInput) required to prepare
    s = df_filtered['n_steps'].isin(range(max(userData[2]-5,0), userData[2]))
    df_filtered = df_filtered[s]

    # Filtering data by number of ingredients in range (userInput-5,userInput) required to prepare
    i = df_filtered['n_ingredients'].isin(range(max(userData[3]-5,0), userData[3])) 
    df_filtered = df_filtered[i]                                    # final filtered data frame 



    # Sorting data by score which is based on average rating and number of votes 
    df_sorted = df_filtered.sort_values('score',ascending = False).head(2000)         # Taking highest scored 2000 recipes  

    # Error handling if df is empty
    if df_sorted.empty:
        return {'error' : 1}

    # Taking a random recipe from top sorted, to prevent same recommendation
    df_final = df_sorted.sample(1)

    # Converting to dict with orient for easy data access in frontend
    df_final = df_final.to_dict(orient='list')

    # Return the final result
    return df_final

