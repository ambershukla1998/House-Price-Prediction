import pickle
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import os

# Streamlit page configuration
st.set_page_config(page_title="Interactive Apartment Recommendations")

# Adjust the dataset directory to be relative to the project root
dataset_dir = os.path.join(os.getcwd(), "datasets")
st.write(f"Adjusted datasets directory path: {dataset_dir}")

# Helper function to load a file
def load_file(filename):
    file_path = os.path.join(dataset_dir, filename)
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"File '{filename}' not found at path: {file_path}")
        return None
    except pickle.UnpicklingError:
        st.error(f"Error unpickling '{filename}'. The file may be corrupted.")
        return None
    except Exception as e:
        st.error(f"Error loading '{filename}': {str(e)}")
        return None

# Load the datasets
location_df = load_file("location_distance.pkl")
cosine_sim1 = load_file("cosine_sim1.pkl")
cosine_sim2 = load_file("cosine_sim2.pkl")
cosine_sim3 = load_file("cosine_sim3.pkl")

# Load CSV file
csv_path = os.path.join(dataset_dir, "data_viz1.csv")
try:
    df1 = pd.read_csv(csv_path)
    st.write("CSV file loaded successfully!")
except FileNotFoundError:
    st.error(f"CSV file not found at the specified path: {csv_path}")
    df1 = None
except Exception as e:
    st.error(f"Error loading CSV file: {str(e)}")
    df1 = None

# Function to recommend properties with scores
def recommend_properties_with_scores(property_name, top_n=5):
    try:
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
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Streamlit UI
st.title('Interactive Apartment Recommendations')

# Location and Radius selection
st.header('Select Location and Radius')
if location_df is not None:
    location_options = sorted(location_df.columns.to_list())
    selected_location = st.selectbox('Location', location_options)
    radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)

    if st.button('Search'):
        try:
            # Filter locations within the specified radius (converted to meters)
            filtered_locations = location_df[location_df[selected_location] < (radius * 1000)][selected_location].sort_values()
            if not filtered_locations.empty:
                st.session_state['filtered_apartments'] = filtered_locations.index.to_list()
                st.write(f"Locations within {radius} km from {selected_location}:")
                for key, value in filtered_locations.items():
                    st.text(f"{key}: {round(value / 1000, 2)} kms")
            else:
                st.warning("No locations found within the specified radius.")
                st.session_state['filtered_apartments'] = []
        except Exception as e:
            st.error(f"Error during location filtering: {str(e)}")

# Apartment Recommendation
st.header('Apartment Recommendation')
if 'filtered_apartments' not in st.session_state:
    st.session_state['filtered_apartments'] = []

# Check if there are filtered apartments from the search
if st.session_state['filtered_apartments']:
    apartment_options = st.session_state['filtered_apartments']
else:
    # If no search was performed, provide all available apartments
    apartment_options = location_df.index.to_list() if location_df is not None else []

selected_apartment = st.selectbox('Select an apartment', apartment_options, key='apartment_selection')

if st.button('Recommend', key='recommend_button'):
    if selected_apartment:
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        if not recommendation_df.empty:
            st.write("Recommended Apartments:")
            st.dataframe(recommendation_df)
        else:
            st.warning("No recommendations found.")
    else:
        st.warning("Please select an apartment to get recommendations.")
