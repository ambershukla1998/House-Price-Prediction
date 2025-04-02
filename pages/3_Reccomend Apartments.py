import pickle
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

st.set_page_config(page_title="Interactive Apartment Recommendations")

# Define the datasets directory (relative path)
DATASET_DIR = os.path.join(os.path.dirname(__file__), "datasets")

# Print the current working directory
st.write(f"Current working directory: {os.getcwd()}")

# Check and print the datasets directory path
st.write(f"Datasets directory path: {DATASET_DIR}")

# List all files in the datasets directory to see if the file exists
def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        st.write(f"Files in datasets directory: {files}")
    except Exception as e:
        st.write(f"Error accessing datasets directory: {e}")

list_files_in_directory(DATASET_DIR)

# Define a helper function to load a file
def load_file(filename):
    file_path = os.path.join(DATASET_DIR, filename)
    try:
        with open(file_path, 'rb') as file:
            st.write(f"Successfully loaded {filename}")
            return pickle.load(file)
    except FileNotFoundError:
        st.write(f"Error loading {filename}: File not found at {file_path}")
        return None
    except pickle.UnpicklingError:
        st.write(f"Error unpickling '{filename}'. The file may be corrupted.")
        return None

# Load the datasets
location_df = load_file("location_distance.pkl")
cosine_sim1 = load_file("cosine_sim1.pkl")
cosine_sim2 = load_file("cosine_sim2.pkl")
cosine_sim3 = load_file("cosine_sim3.pkl")

# Construct the CSV file path and print it
csv_path = os.path.join(DATASET_DIR, "data_viz1.csv")
st.write(f"CSV file path: {csv_path}")

# Try loading the CSV file
try:
    df1 = pd.read_csv(csv_path)
    st.write("CSV file loaded successfully!")
except FileNotFoundError:
    st.write("CSV file not found at the specified path.")
except Exception as e:
    st.write(f"Error loading CSV file: {e}")

# Function to recommend properties with scores
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 3 * cosine_sim1 + 5 * cosine_sim2 + 6 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    return recommendations_df

# Initialize session state variables
if 'filtered_apartments' not in st.session_state:
    st.session_state['filtered_apartments'] = []
if 'selected_apartment' not in st.session_state:
    st.session_state['selected_apartment'] = None

# Location and Radius selection
st.title('Select Location and Radius')
if location_df is not None:
    location_options = sorted(location_df.columns.to_list())
    selected_location = st.selectbox('Location', location_options)
    radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)

    if st.button('Search'):
        filtered_locations = location_df[location_df[selected_location] < (radius * 1000)][selected_location].sort_values()
        if not filtered_locations.empty:
            st.session_state['filtered_apartments'] = filtered_locations.index.to_list()
            st.write(f"Locations within {radius} km from {selected_location}:")
            for key, value in filtered_locations.items():
                st.text(f"{key}: {round(value / 1000, 2)} kms")
        else:
            st.write("No locations found within the specified radius.")
            st.session_state['filtered_apartments'] = []

    # Apartment Recommendation
    st.title('Apartment Recommendation')

    # Display the filtered apartments from the search
    if st.session_state['filtered_apartments']:
        apartment_options = st.session_state['filtered_apartments']
    else:
        apartment_options = location_df.index.to_list()

    selected_apartment = st.selectbox('Select an apartment', apartment_options, key='apartment_selection')
    st.session_state['selected_apartment'] = selected_apartment

    if st.button('Recommend', key='recommend_button'):
        if st.session_state['selected_apartment']:
            recommendation_df = recommend_properties_with_scores(st.session_state['selected_apartment'])
            st.write("Recommended Properties:")
            st.dataframe(recommendation_df)
        else:
            st.write("Please select an apartment to get recommendations.")
else:
    st.write("Location data is not loaded correctly. Please check the dataset.")
