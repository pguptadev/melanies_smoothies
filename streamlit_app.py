#import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

#App Code
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie.
    """)

Order_name = st.text_input('Name on Smoothie:')
st.write('Name on the smoothie will be:',Order_name)

cnx = st.connection("snowflake")
session = cnx.session()

My_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data = My_df, use_container_width=True)
pd_df = My_df.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose upto 5 engrediants:'
    ,My_df
    ,max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit,'SEARCH_ON'].iloc[0]
        st.write('The search value for ',each_fruit,' is ',search_on,'.')

        st.subheader(each_fruit + ' Nutrition Information')
        response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        sf_df = st.dataframe(data=response.json(),use_container_width=True)
            
    #st.write(ingredients_string)

    insert_stmt = """insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,NAME_ON_ORDER) 
    values('""" + ingredients_string + """', '""" + Order_name + """')"""

    #st.write(insert_stmt)
        
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {Order_name} !", icon="✅")
