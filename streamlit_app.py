# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title("Zena's Amazing Athleisure Catalog")


session = get_active_session()
my_dataframe = session.table("zenas_athleisure_db.products.catalog_for_website").select(col('COLOR_OR_STYLE')).collect()
# st.dataframe(data=my_dataframe, use_container_width=True)

styles = [row['COLOR_OR_STYLE'] for row in my_dataframe]

sweatsuit_selected = st.selectbox(
    "Pick a sweatsuit color or style:",
    (styles)
)

# st.stop()


if sweatsuit_selected:
    df_sweatsuit = session.table("zenas_athleisure_db.products.catalog_for_website").filter(col('COLOR_OR_STYLE')== sweatsuit_selected)

    
    # Convert to Pandas DataFrame for Streamlit display
    df_pd = df_sweatsuit.to_pandas()
    # st.dataframe(df_pd)

    image_path = df_pd["FILE_NAME"][0]
    image=session.file.get_stream(f"@zenas_athleisure_db.products.SWEATSUITS/{image_path}" , decompress=False).read()
    
    # Display the image
    st.image(image)
    

    st.write('Price: ', df_pd["PRICE"][0])
    st.write('Size available: ', df_pd["SIZE_LIST"][0])
    st.write('BONUS: ', df_pd["UPSELL_PRODUCT_DESC"][0])




    
