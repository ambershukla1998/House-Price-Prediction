# # import pickle
# # import numpy as np
# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # from wordcloud import WordCloud
# # import matplotlib.pyplot as plt
# #
# # # Streamlit Configuration
# # st.set_page_config(page_title="Price Predictor")
# # st.title('Analytics')
# # feature_text=pickle.load(open('D:\ml project\house price prediction\datasets\feature_text.pkl','rb'))
# #
# # # Load the dataset
# # new_df = pd.read_csv(r'D:\ml project\house price prediction\datasets\data_viz1.csv')
# # group_df = new_df.groupby('sector')[['price','price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
# # # Group data by sector
# #
# # # Plotly Mapbox visualization
# # fig = px.scatter_mapbox(
# #     group_df,
# #     lat="latitude",
# #     lon="longitude",
# #     color="price_per_sqft",
# #     size='built_up_area',
# #     color_continuous_scale=px.colors.cyclical.IceFire,
# #     zoom=10,
# #     mapbox_style="open-street-map",
# #     width=1200,
# #     height=700,
# #     hover_name=group_df.index
# # )
# #
# # # Display the plot in Streamlit
# # st.plotly_chart(fig, use_container_width=True)
# # wordcloud = WordCloud(width = 800, height = 800,
# #                       background_color ='white',
# #                       stopwords = set(['s']),  # Any stopwords you'd like to exclude
# #                       min_font_size = 10).generate(feature_text)
# #
# # plt.figure(figsize = (8, 8), facecolor = None)
# # plt.imshow(wordcloud, interpolation='bilinear')
# # plt.axis("off")
# # plt.tight_layout(pad = 0)
# # plt.show() # st.pyplot()
# import pickle
# import numpy as np
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
#
# # Streamlit Configuration
# st.set_page_config(page_title="Price Predictor", layout="wide")
# st.title('Analytics')
#
# # Load feature text
# try:
#     feature_text = pickle.load(open(r'D:\ml project\house price prediction\datasets\feature_text.pkl', 'rb'))
# except FileNotFoundError:
#     st.error("Feature text file not found.")
#     feature_text = ""
#
# # Load the dataset
# try:
#     new_df = pd.read_csv(r'D:\ml project\house price prediction\datasets\data_viz1.csv')
# except FileNotFoundError:
#     st.error("Dataset file not found.")
#     new_df = pd.DataFrame()
#
# if not new_df.empty:
#     # Group data by sector
#     group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
#
#     # Plotly Mapbox visualization
#     fig = px.scatter_mapbox(
#         group_df,
#         lat="latitude",
#         lon="longitude",
#         color="price_per_sqft",
#         size='built_up_area',
#         color_continuous_scale=px.colors.cyclical.IceFire,
#         zoom=10,
#         mapbox_style="open-street-map",
#         width=1200,
#         height=700,
#         hover_name=group_df.index
#     )
#
#     # Display the plot in Streamlit
#     st.plotly_chart(fig, use_container_width=True)
#
# # Generate WordCloud
# if feature_text:
#     wordcloud = WordCloud(
#         width=800,
#         height=800,
#         background_color='white',
#         stopwords=set(['s']),  # Any stopwords you'd like to exclude
#         min_font_size=10
#     ).generate(feature_text)
#
#     # Plot WordCloud
#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.imshow(wordcloud, interpolation='bilinear')
#     ax.axis("off")
#     st.pyplot(fig)
# else:
#     st.warning("Feature text is empty or invalid.")


import pickle
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Streamlit Configuration
st.set_page_config(page_title="Price Predictor")
st.title("Analytics")

# Load pre-saved feature text and dataset
feature_text = pickle.load(open(r"D:\ml project\house price prediction\datasets\feature_text.pkl", "rb"))
new_df = pd.read_csv(r"D:\ml project\house price prediction\datasets\data_viz1.csv")

# Group data by sector for plotting
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
st.header('Sector Price per Sqft Geomap')
# Plotly Mapbox visualization
fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=700,
    hover_name=group_df.index,
)
st.plotly_chart(fig, use_container_width=True)


st.header('Features Worldcloud')
# Dropdown for selecting sector
wordcloud_df = pd.read_csv(r"D:\ml project\house price prediction\datasets\wordcloud.csv")
selected_sector = st.selectbox("Select a Sector for Word Cloud", wordcloud_df['sector'].unique())
# Generate WordCloud for the selected sector
if selected_sector:
    sector_data = wordcloud_df[wordcloud_df['sector'] == selected_sector]
    text = " ".join(sector_data['features'].astype(str))  # Replace 'built_up_area' with the column for word cloud data
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='white',
        stopwords=set(['s']),  # Add your stopwords here
        min_font_size=10
    ).generate(text)

    # Display the word cloud
    st.subheader(f"Word Cloud for Sector: {selected_sector}")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)


# Streamlit Header
st.header('Area vs Price')


# Property type selection
property_type = st.selectbox("Select property type", ['flat', 'house'])

# Create the scatter plot based on the selected property type
if property_type == 'house':
    fig1 = px.scatter(
        new_df[new_df['property_type'] == 'house'],
        x="built_up_area",
        y="price",
        color="bedRoom",
        title="Area Vs Price (House)"
    )
else:
    fig1 = px.scatter(
        new_df[new_df['property_type'] == 'flat'],
        x="built_up_area",
        y="price",
        color="bedRoom",
        title="Area Vs Price (Flat)"
    )

# Display the chart
st.plotly_chart(fig1, use_container_width=True)




# fig1 = px.scatter(
#     new_df,
#     x="built_up_area",
#     y="price",
#     color="bedRoom",
#     title="Area Vs Price",
# )
#
# st.plotly_chart(fig1, use_container_width=True)


# Streamlit Header
st.header('BHK Pie Chart')

# Sector Dropdown for Pie Chart
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')  # Add "overall" option for all sectors
selected_sector_pie = st.selectbox('Select Sector', sector_options, key="sector_pie")

# Property Type Dropdown for Pie Chart
property_type_pie = st.selectbox("Select Property Type ", ['flat', 'house'], key="property_type_pie")

# Filter the dataset for Pie Chart
filtered_df_pie = new_df.copy()
if selected_sector_pie != 'overall':
    filtered_df_pie = filtered_df_pie[filtered_df_pie['sector'] == selected_sector_pie]

filtered_df_pie = filtered_df_pie[filtered_df_pie['property_type'] == property_type_pie]

# Group the data by number of bedrooms for the pie chart
bhk_counts = filtered_df_pie['bedRoom'].value_counts().reset_index()
bhk_counts.columns = ['bedRoom', 'count']

# Display the Pie Chart or Warning
if bhk_counts.empty:
    st.warning("No data available for the selected filters.")
else:
    fig_pie = px.pie(
        bhk_counts,
        names='bedRoom',
        values='count',
        title=f'BHK Distribution for {selected_sector_pie} ({property_type_pie})',
        hole=0.3  # To make it a donut chart, change this value
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Scatter Plot Section
st.header('BHK Scatter Plot')

# Sector Dropdown for Scatter Plot
selected_sector_scatter = st.selectbox('Select Sector', sector_options, key="sector_scatter")

# Property Type Dropdown for Scatter Plot
property_type_scatter = st.selectbox("Select Property Type ", ['flat', 'house'], key="property_type_scatter")

# Filter the dataset for Scatter Plot
if selected_sector_scatter != 'overall':
    filtered_df_scatter = new_df[
        (new_df['sector'] == selected_sector_scatter) & (new_df['property_type'] == property_type_scatter)
    ]
else:
    filtered_df_scatter = new_df[new_df['property_type'] == property_type_scatter]

# Display the Scatter Plot or Warning
if not filtered_df_scatter.empty:
    fig_scatter = px.scatter(
        filtered_df_scatter,
        x='bedRoom',  # X-axis for scatter plot
        y='price',    # Y-axis for scatter plot
        color='sector',  # Color based on sector
        size='built_up_area',  # Size of markers
        title=f"Scatter Plot: {property_type_scatter.capitalize()} in {selected_sector_scatter}",
        labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'},
        hover_data=['sector', 'price_per_sqft']  # Additional hover data
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning(f"No data available for the selected options: Sector - {selected_sector_scatter}, Property Type - {property_type_scatter}")


# st.header(' Plot')
# fig_3 = px.box(new_df[new_df['bedRoom'] <=4], x='bedRoom', y='price', title='BHK Price Range')
# st.plotly_chart(fig_3, use_container_width=True)
# fig.show()
# Streamlit Header
st.header('Side By Side BKH Price Comparison')

# Create the box plot
fig_3 = px.box(
    new_df[new_df['bedRoom'] <= 4],  # Filter data for BHK <= 4
    x='bedRoom',
    y='price',
    title='BHK Price Range',
    labels={'bedRoom': 'Number of Bedrooms', 'price': 'Price'},  # Add axis labels
    #color='bedRoom'  # Optional: Color boxes by number of bedrooms
)

# Display the plot in Streamlit
st.plotly_chart(fig_3, use_container_width=True)

# import seaborn as sns
# import matplotlib.pyplot as plt
# import streamlit as st
#
# # Streamlit Header
# st.header('Price Density Distribution by Property Type')
#
# # Property Type Selection
# property_type = st.radio("Select Property Type for Comparison", ['house', 'flat', 'both'])
#
# # Create the plot
# fig, ax = plt.subplots(figsize=(14, 6))
#
# if property_type == 'house':
#     sns.kdeplot(
#         data=new_df[new_df['property_type'] == 'house'],
#         x='price',
#         fill=True,
#         label='House',
#         color='blue',
#         ax=ax,
#         alpha=0.5,
#     )
#     ax.set_title('Price Density Distribution for Houses', fontsize=14)
#
# elif property_type == 'flat':
#     sns.kdeplot(
#         data=new_df[new_df['property_type'] == 'flat'],
#         x='price',
#         fill=True,
#         label='Flat',
#         color='green',
#         ax=ax,
#         alpha=0.5,
#     )
#     ax.set_title('Price Density Distribution for Flats', fontsize=14)
#
# else:  # For 'both' option
#     sns.kdeplot(
#         data=new_df[new_df['property_type'] == 'house'],
#         x='price',
#         fill=True,
#         label='House',
#         color='blue',
#         ax=ax,
#         alpha=0.5,
#     )
#     sns.kdeplot(
#         data=new_df[new_df['property_type'] == 'flat'],
#         x='price',
#         fill=True,
#         label='Flat',
#         color='green',
#         ax=ax,
#         alpha=0.5,
#     )
#     ax.set_title('Price Density Distribution for Houses and Flats', fontsize=14)
#
# # Add labels and legend
# ax.set_xlabel('Price', fontsize=12)
# ax.set_ylabel('Density', fontsize=12)
# ax.legend(title="Property Type", fontsize=10)
#
# # Adjust Y-axis for better density display (optional)
# ax.set_ylim(0, 0.6)
#
# # Display the plot in Streamlit
# st.pyplot(fig)

# import plotly.express as px
# import streamlit as st
# import pandas as pd
#
# # Streamlit Header
# st.header('Interactive Price Density Distribution by Property Type')
#
# # Property Type Selection
# property_type = st.radio("Select Property Type for Comparison", ['house', 'flat', 'both'])
#
# # Filter data based on property type
# filtered_df = new_df.copy()
# if property_type == 'house':
#     filtered_df = filtered_df[filtered_df['property_type'] == 'house']
# elif property_type == 'flat':
#     filtered_df = filtered_df[filtered_df['property_type'] == 'flat']
#
# # Create the interactive plot
# if property_type == 'both':
#     fig = px.histogram(
#         new_df,
#         x='price',
#         color='property_type',
#         nbins=50,
#         marginal='violin',  # Adds a violin plot on the side
#         histnorm='density',
#         title='Price Density Distribution for Houses and Flats',
#         labels={'price': 'Price', 'density': 'Density'},
#     )
# else:
#     fig = px.histogram(
#         filtered_df,
#         x='price',
#         nbins=50,
#         marginal='violin',  # Adds a violin plot on the side
#         histnorm='density',
#         title=f'Price Density Distribution for {property_type.capitalize()}',
#         labels={'price': 'Price', 'density': 'Density'},
#         color_discrete_sequence=['blue' if property_type == 'house' else 'green'],
#     )
#
# # Customize hover details
# fig.update_traces(hovertemplate='Price: %{x}<br>Density: %{y}')
#
# # Layout adjustments
# fig.update_layout(
#     xaxis_title="Price",
#     yaxis_title="Density",
#     legend_title="Property Type",
#     template="plotly_white",
#     width=800,
#     height=500,
# )
#
# # Display the plot in Streamlit
# st.plotly_chart(fig, use_container_width=True)



# Streamlit Header
st.header('Price vs Density Distribution')

# Sidebar Filters
st.sidebar.header("Filters")
property_types = st.sidebar.multiselect(
    "Select Property Types",
    options=new_df['property_type'].unique().tolist(),
    default=new_df['property_type'].unique().tolist()
)

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=int(new_df['price'].min()),
    max_value=int(new_df['price'].max()),
    value=(int(new_df['price'].min()), int(new_df['price'].max()))
)

# Filter data based on selections
filtered_df = new_df[
    (new_df['property_type'].isin(property_types)) &
    (new_df['price'] >= price_range[0]) &
    (new_df['price'] <= price_range[1])
]

# Display filtered data count
st.write(f"Filtered data includes {len(filtered_df)} properties.")

# Create the interactive plot
fig = px.histogram(
    filtered_df,
    x='price',
    color='property_type',
    nbins=50,
    marginal='violin',  # Adds a violin plot on the side
    histnorm='density',
    title='Interactive Price Density Distribution',
    labels={'price': 'Price', 'density': 'Density'},
    hover_data={'price': ':.2f', 'property_type': True},  # Custom hover formatting
    opacity=0.7,
)

# Add hovertemplate for detailed interaction
fig.update_traces(
    hovertemplate="<b>Price:</b> %{x}<br><b>Density:</b> %{y}<br><b>Type:</b> %{color}"
)

# Customize layout
fig.update_layout(
    xaxis_title="Price",
    yaxis_title="Density",
    legend_title="Property Type",
    template="plotly_white",
    width=900,
    height=600,
)

# Add Range Slider for Interactive Control
fig.update_xaxes(rangeslider_visible=True)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Additional Insights (if data is available)
if not filtered_df.empty:
    avg_price = filtered_df['price'].mean()
    max_price = filtered_df['price'].max()
    min_price = filtered_df['price'].min()
    st.markdown(f"""
    ### Additional Insights:
    - **Average Price:** ₹{avg_price:,.2f}
    - **Max Price:** ₹{max_price:,.2f}
    - **Min Price:** ₹{min_price:,.2f}
    """)
else:
    st.warning("No data available for the selected filters.")

# Advanced Analytics
if not new_df.empty:
    st.write("### Advanced Analytics")

    # # Select only numeric columns for correlation matrix
    # numeric_df = new_df.select_dtypes(include=[np.number])
    #
    # if not numeric_df.empty:
    #     correlation_matrix = numeric_df.corr()
    #     st.write("Correlation Matrix")
    #     st.dataframe(correlation_matrix)
    # else:
    #     st.warning("No numeric data available for correlation analysis.")

    # Download Button for filtered data (ignoring non-numeric columns)
    st.sidebar.subheader("Download Filtered Data")
    csv = new_df.to_csv(index=False)
    st.sidebar.download_button(label="Download CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")
else:
    st.warning("No data available for Advanced Analytics.")
