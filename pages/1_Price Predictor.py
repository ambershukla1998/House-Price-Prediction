import streamlit as st
import pickle
import pandas as pd
import numpy as np
st.set_page_config(page_title="Price Predictor")
st.title('Price Predictor')
with open(r"D:\ml project\house price prediction\df.pkl", 'rb') as file:
    df = pickle.load(file)
with open(r"D:\ml project\house price prediction\pipeline.pkl", 'rb') as file:
    pipeline = pickle.load(file)

#st.dataframe(df)

property_type = st.selectbox('Property Type',['flat','House'])
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
bedrooms = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
built_up_area = float(st.number_input('Built Up Area'))
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# Predict button
if st.button('Predict'):
    # Form a DataFrame with user inputs and ensure column names match the pipeline
    one_df = pd.DataFrame({
        'property_type': [property_type],
        'sector': [sector],
        'bedRoom': [bedrooms],  # Fixed to match 'bedRoom' (uppercase 'B')
        'bathroom': [bathroom],
        'balcony': [balcony],
        'agePossession': [property_age],  # Ensure correct column name
        'built_up_area': [built_up_area],
        'servant room': [servant_room],  # Fixed column name
        'store room': [store_room],  # Fixed column name
        'furnishing_type': [furnishing_type],
        'luxury_category': [luxury_category],
        'floor_category': [floor_category],
    })

    #st.dataframe(one_df)

    # prediction
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22 * base_price  # 22% less than base price
    high = base_price + 0.22 * base_price  # 22% more than base price

    # Display result
    st.text(f"The price of the flat is between {round(low, 2)} Cr and {round(high, 2)} Cr")
