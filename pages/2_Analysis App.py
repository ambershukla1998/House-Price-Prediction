# import pickle
# import numpy as np
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
#
# # Streamlit Configuration
# st.set_page_config(page_title="Price Predictor")
# st.title("Analytics")
#
# # Load pre-saved feature text and dataset
#
# import os
# import pickle
#
# # Get the current directory (the script's location)
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # Get the parent directory of the current directory
# parent_dir = os.path.dirname(current_dir)
#
# # Try loading feature_text.pkl using the relative path
# try:
#     with open(os.path.join(parent_dir, "datasets", "feature_text.pkl"), 'rb') as file:
#         feature_text = pickle.load(file)
#     print("Loaded feature_text from the relative path.")
# except FileNotFoundError:
#     # Fallback to absolute path if the file is not found
#     try:
#         with open(r"D:\ml project\house price prediction\datasets\feature_text.pkl", 'rb') as file:
#             feature_text = pickle.load(file)
#         print("Loaded feature_text from the absolute path.")
#     except FileNotFoundError:
#         print("The file feature_text.pkl could not be found.")
#
# # feature_text = pickle.load(open(r"D:\ml project\house price prediction\datasets\feature_text.pkl", "rb"))
#
#
# new_df = pd.read_csv(r"D:\ml project\house price prediction\datasets\data_viz1.csv")
#
# # Group data by sector for plotting
# group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
# st.header('Sector Price per Sqft Geomap')
# # Plotly Mapbox visualization
# fig = px.scatter_mapbox(
#     group_df,
#     lat="latitude",
#     lon="longitude",
#     color="price_per_sqft",
#     size="built_up_area",
#     color_continuous_scale=px.colors.cyclical.IceFire,
#     zoom=10,
#     mapbox_style="open-street-map",
#     width=1200,
#     height=700,
#     hover_name=group_df.index,
# )
# st.plotly_chart(fig, use_container_width=True)
#
#
# st.header('Features Worldcloud')
# # Dropdown for selecting sector
# wordcloud_df = pd.read_csv(r"D:\ml project\house price prediction\datasets\wordcloud.csv")
# selected_sector = st.selectbox("Select a Sector for Word Cloud", wordcloud_df['sector'].unique())
# # Generate WordCloud for the selected sector
# if selected_sector:
#     sector_data = wordcloud_df[wordcloud_df['sector'] == selected_sector]
#     text = " ".join(sector_data['features'].astype(str))  # Replace 'built_up_area' with the column for word cloud data
#     wordcloud = WordCloud(
#         width=800,
#         height=800,
#         background_color='white',
#         stopwords=set(['s']),  # Add your stopwords here
#         min_font_size=10
#     ).generate(text)
#
#     # Display the word cloud
#     st.subheader(f"Word Cloud for Sector: {selected_sector}")
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.imshow(wordcloud, interpolation="bilinear")
#     ax.axis("off")
#     st.pyplot(fig)
#
#
# # Streamlit Header
# st.header('Area vs Price')
#
#
# # Property type selection
# property_type = st.selectbox("Select property type", ['flat', 'house'])
#
# # Create the scatter plot based on the selected property type
# if property_type == 'house':
#     fig1 = px.scatter(
#         new_df[new_df['property_type'] == 'house'],
#         x="built_up_area",
#         y="price",
#         color="bedRoom",
#         title="Area Vs Price (House)"
#     )
# else:
#     fig1 = px.scatter(
#         new_df[new_df['property_type'] == 'flat'],
#         x="built_up_area",
#         y="price",
#         color="bedRoom",
#         title="Area Vs Price (Flat)"
#     )
#
# # Display the chart
# st.plotly_chart(fig1, use_container_width=True)
#
# # Streamlit Header
# st.header('BHK Pie Chart')
#
# # Sector Dropdown for Pie Chart
# sector_options = new_df['sector'].unique().tolist()
# sector_options.insert(0, 'overall')  # Add "overall" option for all sectors
# selected_sector_pie = st.selectbox('Select Sector', sector_options, key="sector_pie")
#
# # Property Type Dropdown for Pie Chart
# property_type_pie = st.selectbox("Select Property Type ", ['flat', 'house'], key="property_type_pie")
#
# # Filter the dataset for Pie Chart
# filtered_df_pie = new_df.copy()
# if selected_sector_pie != 'overall':
#     filtered_df_pie = filtered_df_pie[filtered_df_pie['sector'] == selected_sector_pie]
#
# filtered_df_pie = filtered_df_pie[filtered_df_pie['property_type'] == property_type_pie]
#
# # Group the data by number of bedrooms for the pie chart
# bhk_counts = filtered_df_pie['bedRoom'].value_counts().reset_index()
# bhk_counts.columns = ['bedRoom', 'count']
#
# # Display the Pie Chart or Warning
# if bhk_counts.empty:
#     st.warning("No data available for the selected filters.")
# else:
#     fig_pie = px.pie(
#         bhk_counts,
#         names='bedRoom',
#         values='count',
#         title=f'BHK Distribution for {selected_sector_pie} ({property_type_pie})',
#         hole=0.3  # To make it a donut chart, change this value
#     )
#     st.plotly_chart(fig_pie, use_container_width=True)
#
# # Scatter Plot Section
# st.header('BHK Scatter Plot')
#
# # Sector Dropdown for Scatter Plot
# selected_sector_scatter = st.selectbox('Select Sector', sector_options, key="sector_scatter")
#
# # Property Type Dropdown for Scatter Plot
# property_type_scatter = st.selectbox("Select Property Type ", ['flat', 'house'], key="property_type_scatter")
#
# # Filter the dataset for Scatter Plot
# if selected_sector_scatter != 'overall':
#     filtered_df_scatter = new_df[
#         (new_df['sector'] == selected_sector_scatter) & (new_df['property_type'] == property_type_scatter)
#     ]
# else:
#     filtered_df_scatter = new_df[new_df['property_type'] == property_type_scatter]
#
# # Display the Scatter Plot or Warning
# if not filtered_df_scatter.empty:
#     fig_scatter = px.scatter(
#         filtered_df_scatter,
#         x='bedRoom',  # X-axis for scatter plot
#         y='price',    # Y-axis for scatter plot
#         color='sector',  # Color based on sector
#         size='built_up_area',  # Size of markers
#         title=f"Scatter Plot: {property_type_scatter.capitalize()} in {selected_sector_scatter}",
#         labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'},
#         hover_data=['sector', 'price_per_sqft']  # Additional hover data
#     )
#     st.plotly_chart(fig_scatter, use_container_width=True)
# else:
#     st.warning(f"No data available for the selected options: Sector - {selected_sector_scatter}, Property Type - {property_type_scatter}")
#
# st.header('Side By Side BKH Price Comparison')
#
# # Create the box plot
# fig_3 = px.box(
#     new_df[new_df['bedRoom'] <= 4],  # Filter data for BHK <= 4
#     x='bedRoom',
#     y='price',
#     title='BHK Price Range',
#     labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'},  # Add axis labels
#     #color='bedRoom'  # Optional: Color boxes by number of bedrooms
# )
#
# # Display the plot in Streamlit
# st.plotly_chart(fig_3, use_container_width=True)
# # Streamlit Header
# st.header('Price vs Density Distribution')
#
# # Sidebar Filters
# st.sidebar.header("Filters")
# property_types = st.sidebar.multiselect(
#     "Select Property Types",
#     options=new_df['property_type'].unique().tolist(),
#     default=new_df['property_type'].unique().tolist()
# )
#
# price_range = st.sidebar.slider(
#     "Select Price Range",
#     min_value=int(new_df['price'].min()),
#     max_value=int(new_df['price'].max()),
#     value=(int(new_df['price'].min()), int(new_df['price'].max()))
# )
#
# # Filter data based on selections
# filtered_df = new_df[
#     (new_df['property_type'].isin(property_types)) &
#     (new_df['price'] >= price_range[0]) &
#     (new_df['price'] <= price_range[1])
# ]
#
# # Display filtered data count
# st.write(f"Filtered data includes {len(filtered_df)} properties.")
#
# # Create the interactive plot
# fig = px.histogram(
#     filtered_df,
#     x='price',
#     color='property_type',
#     nbins=50,
#     marginal='violin',  # Adds a violin plot on the side
#     histnorm='density',
#     title='Interactive Price Density Distribution',
#     labels={'price': 'Price', 'density': 'Density'},
#     hover_data={'price': ':.2f', 'property_type': True},  # Custom hover formatting
#     opacity=0.7,
# )
#
# # Add hovertemplate for detailed interaction
# fig.update_traces(
#     hovertemplate="<b>Price:</b> %{x}<br><b>Density:</b> %{y}<br><b>Type:</b> %{color}"
# )
#
# # Customize layout
# fig.update_layout(
#     xaxis_title="Price",
#     yaxis_title="Density",
#     legend_title="Property Type",
#     template="plotly_white",
#     width=900,
#     height=600,
# )
#
# # Add Range Slider for Interactive Control
# fig.update_xaxes(rangeslider_visible=True)
#
# # Display the plot
# st.plotly_chart(fig, use_container_width=True)
#
# # Additional Insights (if data is available)
# if not filtered_df.empty:
#     avg_price = filtered_df['price'].mean()
#     max_price = filtered_df['price'].max()
#     min_price = filtered_df['price'].min()
#     st.markdown(f"""
#     ### Additional Insights:
#     - **Average Price:** ₹{avg_price:,.2f}
#     - **Max Price:** ₹{max_price:,.2f}
#     - **Min Price:** ₹{min_price:,.2f}
#     """)
# else:
#     st.warning("No data available for the selected filters.")
#

# import os
# import pickle
# import numpy as np
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
#
# # --- App Configuration ---
# st.set_page_config(page_title="🏡 House Price Insights", layout="wide")
# st.title("📊 House Price Analytics Dashboard")
#
# # --- Load Data Section ---
#
#
# import pickle
#
# import pandas as pd
# import joblib
# from pathlib import Path
# import streamlit as st
#
# @st.cache_data
# def load_data():
#     try:
#         data_dir = Path(__file__).resolve().parent.parent / "datasets"
#
#         st.write("📂 Loading from:", data_dir)
#         st.write("🔑 Trying to load:", data_dir / "feature_text.pkl")
#
#         # ✅ Use joblib instead of pickle
#         feature_text = joblib.load(data_dir / "feature_text.pkl")
#
#         new_df = pd.read_csv(data_dir / "data_viz1.csv")
#         wordcloud_df = pd.read_csv(data_dir / "wordcloud.csv")
#
#         return feature_text, new_df, wordcloud_df
#
#     except Exception as e:
#         st.error(f"❌ Error loading data: {e}")
#         return None, None, None
#
#
#
# feature_text, new_df, wordcloud_df = load_data()
# if new_df is None:
#     st.stop()
#
# # --- Sidebar Filters ---
# st.sidebar.header("🔧 Filters")
# property_types = st.sidebar.multiselect("Select Property Types", new_df['property_type'].unique(), default=new_df['property_type'].unique())
# price_range = st.sidebar.slider("Select Price Range", int(new_df['price'].min()), int(new_df['price'].max()), (int(new_df['price'].min()), int(new_df['price'].max())))
#
# filtered_df = new_df[(new_df['property_type'].isin(property_types)) & (new_df['price'].between(price_range[0], price_range[1]))]
#
# # --- Sector Price GeoMap ---
# st.subheader("🗺️ Price per Sqft Across Sectors")
# group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
# fig_geo = px.scatter_mapbox(
#     group_df,
#     lat="latitude", lon="longitude",
#     color="price_per_sqft", size="built_up_area",
#     color_continuous_scale=px.colors.sequential.Viridis,
#     hover_name="sector", zoom=10,
#     mapbox_style="open-street-map",
#     width=1200, height=650
# )
# st.plotly_chart(fig_geo, use_container_width=True)
#
# # --- Word Cloud ---
# st.subheader("☁️ Word Cloud of Features by Sector")
# selected_sector = st.selectbox("Choose a sector", wordcloud_df['sector'].unique())
# text_data = " ".join(wordcloud_df[wordcloud_df['sector'] == selected_sector]['features'].astype(str))
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
# fig_wc, ax = plt.subplots(figsize=(10, 5))
# ax.imshow(wordcloud, interpolation="bilinear")
# ax.axis("off")
# st.pyplot(fig_wc)
#
# # --- Area vs Price ---
# st.subheader("📐 Area vs Price Scatter")
# property_type = st.radio("Select Property Type", ['flat', 'house'], horizontal=True)
# df_plot = new_df[new_df['property_type'] == property_type]
# fig_area = px.scatter(df_plot, x="built_up_area", y="price", color="bedRoom", title=f"Area vs Price for {property_type.title()}s")
# st.plotly_chart(fig_area, use_container_width=True)
#
# # --- Pie Chart: BHK Distribution ---
# st.subheader("🥧 BHK Distribution")
# sector_opt = st.selectbox("Choose Sector", ['overall'] + sorted(new_df['sector'].unique()))
# prop_type_opt = st.selectbox("Property Type", ['flat', 'house'], key="pie_property")
# df_pie = new_df[(new_df['property_type'] == prop_type_opt)]
# if sector_opt != 'overall':
#     df_pie = df_pie[df_pie['sector'] == sector_opt]
#
# bhk_counts = df_pie['bedRoom'].value_counts().reset_index()
# bhk_counts.columns = ['bedRoom', 'count']
#
# if bhk_counts.empty:
#     st.warning("No data available for this selection.")
# else:
#     fig_pie = px.pie(bhk_counts, names='bedRoom', values='count', hole=0.4,
#                      title=f"BHK Distribution for {sector_opt} ({prop_type_opt})")
#     st.plotly_chart(fig_pie, use_container_width=True)
#
# # --- BHK vs Price Scatter ---
# st.subheader("📊 BHK vs Price Scatter Plot")
# scatter_sector = st.selectbox("Sector", ['overall'] + sorted(new_df['sector'].unique()), key="scatter_sector")
# scatter_type = st.selectbox("Property Type", ['flat', 'house'], key="scatter_type")
# df_scatter = new_df[(new_df['property_type'] == scatter_type)]
# if scatter_sector != 'overall':
#     df_scatter = df_scatter[df_scatter['sector'] == scatter_sector]
#
# if df_scatter.empty:
#     st.warning("No data found for selected options.")
# else:
#     fig_scatter = px.scatter(df_scatter, x='bedRoom', y='price', color='sector',
#                              size='built_up_area', hover_data=['price_per_sqft'],
#                              title=f"{scatter_type.title()}s in {scatter_sector}")
#     st.plotly_chart(fig_scatter, use_container_width=True)
#
# # --- Box Plot: Price Comparison by BHK ---
# st.subheader("🪟 BHK-wise Price Comparison")
# fig_box = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price',
#                  title='BHK-wise Price Range (≤ 4 BHK)',
#                  labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'})
# st.plotly_chart(fig_box, use_container_width=True)
#
# # --- Price Density Histogram ---
# st.subheader("📈 Price Distribution & Density")
# fig_hist = px.histogram(
#     filtered_df,
#     x='price',
#     color='property_type',
#     nbins=50,
#     marginal='violin',
#     histnorm='density',
#     title='Price Density by Property Type',
#     opacity=0.75
# )
# fig_hist.update_layout(bargap=0.1)
# fig_hist.update_xaxes(rangeslider_visible=True)
# st.plotly_chart(fig_hist, use_container_width=True)
#
# # --- Summary Statistics ---
# if not filtered_df.empty:
#     avg_price = filtered_df['price'].mean()
#     st.markdown(f"""
#     #### 📌 Summary:
#     - **Properties Displayed:** {len(filtered_df)}
#     - **Average Price:** ₹{avg_price:,.2f}
#     - **Max Price:** ₹{filtered_df['price'].max():,.2f}
#     - **Min Price:** ₹{filtered_df['price'].min():,.2f}
#     """)
# else:
#     st.warning("No properties match the selected filters.")


import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

# --- App Configuration ---
st.set_page_config(page_title="🏡 House Price Insights", layout="wide")
st.title("📊 House Price Analytics Dashboard")

# --- Load Data Section ---
@st.cache_data
def load_data():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(base_dir, "..", "datasets"))

        st.write("📂 Loading from:", data_dir)
        file_path = os.path.join(data_dir, "feature_text.pkl")
        st.write("🔑 Trying to load:", file_path)

        # Debug: check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Try reading the pkl file
        feature_text = joblib.load(file_path)
        new_df = pd.read_csv(os.path.join(data_dir, "data_viz1.csv"))
        wordcloud_df = pd.read_csv(os.path.join(data_dir, "wordcloud.csv"))

        return feature_text, new_df, wordcloud_df

    except Exception as e:
        import traceback
        st.error(f"❌ Error loading data: {str(e)}")
        st.code(traceback.format_exc(), language='python')
        return None, None, None


# Load Data
feature_text, new_df, wordcloud_df = load_data()
if new_df is None:
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("🔧 Filters")
property_types = st.sidebar.multiselect("Select Property Types", new_df['property_type'].unique(), default=new_df['property_type'].unique())
price_range = st.sidebar.slider("Select Price Range", int(new_df['price'].min()), int(new_df['price'].max()), (int(new_df['price'].min()), int(new_df['price'].max())))

filtered_df = new_df[(new_df['property_type'].isin(property_types)) & (new_df['price'].between(price_range[0], price_range[1]))]

# --- Sector Price GeoMap ---
st.subheader("🗺️ Price per Sqft Across Sectors")
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
fig_geo = px.scatter_mapbox(
    group_df,
    lat="latitude", lon="longitude",
    color="price_per_sqft", size="built_up_area",
    color_continuous_scale=px.colors.sequential.Viridis,
    hover_name="sector", zoom=10,
    mapbox_style="open-street-map",
    width=1200, height=650
)
st.plotly_chart(fig_geo, use_container_width=True)

# --- Word Cloud ---
st.subheader("☁️ Word Cloud of Features by Sector")
selected_sector = st.selectbox("Choose a sector", wordcloud_df['sector'].unique())
text_data = " ".join(wordcloud_df[wordcloud_df['sector'] == selected_sector]['features'].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
fig_wc, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig_wc)

# --- Area vs Price ---
st.subheader("📐 Area vs Price Scatter")
property_type = st.radio("Select Property Type", ['flat', 'house'], horizontal=True)
df_plot = new_df[new_df['property_type'] == property_type]
fig_area = px.scatter(df_plot, x="built_up_area", y="price", color="bedRoom", title=f"Area vs Price for {property_type.title()}s")
st.plotly_chart(fig_area, use_container_width=True)

# --- Pie Chart: BHK Distribution ---
st.subheader("🥧 BHK Distribution")
sector_opt = st.selectbox("Choose Sector", ['overall'] + sorted(new_df['sector'].unique()))
prop_type_opt = st.selectbox("Property Type", ['flat', 'house'], key="pie_property")
df_pie = new_df[(new_df['property_type'] == prop_type_opt)]
if sector_opt != 'overall':
    df_pie = df_pie[df_pie['sector'] == sector_opt]

bhk_counts = df_pie['bedRoom'].value_counts().reset_index()
bhk_counts.columns = ['bedRoom', 'count']

if bhk_counts.empty:
    st.warning("No data available for this selection.")
else:
    fig_pie = px.pie(bhk_counts, names='bedRoom', values='count', hole=0.4,
                     title=f"BHK Distribution for {sector_opt} ({prop_type_opt})")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- BHK vs Price Scatter ---
st.subheader("📊 BHK vs Price Scatter Plot")
scatter_sector = st.selectbox("Sector", ['overall'] + sorted(new_df['sector'].unique()), key="scatter_sector")
scatter_type = st.selectbox("Property Type", ['flat', 'house'], key="scatter_type")
df_scatter = new_df[(new_df['property_type'] == scatter_type)]
if scatter_sector != 'overall':
    df_scatter = df_scatter[df_scatter['sector'] == scatter_sector]

if df_scatter.empty:
    st.warning("No data found for selected options.")
else:
    fig_scatter = px.scatter(df_scatter, x='bedRoom', y='price', color='sector',
                             size='built_up_area', hover_data=['price_per_sqft'],
                             title=f"{scatter_type.title()}s in {scatter_sector}")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Box Plot: Price Comparison by BHK ---
st.subheader("🪟 BHK-wise Price Comparison")
fig_box = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price',
                 title='BHK-wise Price Range (≤ 4 BHK)',
                 labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'})
st.plotly_chart(fig_box, use_container_width=True)

# --- Price Density Histogram ---
st.subheader("📈 Price Distribution & Density")
fig_hist = px.histogram(
    filtered_df,
    x='price',
    color='property_type',
    nbins=50,
    marginal='violin',
    histnorm='density',
    title='Price Density by Property Type',
    opacity=0.75
)
fig_hist.update_layout(bargap=0.1)
fig_hist.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig_hist, use_container_width=True)

# --- Summary Statistics ---
if not filtered_df.empty:
    avg_price = filtered_df['price'].mean()
    st.markdown(f"""
    #### 📌 Summary:
    - **Properties Displayed:** {len(filtered_df)}
    - **Average Price:** ₹{avg_price:,.2f}
    - **Max Price:** ₹{filtered_df['price'].max():,.2f}
    - **Min Price:** ₹{filtered_df['price'].min():,.2f}
    """)
else:
    st.warning("No properties match the selected filters.")
