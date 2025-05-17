# Import Python packages
from snowflake.snowpark.functions import col, when_matched
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write("Choose the fruits that you want in your custom Smoothie!")

title = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", title)

# Get Snowflake session
cnx=st.connected("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name')).to_pandas()

# Convert DataFrame column to list
fruit_list = my_dataframe['FRUIT_NAME'].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Properly format ingredients

    # Display SQL statement for debugging
    st.write(f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{title}')")

    # Submit order button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql("INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)", 
                    [ingredients_string, title]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


