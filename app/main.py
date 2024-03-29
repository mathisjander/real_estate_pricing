# create a streamlit app for the model
# run with: streamlit run main.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
import shap
import os
import matplotlib.pyplot as plt


def main():

    # Get the absolute path of the directory containing main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the .pkl file
    model_path = os.path.join(current_dir, 'real_estate_model.pkl')

 
    # load the model
    model = pickle.load(open(model_path, 'rb'))

    # Construct the absolute path of the .pkl file
    scaler_path = os.path.join(current_dir, 'input_scaler.pkl')

    # load the scaler
    scaler = pickle.load(open(scaler_path, 'rb'))

    # create input widgets in streamlit app for model inputs

    st.title('Real Estate Price Predictor')
    st.text('Disclaimer: This app is a study project and the predictions returned should be not \ntaken at face value. \nThe model was trained on real estate listings in Berlin (Germany) during April 2023.')
    st.text('Please enter the following information to get a price estimate for your apartment.')
    
    
    area = st.number_input('Area in square meters', min_value=0, max_value=5000, value=50, step=1)
    rooms = st.number_input('Number of rooms', min_value=0, max_value=100, value=1, step=1)
    zip = st.number_input('ZIP code ', min_value=0, max_value=1000000, value=0, step=1)
    year = st.number_input('Year of construction', min_value=1800, max_value=2023, value=2000, step=1)
    level = st.number_input('Floor level', min_value=0, max_value=250, value=0, step=1)

    # create a dataframe with the input values 
    input_df = pd.DataFrame({'area': [area], 'rooms': [rooms], 'zipcode': [zip], 'construction_year': [year], 'level': [level]})

    # predict based on input values and scaler
    prediction = model.predict(scaler.transform(input_df))[0]

    # return prediction
    st.text('The estimated price for your home is: ' + str(round(prediction)) + '€')

    # add shap values to explain prediction
    st.text('The following features contributed to the prediction:')

    # Construct the absolute path of the .pkl file
    explainler_path = os.path.join(current_dir, 'explainer.pkl')
    explainer = pickle.load(open(explainler_path, 'rb'))

    shap_values = explainer.shap_values(scaler.transform(input_df))
    

    # Create the force plot
    fig = shap.force_plot(
        base_value=explainer.expected_value,
        shap_values=shap_values[0],
        features=input_df.iloc[0,:],
        feature_names=input_df.columns,
        matplotlib=True,
        show=False
    )
    st.pyplot(fig)
        

if __name__ == '__main__':
    main()
