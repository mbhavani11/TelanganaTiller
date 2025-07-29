import streamlit as st
import pandas as pd
import os
import altair as alt

# Page config
st.set_page_config(page_title="TelanganaTiller 🌾", layout="wide")

st.title("🌾 TelanganaTiller - Regional Farming Wisdom and Data Explorer")
st.markdown("Explore district-wise crop data, traditional wisdom, and production trends in Telangana.")

# Load data
@st.cache_data
def load_data():
    file_path = os.path.join("data", "telangana_crops.csv")
    return pd.read_csv(file_path)

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")
    districts = st.multiselect("Select District(s)", df["District"].unique())
    crops = st.multiselect("Select Crop(s)", df["Crop"].unique())
    seasons = st.multiselect("Select Season(s)", df["Season"].unique())

# Apply filters
filtered_df = df.copy()
if districts:
    filtered_df = filtered_df[filtered_df["District"].isin(districts)]
if crops:
    filtered_df = filtered_df[filtered_df["Crop"].isin(crops)]
if seasons:
    filtered_df = filtered_df[filtered_df["Season"].isin(seasons)]

# Show filtered data
st.subheader("📊 Crop Data Overview")
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("📈 Production by Crop")

if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("Crop", sort='-y'),
        y="Production(Tonnes)",
        color="District",
        tooltip=["District", "Crop", "Production(Tonnes)"]
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("No data to display for the selected filters.")

# Traditional Wisdom Section
st.subheader("📚 Regional Farming Wisdom")

farming_wisdom = {
    "Adilabad": "Maize is intercropped with legumes for natural nitrogen fixation.",
    "Bhadradri Kothagudem": "Sugarcane farmers rely on traditional flood irrigation.",
    "Hyderabad": "Urban gardeners use recycled containers and rooftop beds for leafy greens.",
    "Jagtial": "Paddy farmers use tank silt and cattle compost to enrich soil before sowing.",
    "Jangaon": "Vegetable growers rotate crops with green gram to restore nutrients.",
    "Jayashankar Bhupalapally": "Cotton is grown with turmeric for mutual pest resistance.",
    "Jogulamba Gadwal": "Pulses are intercropped with castor to reduce water demand.",
    "Kamareddy": "Maize sowing aligns with local rainfall predictions and bird activity.",
    "Karimnagar": "Cotton farmers apply neem oil for pest control, avoiding chemicals.",
    "Khammam": "Chilli growers use ash and cow dung to protect young plants.",
    "Komaram Bheem Asifabad": "Red gram and millet rotation helps preserve soil in hilly terrain.",
    "Mahabubabad": "Farmers conserve forest-edge moisture using ridge planting.",
    "Mahbubnagar": "Groundnut is often grown post-monsoon using residual soil moisture.",
    "Mancherial": "Cotton and maize fields are irrigated using age-old tank systems.",
    "Medak": "Jowar fields are rotated with pulses to improve fertility.",
    "Medchal–Malkajgiri": "Urban farmers favor hydroponics and terrace crops for space efficiency.",
    "Mulugu": "Tribal farming includes mixed cropping of turmeric, pulses, and minor millets.",
    "Nagarkurnool": "Millet and pulse systems thrive using low-input dryland techniques.",
    "Nalgonda": "Paddy growers follow moon phases to schedule transplanting.",
    "Narayanpet": "Cotton and pulses follow contour trenching for water conservation.",
    "Nirmal": "Farmers use turmeric as a natural insect barrier in mixed gardens.",
    "Nizamabad": "Sugarcane and paddy are rotated with pulses to restore soil balance.",
    "Peddapalli": "Vegetables are grown with native compost piles and greywater reuse.",
    "Rajanna Sircilla": "Turmeric growers ferment cattle dung for fungal disease prevention.",
    "Ranga Reddy": "Dairy-linked farming combines fodder crops with vegetable gardens.",
    "Sangareddy": "Rainfed cotton is alternated with legumes to reduce input dependency.",
    "Siddipet": "Floriculture integrates marigold and chrysanthemum with pest-trapping plants.",
    "Suryapet": "Horticulture farmers mulch with sugarcane trash to reduce evaporation.",
    "Vikarabad": "Millets are preserved using seed exchange festivals and organic sprays.",
    "Wanaparthy": "Millet farming relies on low-input traditional drought-resistant varieties.",
    "Warangal Rural": "Intercropping paddy with green manure crops is a common practice.",
    "Warangal Urban": "Urban growers integrate compost pits with floriculture beds.",
    "Yadadri Bhuvanagiri": "Floriculture fields are pollinator-friendly and avoid synthetic sprays."
}

selected_district = st.selectbox("Select a district to learn traditional wisdom", df["District"].unique())
tip = farming_wisdom.get(selected_district, "Traditional wisdom data not available for this district.")
st.info(f"**{selected_district} Wisdom:** {tip}")

