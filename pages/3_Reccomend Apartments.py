import os
import gdown
import pickle
import streamlit as st
import pandas as pd

# Set the page config for Streamlit
st.set_page_config(page_title="Interactive Apartment Recommendations")

# Define dataset directory (relative path)
DATASET_DIR = os.path.join(os.getcwd(), "datasets")  # Use relative path to the dataset folder

# Ensure dataset directory exists
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# Function to download files from Google Drive
def download_from_gdrive(file_id, filename):
    try:
        # Construct the URL to download the file from Google Drive
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        output_path = os.path.join(DATASET_DIR, filename)

        # Download the file using gdown
        st.write(f"Downloading {filename} from Google Drive...")
        gdown.download(url, output_path, quiet=False)

        # Check if the file exists after downloading
        if os.path.exists(output_path):
            st.write(f"Successfully downloaded {filename}")
        else:
            st.error(f"Failed to download {filename}. The file was not saved correctly.")
    except Exception as e:
        st.error(f"Error downloading {filename}: {str(e)}")
        print(f"Error downloading {filename}: {str(e)}")

# Example file IDs for location_distance, cosine_sim3, cosine_sim2, and cosine_sim1
file_ids = {
    "location_distance.pkl": "1HTrAJHhi_ZVFYQtxq_8fbV-EbiC73WUz",  # Your actual file ID for location_distance.pkl
    "cosine_sim3.pkl": "1WKxGszmIS5-Fvl1lO2O8VyDRnkhGSmUs",  # Your actual file ID for cosine_sim3.pkl
    "cosine_sim2.pkl": "1Nd7XIGH77ELlA9OvNdXAfVr42QEoK27o",  # Your actual file ID for cosine_sim2.pkl
    "cosine_sim1.pkl": "1vUewOgl-ubKpFbWKbQi9YKp0YrgmtJcY",  # Your actual file ID for cosine_sim1.pkl
}

# Function to check if file exists and download it if not
def check_and_download_file(filename, file_id):
    file_path = os.path.join(DATASET_DIR, filename)
    if os.path.exists(file_path):
        st.write(f"File {filename} already exists.")
    else:
        st.write(f"Downloading {filename}...")
        download_from_gdrive(file_id, filename)

# Check and download files if they don't exist
for filename, file_id in file_ids.items():
    check_and_download_file(filename, file_id)

# Helper function to load pickle files with enhanced error handling
def load_file(filename):
    file_path = os.path.join(DATASET_DIR, filename)
    try:
        # Try to open and load the pickle file
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            st.write(f"Successfully loaded {filename}")
            return data
    except FileNotFoundError:
        st.error(f"File '{filename}' not found in {DATASET_DIR}. Please make sure the dataset is in the correct directory.")
        return None
    except pickle.UnpicklingError:
        st.error(f"Error unpickling '{filename}'. The file may be corrupted or incompatible.")
        return None
    except Exception as e:
        st.error(f"Error loading '{filename}': {str(e)}")
        return None

# Load pickle files
location_df = load_file("location_distance.pkl")
cosine_sim1 = load_file("cosine_sim1.pkl")
cosine_sim2 = load_file("cosine_sim2.pkl")
cosine_sim3 = load_file("cosine_sim3.pkl")

# Load the CSV file
csv_path = os.path.join(DATASET_DIR, "data_viz1.csv")
try:
    df1 = pd.read_csv(csv_path)
    st.write("CSV file loaded successfully!")
except FileNotFoundError:
    st.error(f"CSV file not found at {csv_path}")
    df1 = None
except Exception as e:
    st.error(f"Error loading CSV file: {str(e)}")
    df1 = None

# Function to recommend properties with scores
def recommend_properties_with_scores(property_name, top_n=5):
    try:
        if location_df is None or cosine_sim1 is None or cosine_sim2 is None or cosine_sim3 is None:
            st.error("Required data files are missing. Please ensure all pickle files are in the correct directory.")
            return pd.DataFrame()

        # Combine the cosine similarity matrices with weights
        cosine_sim_matrix = 3 * cosine_sim1 + 5 * cosine_sim2 + 6 * cosine_sim3

        # Ensure that the property_name exists in the location_df
        if property_name not in location_df.index:
            st.error(f"Property '{property_name}' not found in the dataset.")
            return pd.DataFrame()

        # Get the similarity scores
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top_n recommendations
        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
        top_properties = location_df.index[top_indices].tolist()

        # Create a DataFrame with recommendations
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

st.header('Select Location and Radius')
if location_df is not None:
    location_options = sorted(location_df.columns.to_list())
    selected_location = st.selectbox('Location', location_options)
    radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)

    if st.button('Search'):
        try:
            # Filter locations within the selected radius
            filtered_locations = location_df[location_df[selected_location] < (radius * 1000)][
                selected_location].sort_values()

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

st.header('Apartment Recommendation')
if 'filtered_apartments' not in st.session_state:
    st.session_state['filtered_apartments'] = []

if st.session_state['filtered_apartments']:
    apartment_options = st.session_state['filtered_apartments']
else:
    apartment_options = location_df.index.to_list() if location_df is not None else []

selected_apartment = st.selectbox('Select an apartment', apartment_options)

if st.button('Recommend'):
    if selected_apartment:
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        if not recommendation_df.empty:
            st.write("Recommended Apartments:")
            st.dataframe(recommendation_df)
        else:
            st.warning("No recommendations found.")
    else:
        st.warning("Please select an apartment to get recommendations.")
