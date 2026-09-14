# Import Python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smothies :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

order_name = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be: ", order_name)

# option = st.selectbox("What is your favorite fruit?"
#                       , ('Banana', 'Strawberries', 'Peaches'))

# st.write('Your favourite fuit is: ', option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
# my_dataframe = session.table("smoothies.public.fruit_options").select(col.'FRUIT_NAME')

# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingrediients:'
                                 , my_dataframe
                                 , max_selections = 5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + ingredient)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + order_name + """')
                    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {order_name}!', icon="✅")



