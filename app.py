# SEO - Directories Analyzer
# V1 - April 2022
# By Michael Pinatton @michaelpinatton


#import libraries
import streamlit as st
import pandas as pd
from polyfuzz import PolyFuzz
import xlsxwriter
from io import BytesIO
import time

#app config
st.set_page_config(page_title="SEO - URL Similarity", layout="wide")

#header
st.title("SEO - URL Similarity")
st.subheader("Quickly match 2 lists of URL with a similarity score")
st.write("Matching URL can be very useful in SEO !")
st.write("For example: matching old and new pages in case of website migration or finding the best URL to redirect 404 pages.")
st.markdown(
        "Made by [@MichaelPinatton](https://twitter.com/michaelpinatton) with [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/) "
    )


with st.expander("🛠️ -- How to use the app?", expanded=False):
    st.markdown("")
    st.markdown(
        """
1. Upload a first **Excel file** (only 1 column) with the URL to match
2. Upload a second **Excel file** (only 1 column) with the URL to be matched with
3. Download the result file in Excel or CSV format
	    """)
    st.markdown("")
    st.markdown("💡 Tip: For a clearer view, I like to get rid of the host name (https://www.domain.com) and only keep the relative path (/category/blog-post) in the URL list")

with st.expander("🎥 -- Demo", expanded=False):
    st.markdown("")
    st.markdown(
            "Watch the demo here : [DEMO URL](https://www.loom.com/share/f7c16e67ff6d44388c8d9aef111c9b2a)[![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/) "
        )
    st.markdown("")

#upload files
st.subheader('1) Upload your URL list to match')
input_a = st.file_uploader('Upload your URL list to match in Excel format')
st.subheader('2) Upload your URL list to be matched with')
input_b = st.file_uploader('Upload your URL list to be matched with in Excel format')

#script
if input_a is not None and input_b is not None:
    start = time.time()
    url_a = pd.read_excel(input_a)
    url_b = pd.read_excel(input_b)
    url_a.rename(columns={url_a.columns[0]:'url_A'}, inplace=True)
    url_b.rename(columns={url_b.columns[0]:'url_B'}, inplace=True)
    list_a = url_a['url_A'].tolist()
    list_b = url_b['url_B'].tolist()
    model = PolyFuzz('TF-IDF').match(list_a, list_b)
    match = model.get_matches()
    match.sort_values(by='Similarity', ascending=False, inplace=True)
    end = time.time()
    total_time = round(end-start, 3)

    st.success(f"Matching done in {total_time} sec 🎉")

    st.subheader('3) Download your results')



    #EXPORT EXCEL FILE
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    match.to_excel(writer, sheet_name='URL_Similarity', index=False)
    worksheet = writer.sheets['URL_Similarity']
    format_center = workbook.add_format()
    format_center.set_align('center')
    worksheet.set_column('A:B', 80)
    worksheet.set_column('C:C', 15, format_center)
    worksheet.conditional_format('C2:C50000', {'type': '3_color_scale',
                                             'min_color': "#F8696B",
                                              'mid_color': "#FFEB84",
                                             'max_color': "#63BE7B"})
    writer.save()

    st.download_button(
    label="Click to download the Excel file",
    data=output.getvalue(),
    file_name="URL_Similarity.xlsx",
    mime="application/vnd.ms-excel")

    st.markdown("")

    #EXPORT CSV FILE
    def convert_df(df):
       return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(match)

    st.download_button(
       "Click to download the CSV file",
       csv,
       "URL_Similarity.csv",
       "text/csv",
       key='download-csv'
    )

else:
    st.markdown("")
    st.info('☝️ Upload the 2 Excel files')
