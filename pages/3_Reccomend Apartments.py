# import os
# import gdown
# import pickle
# import streamlit as st
# import pandas as pd
#
# # Set the page config for Streamlit
# st.set_page_config(page_title="Interactive Apartment Recommendations")
#
# # Define dataset directory (relative path)
# DATASET_DIR = os.path.join(os.getcwd(), "datasets")  # Use relative path to the dataset folder
#
#
# # Function to download files from Google Drive
# def download_from_gdrive(file_id, filename):
#     try:
#         # Construct the URL to download the file from Google Drive
#         url = f"https://drive.google.com/uc?export=download&id={file_id}"
#         output_path = os.path.join(DATASET_DIR, filename)
#
#         # Download the file using gdown
#         gdown.download(url, output_path, quiet=False)
#
#         # Check if the file exists after downloading
#         if os.path.exists(output_path):
#             st.write(f"Successfully downloaded {filename}")
#         else:
#             st.error(f"Failed to download {filename}. The file was not saved correctly.")
#     except Exception as e:
#         st.error(f"Error downloading {filename}: {str(e)}")
#         print(f"Error downloading {filename}: {str(e)}")
#
#
# # Example file IDs for location_distance, cosine_sim3, cosine_sim2, and cosine_sim1
# file_ids = {
#     "location_distance.pkl": "1HTrAJHhi_ZVFYQtxq_8fbV-EbiC73WUz",  # Your actual file ID for location_distance.pkl
#     "cosine_sim3.pkl": "1WKxGszmIS5-Fvl1lO2O8VyDRnkhGSmUs",  # Your actual file ID for cosine_sim3.pkl
#     "cosine_sim2.pkl": "1Nd7XIGH77ELlA9OvNdXAfVr42QEoK27o",  # Your actual file ID for cosine_sim2.pkl
#     "cosine_sim1.pkl": "1vUewOgl-ubKpFbWKbQi9YKp0YrgmtJcY",  # Your actual file ID for cosine_sim1.pkl
# }
#
# # Check and download files if they don't exist
# for filename, file_id in file_ids.items():
#     if not os.path.exists(os.path.join(DATASET_DIR, filename)):
#         download_from_gdrive(file_id, filename)
#
#
# # Helper function to load pickle files
# def load_file(filename):
#     file_path = os.path.join(DATASET_DIR, filename)
#     try:
#         # Try to open and load the pickle file
#         with open(file_path, 'rb') as file:
#             data = pickle.load(file)
#             return data
#     except FileNotFoundError:
#         st.error(
#             f"File '{filename}' not found in {DATASET_DIR}. Please make sure the dataset is in the correct directory.")
#         return None
#     except pickle.UnpicklingError:
#         st.error(f"Error unpickling '{filename}'. The file may be corrupted or incompatible.")
#         return None
#     except Exception as e:
#         st.error(f"Error loading '{filename}': {str(e)}")
#         return None
#
#
# # Load the pickle files directly from the datasets folder
# location_df = load_file("location_distance.pkl")
# cosine_sim1 = load_file("cosine_sim1.pkl")
# cosine_sim2 = load_file("cosine_sim2.pkl")
# cosine_sim3 = load_file("cosine_sim3.pkl")
#
# # Load the CSV file
# csv_path = os.path.join(DATASET_DIR, "data_viz1.csv")
# try:
#     df1 = pd.read_csv(csv_path)
# except FileNotFoundError:
#     st.error(f"CSV file not found at {csv_path}")
#     df1 = None
# except Exception as e:
#     st.error(f"Error loading CSV file: {str(e)}")
#     df1 = None
#
#
# # Function to recommend properties with scores
# def recommend_properties_with_scores(property_name, top_n=5):
#     try:
#         if location_df is None or cosine_sim1 is None or cosine_sim2 is None or cosine_sim3 is None:
#             st.error("Required data files are missing. Please ensure all pickle files are in the correct directory.")
#             return pd.DataFrame()
#
#         cosine_sim_matrix = 3 * cosine_sim1 + 5 * cosine_sim2 + 6 * cosine_sim3
#         sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
#         sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#         top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
#         top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
#         top_properties = location_df.index[top_indices].tolist()
#         recommendations_df = pd.DataFrame({
#             'PropertyName': top_properties,
#             'SimilarityScore': top_scores
#         })
#         return recommendations_df
#     except Exception as e:
#         st.error(f"Error generating recommendations: {str(e)}")
#         return pd.DataFrame()
#
#
# # Streamlit UI
# st.title('Interactive Apartment Recommendations')
#
# st.header('Select Location and Radius')
# if location_df is not None:
#     location_options = sorted(location_df.columns.to_list())
#     selected_location = st.selectbox('Location', location_options)
#     radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)
#
#     if st.button('Search'):
#         try:
#             filtered_locations = location_df[location_df[selected_location] < (radius * 1000)][
#                 selected_location].sort_values()
#             if not filtered_locations.empty:
#                 st.session_state['filtered_apartments'] = filtered_locations.index.to_list()
#                 st.write(f"Locations within {radius} km from {selected_location}:")
#                 for key, value in filtered_locations.items():
#                     st.text(f"{key}: {round(value / 1000, 2)} kms")
#             else:
#                 st.warning("No locations found within the specified radius.")
#                 st.session_state['filtered_apartments'] = []
#         except Exception as e:
#             st.error(f"Error during location filtering: {str(e)}")
#
# st.header('Apartment Recommendation')
# if 'filtered_apartments' not in st.session_state:
#     st.session_state['filtered_apartments'] = []
#
# if st.session_state['filtered_apartments']:
#     apartment_options = st.session_state['filtered_apartments']
# else:
#     apartment_options = location_df.index.to_list() if location_df is not None else []
#
# selected_apartment = st.selectbox('Select an apartment', apartment_options)
#
# if st.button('Recommend'):
#     if selected_apartment:
#         recommendation_df = recommend_properties_with_scores(selected_apartment)
#         if not recommendation_df.empty:
#             st.write("Recommended Apartments:")
#             st.dataframe(recommendation_df)
#         else:
#             st.warning("No recommendations found.")
#     else:
#         st.warning("Please select an apartment to get recommendations.")


import os
import gdown
import pickle
import streamlit as st
import pandas as pd

# Set the page config for Streamlit
st.set_page_config(page_title="Interactive Apartment Recommendations")

# Define dataset directory (relative path)
DATASET_DIR = os.path.join(os.getcwd(), "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)  # Ensure the directory exists

# Optional file inspection (first few bytes)
def inspect_file(filename):
    path = os.path.join(DATASET_DIR, filename)
    try:
        with open(path, 'rb') as f:
            content = f.read(100)
            print(f"First 100 bytes of {filename}: {content[:100]}")
    except Exception as e:
        print(f"Could not inspect file {filename}: {str(e)}")

# Optional MIME-type checker using `python-magic`
# def check_file_type(path):
#     import magic
#     mime = magic.from_file(path, mime=True)
#     print(f"File type of {path}: {mime}")

# Function to download files from Google Drive
def download_from_gdrive(file_id, filename):
    try:
        url = f"https://drive.google.com/uc?id={file_id}"
        output_path = os.path.join(DATASET_DIR, filename)

        gdown.download(url, output_path, quiet=False, fuzzy=True)

        if os.path.exists(output_path):
            st.write(f"✅ Successfully downloaded {filename}")
            inspect_file(filename)  # Inspect the first few bytes
            # check_file_type(output_path)  # Optional: check MIME type
        else:
            st.error(f"❌ Failed to save {filename}.")
    except Exception as e:
        st.error(f"🚨 Error downloading {filename}: {str(e)}")

# File IDs for Google Drive downloads
file_ids = {
    "location_distance.pkl": "1HTrAJHhi_ZVFYQtxq_8fbV-EbiC73WUz",
    "cosine_sim3.pkl": "1WKxGszmIS5-Fvl1lO2O8VyDRnkhGSmUs",
    "cosine_sim2.pkl": "1Nd7XIGH77ELlA9OvNdXAfVr42QEoK27o",
    "cosine_sim1.pkl": "1vUewOgl-ubKpFbWKbQi9YKp0YrgmtJcY",
}

# Download missing files
for filename, file_id in file_ids.items():
    if not os.path.exists(os.path.join(DATASET_DIR, filename)):
        download_from_gdrive(file_id, filename)

# Load pickle file
def load_file(filename):
    file_path = os.path.join(DATASET_DIR, filename)
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        st.error(f"❌ File '{filename}' not found in {DATASET_DIR}.")
        return None
    except pickle.UnpicklingError:
        st.error(f"⚠️ Unpickling error: '{filename}' may be corrupted or invalid.")
        return None
    except Exception as e:
        st.error(f"🚨 Error loading '{filename}': {str(e)}")
        return None

# Load datasets
location_df = load_file("location_distance.pkl")
cosine_sim1 = load_file("cosine_sim1.pkl")
cosine_sim2 = load_file("cosine_sim2.pkl")
cosine_sim3 = load_file("cosine_sim3.pkl")

# Load CSV file
csv_path = os.path.join(DATASET_DIR, "data_viz1.csv")
try:
    df1 = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"❌ CSV file not found at {csv_path}")
    df1 = None
except Exception as e:
    st.error(f"🚨 Error loading CSV: {str(e)}")
    df1 = None

# Recommend properties function
def recommend_properties_with_scores(property_name, top_n=5):
    try:
        if location_df is None or cosine_sim1 is None or cosine_sim2 is None or cosine_sim3 is None:
            st.error("❌ Required data files are missing.")
            return pd.DataFrame()

        cosine_sim_matrix = 3 * cosine_sim1 + 5 * cosine_sim2 + 6 * cosine_sim3
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
        top_properties = location_df.index[top_indices].tolist()

        return pd.DataFrame({
            'PropertyName': top_properties,
            'SimilarityScore': top_scores
        })
    except Exception as e:
        st.error(f"🚨 Error generating recommendations: {str(e)}")
        return pd.DataFrame()

# Streamlit UI
st.title('🏢 Interactive Apartment Recommendations')

st.header('📍 Select Location and Radius')
if location_df is not None:
    location_options = sorted(location_df.columns.to_list())
    selected_location = st.selectbox('Location', location_options)
    radius = st.number_input('Radius in Kms', min_value=0.1, value=5.0, step=0.1)

    if st.button('🔍 Search'):
        try:
            filtered_locations = location_df[location_df[selected_location] < (radius * 1000)][
                selected_location].sort_values()
            if not filtered_locations.empty:
                st.session_state['filtered_apartments'] = filtered_locations.index.to_list()
                st.write(f"Properties within {radius} km from {selected_location}:")
                for key, value in filtered_locations.items():
                    st.text(f"{key}: {round(value / 1000, 2)} km")
            else:
                st.warning("⚠️ No properties found within that radius.")
                st.session_state['filtered_apartments'] = []
        except Exception as e:
            st.error(f"🚨 Error filtering locations: {str(e)}")

st.header('🏘️ Apartment Recommendation')
if 'filtered_apartments' not in st.session_state:
    st.session_state['filtered_apartments'] = []

apartment_options = (
    st.session_state['filtered_apartments']
    if st.session_state['filtered_apartments']
    else location_df.index.to_list() if location_df is not None else []
)

selected_apartment = st.selectbox('Select an apartment', apartment_options)

if st.button('🎯 Recommend'):
    if selected_apartment:
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        if not recommendation_df.empty:
            st.write("📌 Recommended Apartments:")
            st.dataframe(recommendation_df)
        else:
            st.warning("⚠️ No recommendations found.")
    else:
        st.warning("⚠️ Please select an apartment to get recommendations.")

