import streamlit as st
import pandas as pd
import requests


products_df = pd.read_csv("metadata/products.csv")


API_URL = "http://127.0.0.1:5000/recommend"


st.title("🧴 Sephora Skincare Recommender")
st.write("Select a product category and get personalized recommendations!")


categories = products_df["primary_category"].dropna().unique()
selected_category = st.selectbox("Select a category:", sorted(categories))


filtered_products = products_df[products_df["primary_category"] == selected_category]


product_name = st.selectbox("Choose a product:", filtered_products["product_name"].unique())


product_id = filtered_products.loc[filtered_products["product_name"] == product_name, "product_id"].values[0]


num_recommendations = st.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)


if st.button("Get Recommendations"):
    params = {"product_id": product_id, "num_recommendations": num_recommendations}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        recommendations = response.json()["recommendations"]
        
        if recommendations:
            st.write("### Recommended Products:")
            recommendations_df = pd.DataFrame(recommendations)
            st.table(recommendations_df)
        else:
            st.write("No recommendations found.")
    else:
        st.write("Error fetching recommendations. Please check the product ID.")