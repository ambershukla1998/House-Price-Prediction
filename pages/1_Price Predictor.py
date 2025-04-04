# import streamlit as st
# import pickle
# import pandas as pd
# import numpy as np
# import os
# import gdown
#
# st.set_page_config(page_title="Price Predictor")
# st.title('Price Predictor')
#
# # Google Drive URL for pipeline.pkl
# pipeline_url = "https://drive.google.com/uc?export=download&id=1jqINDDVjQJNTxLog5_I60UHYQeo1F9LN"
#
# # Load df.pkl using relative path or fallback to absolute path
# try:
#     # Try loading df.pkl from the parent directory
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     parent_dir = os.path.dirname(current_dir)
#     with open(os.path.join(parent_dir, "df.pkl"), 'rb') as file:
#         df = pickle.load(file)
#     #st.write("df.pkl loaded from the relative path.")
# except FileNotFoundError:
#     # Fallback to absolute path
#     try:
#         with open(r"D:\ml project\house price prediction\df.pkl", 'rb') as file:
#             df = pickle.load(file)
#         #st.write("df.pkl loaded from the absolute path.")
#     except FileNotFoundError:
#         st.error("The file df.pkl could not be found. Please ensure it is uploaded.")
#         raise
#
# # Download pipeline.pkl from Google Drive if not already present
# if not os.path.exists("pipeline.pkl"):
#     gdown.download(pipeline_url, "pipeline.pkl", quiet=False)
#
# # Load pipeline.pkl
# with open("pipeline.pkl", "rb") as file:
#     pipeline = pickle.load(file)
#
#
# # UI Elements
# property_type = st.selectbox('Property Type', ['flat', 'house'])
# sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
# bedrooms = st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()))
# bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
# balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
# property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
# built_up_area = float(st.number_input('Built Up Area', min_value=1.0))
# servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
# store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
# furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
# luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
# floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))
#
# # Predict button
# if st.button('Predict'):
#     try:
#         # Prepare input data
#         one_df = pd.DataFrame({
#             'property_type': [property_type],
#             'sector': [sector],
#             'bedRoom': [bedrooms],
#             'bathroom': [bathroom],
#             'balcony': [balcony],
#             'agePossession': [property_age],
#             'built_up_area': [built_up_area],
#             'servant room': [servant_room],
#             'store room': [store_room],
#             'furnishing_type': [furnishing_type],
#             'luxury_category': [luxury_category],
#             'floor_category': [floor_category],
#         })
#
#         # Make prediction
#         base_price = np.expm1(pipeline.predict(one_df))[0]
#         low = base_price - 0.22 * base_price
#         high = base_price + 0.22 * base_price
#         st.text(f"The price of the flat is between {round(low, 2)} Cr and {round(high, 2)} Cr")
#     except Exception as e:
#         st.error(f"An error occurred during prediction: {e}")

# import streamlit as st
# import pickle
# import pandas as pd
# import numpy as np
# import os
# import gdown
#
# # Page config
# st.set_page_config(page_title="🏠 Real Estate Price Predictor", layout="centered")
# st.title("💰 House Price Estimator")
# st.subheader("Find out how much your dream property is worth in just a few clicks!")
#
# # Google Drive link to download pipeline
# pipeline_url = "https://drive.google.com/uc?export=download&id=1jqINDDVjQJNTxLog5_I60UHYQeo1F9LN"
#
# # Load DataFrame
# try:
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     parent_dir = os.path.dirname(current_dir)
#     with open(os.path.join(parent_dir, "df.pkl"), 'rb') as file:
#         df = pickle.load(file)
# except FileNotFoundError:
#     try:
#         with open(r"D:\ml project\house price prediction\df.pkl", 'rb') as file:
#             df = pickle.load(file)
#     except FileNotFoundError:
#         st.error("⚠️ The file `df.pkl` could not be found. Please ensure it's uploaded correctly.")
#         raise
#
# # Download pipeline.pkl if not present
# if not os.path.exists("pipeline.pkl"):
#     st.info("⏳ Downloading ML model... Please wait.")
#     gdown.download(pipeline_url, "pipeline.pkl", quiet=False)
#
# # Load ML model
# with open("pipeline.pkl", "rb") as file:
#     pipeline = pickle.load(file)
#
# # User Inputs
# st.markdown("### 🏗️ Enter Property Details Below")
#
# col1, col2 = st.columns(2)
#
# with col1:
#     property_type = st.selectbox('🏘️ Property Type', ['flat', 'house'])
#     sector = st.selectbox('📍 Sector', sorted(df['sector'].unique()))
#     bedrooms = st.selectbox('🛏️ Bedrooms', sorted(df['bedRoom'].unique()))
#     bathroom = float(st.selectbox('🚿 Bathrooms', sorted(df['bathroom'].unique())))
#     balcony = st.selectbox('🌅 Balconies', sorted(df['balcony'].unique()))
#     property_age = st.selectbox('⏳ Property Age', sorted(df['agePossession'].unique()))
#
# with col2:
#     built_up_area = float(st.number_input('📐 Built-Up Area (in sq. ft.)', min_value=1.0))
#     servant_room = float(st.selectbox('🧹 Servant Room', [0.0, 1.0]))
#     store_room = float(st.selectbox('📦 Store Room', [0.0, 1.0]))
#     furnishing_type = st.selectbox('🛋️ Furnishing Type', sorted(df['furnishing_type'].unique()))
#     luxury_category = st.selectbox('💎 Luxury Category', sorted(df['luxury_category'].unique()))
#     floor_category = st.selectbox('🏢 Floor Category', sorted(df['floor_category'].unique()))
#
# # Prediction Logic
# if st.button('🔮 Predict Price'):
#     try:
#         input_data = pd.DataFrame({
#             'property_type': [property_type],
#             'sector': [sector],
#             'bedRoom': [bedrooms],
#             'bathroom': [bathroom],
#             'balcony': [balcony],
#             'agePossession': [property_age],
#             'built_up_area': [built_up_area],
#             'servant room': [servant_room],
#             'store room': [store_room],
#             'furnishing_type': [furnishing_type],
#             'luxury_category': [luxury_category],
#             'floor_category': [floor_category],
#         })
#
#         prediction = pipeline.predict(input_data)
#         base_price = np.expm1(prediction[0])
#         lower_bound = round(base_price * 0.78, 2)
#         upper_bound = round(base_price * 1.22, 2)
#
#         st.success(f"🏷️ Estimated Price Range: ₹ {lower_bound} Cr – ₹ {upper_bound} Cr")
#     except Exception as e:
#         st.error(f"❌ Oops! Something went wrong: {e}")

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import gdown

# Page config
st.set_page_config(page_title="🏠 Real Estate Price Predictor", layout="centered")
st.title("💰 House Price Estimator")
st.subheader("Find out how much your dream property is worth in just a few clicks!")

# Google Drive link to download pipeline
pipeline_url = "https://drive.google.com/uc?export=download&id=1jqINDDVjQJNTxLog5_I60UHYQeo1F9LN"

# Load DataFrame
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    with open(os.path.join(parent_dir, "df.pkl"), 'rb') as file:
        df = pickle.load(file)
except FileNotFoundError:
    try:
        with open(r"D:\ml project\house price prediction\df.pkl", 'rb') as file:
            df = pickle.load(file)
    except FileNotFoundError:
        st.error("⚠️ The file `df.pkl` could not be found. Please ensure it's uploaded correctly.")
        raise

# Download pipeline.pkl if not present
if not os.path.exists("pipeline.pkl"):
    st.info("⏳ Downloading ML model... Please wait.")
    gdown.download(pipeline_url, "pipeline.pkl", quiet=False)

# Load ML model
with open("pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# User Inputs
st.markdown("### 🏗️ Enter Property Details Below")

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox('🏘️ Property Type', ['flat', 'house'])
    sector = st.selectbox('📍 Sector', sorted(df['sector'].unique()))
    bedrooms = st.selectbox('🛏️ Bedrooms', sorted(df['bedRoom'].unique()))
    bathroom = float(st.selectbox('🚿 Bathrooms', sorted(df['bathroom'].unique())))
    balcony = st.selectbox('🌅 Balconies', sorted(df['balcony'].unique()))
    property_age = st.selectbox('⏳ Property Age', sorted(df['agePossession'].unique()))

with col2:
    built_up_area = float(st.number_input('📐 Built-Up Area (in sq. ft.)', min_value=1.0))
    servant_room = float(st.selectbox('🧹 Servant Room', [0.0, 1.0]))
    store_room = float(st.selectbox('📦 Store Room', [0.0, 1.0]))
    furnishing_type = st.selectbox('🛋️ Furnishing Type', sorted(df['furnishing_type'].unique()))
    luxury_category = st.selectbox('💎 Luxury Category', sorted(df['luxury_category'].unique()))
    floor_category = st.selectbox('🏢 Floor Category', sorted(df['floor_category'].unique()))

# Prediction Logic
if st.button('🔮 Predict Price'):
    try:
        input_data = pd.DataFrame({
            'property_type': [property_type],
            'sector': [sector],
            'bedRoom': [bedrooms],
            'bathroom': [bathroom],
            'balcony': [balcony],
            'agePossession': [property_age],
            'built_up_area': [built_up_area],
            'servant room': [servant_room],
            'store room': [store_room],
            'furnishing_type': [furnishing_type],
            'luxury_category': [luxury_category],
            'floor_category': [floor_category],
        })

        prediction = pipeline.predict(input_data)
        base_price = np.expm1(prediction[0])
        lower_bound = round(base_price * 0.78, 2)
        upper_bound = round(base_price * 1.22, 2)

        st.success(f"🏷️ Estimated Price Range: ₹ {lower_bound} Cr – ₹ {upper_bound} Cr")

        # Prepare result DataFrame
        result_df = input_data.copy()
        result_df["Estimated Base Price (₹ Cr)"] = round(base_price, 2)
        result_df["Estimated Lower Price (₹ Cr)"] = lower_bound
        result_df["Estimated Upper Price (₹ Cr)"] = upper_bound

        # Show the result in Streamlit
        st.markdown("### 📊 Prediction Summary")
        st.dataframe(result_df)

        # CSV Download
        csv_data = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name='house_price_prediction.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"❌ Oops! Something went wrong: {e}")

