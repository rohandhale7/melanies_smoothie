# Import Python packages
from snowflake.snowpark.functions import col, when_matched
import streamlit as st
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write("Choose the fruits that you want in your custom Smoothie!")

title = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", title)

# Get Snowflake session
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('Search_on'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# Convert DataFrame column to list
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    
    st.subheader(fruit_chosen + 'Nutrition Information')
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/" + search_on)
    fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

# Display SQL statement for debugging
st.write(f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{title}')")
# Submit order button
time_to_insert = st.button('Submit Order')

if time_to_insert:
   session.sql("INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)", 
                [ingredients_string, title]).collect()
   st.success('Your Smoothie is ordered!', icon="✅")
