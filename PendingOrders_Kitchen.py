#import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

#App Code
st.title(f":cup_with_straw: Pending Smoothie Orders:cup_with_straw:")
st.write(
    """Orders that need to be filled.
    """)

session = get_active_session()
My_df = session.table("SMOOTHIES.PUBLIC.ORDERS").filter(col('ORDER_FILLED') == 0).collect()
#st.dataframe(data = My_df, use_container_width=True)

if My_df:
    editable_df = st.data_editor(data=My_df)
    submitted = st.button('Submit')
    
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
        st.success("Order(s) updated.", icon= '👍')

else:
    st.success("No Pending Orders", icon= '👍')
