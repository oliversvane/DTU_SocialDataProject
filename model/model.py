import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def user_input_model(df,liste,scaler,model_xg):
    #Define input variables and target variable
    X,y=[      'Sewage connection', 
              'Water Connection',
              'Current use',
              'BBR Date of renovation', #When the house was rennovated
              'Heat Supply',
              'Material of roof',
              'Material of wall',
              'Kommune',
              'Year of construction', #Intervals of 10 years
              #'has_been_rennovated', All have been rennovated
              'Area of building [m^2]' #Area of house in square meteres
              ],['Energy Label']

    pred_df=df.sort_values(by=['Energy Label'])
    y=pred_df[y].values
    x=pred_df[X]
    x=pd.get_dummies(x)
    index_dict = dict(zip(x.columns,range(x.shape[1])))
    x=scaler.fit_transform(x)
    
    new_vector = np.zeros(len(index_dict))
    try:
        new_vector[index_dict[liste[0]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[1]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[2]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[3]]] = liste[3]
    except:
        pass
    try:
        new_vector[index_dict[liste[4]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[5]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[6]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[7]]] = 1
    except:
        pass
    try:
        new_vector[index_dict[liste[8]]] = liste[8]
    except:
        pass
    try:
        new_vector[index_dict[liste[9]]] = liste[9]
    except:
        pass
    new_vector = new_vector.reshape(1,-1)
    new_vector=scaler.transform(new_vector)
    Prediction = model_xg.predict(new_vector) ### Kald din gemte model her

    return Prediction