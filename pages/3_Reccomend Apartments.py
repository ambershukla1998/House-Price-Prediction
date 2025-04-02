# import pickle
# import streamlit as st
# import pandas as pd
#
# st.set_page_config(page_title="Recommend Apartments")
#
# # Load the dataset
# location_df = pickle.load(open('D:/ml project/house price prediction/datasets/location_distance.pkl', 'rb'))
# cosine_sim1 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim1.pkl', 'rb'))
# cosine_sim2 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim2.pkl', 'rb'))
# cosine_sim3 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim3.pkl', 'rb'))
#
#
# def recommend_properties_with_scores(property_name, top_n=5):
#     cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3
#     # cosine_sim_matrix = cosine_sim3
#
#     # Get the similarity scores for the property using its name as the index
#     sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
#
#     # Sort properties based on the similarity scores
#     sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#
#     # Get the indices and scores of the top_n most similar properties
#     top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
#     top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
#
#     # Retrieve the names of the top properties using the indices
#     top_properties = location_df.index[top_indices].tolist()
#
#     # Create a dataframe with the results
#     recommendations_df = pd.DataFrame({
#         'PropertyName': top_properties,
#         'SimilarityScore': top_scores
#     })
#
#     return recommendations_df
#
# # Location and Radius selection
# st.title('Select Location and Radius')
# location_options = sorted(location_df.columns.to_list())  # List of location options for selection
#
# # Select location for search
# selected_location = st.selectbox('Location', location_options)
#
# # Select radius in kilometers
# radius = st.number_input('Radius in Kms')
#
# #Search button functionality
# if st.button('Search'):
#     # Filter locations within the given radius (convert radius to meters for comparison)
#     result_search = location_df[location_df[selected_location] < (radius * 1000)][selected_location].sort_values()
#
#     # Display filtered locations
#     if not result_search.empty:
#         st.write(f"Locations within {radius} km from {selected_location}:")
#         for key, value in result_search.items():
#             st.text(f"{key}: {round(value / 1000, 2)} kms")
#         else:
#             st.write("No locations found within the specified radius.")
#
# # Recommend Apartments section
# st.title('Recommend Apartments')
#
# # Apartment selection dropdown
# selected_apartment = st.selectbox('Select an apartment', sorted(location_df.index.to_list()))
#
# # Recommendation button functionality
# if st.button('Recommend'):
#     recommendation_df=recommend_properties_with_scores(selected_apartment)
#     st.dataframe(recommendation_df)
import pickle
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Interactive Apartment Recommendations")

# Load datasets
# Load the dataset
# location_df = pickle.load(open('D:/ml project/house price prediction/datasets/location_distance.pkl', 'rb'))
# cosine_sim1 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim1.pkl', 'rb'))
# cosine_sim2 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim2.pkl', 'rb'))
# cosine_sim3 = pickle.load(open('D:/ml project/house price prediction/datasets/cosine_sim3.pkl', 'rb'))
########
import os
import pickle

# Get the current directory (the script's location)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the current directory
parent_dir = os.path.dirname(current_dir)

# Define a helper function to load a file
def load_file(filename):
    # Try loading from relative path
    try:
        with open(os.path.join(parent_dir, "datasets", filename), 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        # Fallback to absolute path if file is not found
        try:
            with open(f'D:/ml project/house price prediction/datasets/{filename}', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f"The file {filename} could not be found.")
            return None

# Load the datasets
location_df = load_file("location_distance.pkl")
cosine_sim1 = load_file("cosine_sim1.pkl")
cosine_sim2 = load_file("cosine_sim2.pkl")
cosine_sim3 = load_file("cosine_sim3.pkl")

# Check if files were loaded
if location_df is not None:
    print("Loaded location_distance.pkl successfully.")
if cosine_sim1 is not None:
    print("Loaded cosine_sim1.pkl successfully.")
if cosine_sim2 is not None:
    print("Loaded cosine_sim2.pkl successfully.")
if cosine_sim3 is not None:
    print("Loaded cosine_sim3.pkl successfully.")
#######


df1 = pd.read_csv(r"D:\ml project\house price prediction\datasets\data_viz1.csv")


def recommend_properties_with_scores(property_name, top_n=5):
    # Combine similarity matrices with assigned weights
    cosine_sim_matrix = 3 * cosine_sim1 + 5 * cosine_sim2 + 6 * cosine_sim3
    # Get similarity scores for the selected property
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    # Sort properties based on similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get indices and scores of top recommended properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    # Retrieve property names
    top_properties = location_df.index[top_indices].tolist()
    # Create a DataFrame with recommendations and their scores
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
location_options = sorted(location_df.columns.to_list())
selected_location = st.selectbox('Location', location_options)
radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)

if st.button('Search'):
    # Filter locations within the specified radius (converted to meters)
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

# Check if there are filtered apartments from the search
if st.session_state['filtered_apartments']:
    apartment_options = st.session_state['filtered_apartments']
else:
    # If no search was performed, provide all available apartments
    apartment_options = location_df.index.to_list()

selected_apartment = st.selectbox('Select an apartment', apartment_options, key='apartment_selection')
st.session_state['selected_apartment'] = selected_apartment

if st.button('Recommend', key='recommend_button'):
    if st.session_state['selected_apartment']:
        recommendation_df = recommend_properties_with_scores(st.session_state['selected_apartment'])
        recommendation_df
    else:
        st.write("Please select an apartment to get recommendations.")










