import streamlit as st
from PIL import Image
from searcher import Searcher
img = Image.open('assets/kogni-white.jpeg')
st.set_page_config(page_title='Kogni', page_icon=img)
languages_mapping = {
    'en': "English",
    'sv': "Sweedish",
    'de': "German",
    'fr': "French"
}
languages_colours = {
    'en': '#2ECC71',
    'sv': '#2980B9',
    'de': '#E67E22',
    'fr': '#9B59B6'
}
col1, mid, col2 = st.columns([1,3,20])
with col1:
    st.image(img, width=100)
with col2:
    st.write('Welcome to the demo for Kogni!')

search_engine = Searcher.load_models()

query = st.text_area(
    "Search query",
    value="",
)
if st.button("Search"):
    results = Searcher.search(query=query)

    st.success('Search finished successfully.')

    for result in results:
        with st.expander("Results for {}".format(languages_mapping[result['language']])):
            for i in range(5):
                st.markdown("""
                    Document number {} got a matching score of **{:.2f}** and a relevance score of **{:.2f}**.
                    > <p style='background-color: {}'>{}</p>
                """.format(
                    i+1,
                    result['match_score_{}'.format(i+1)],
                    result['relevance_{}'.format(i+1)],
                    languages_colours[result['language']],
                    result['original_content_{}'.format(i+1)]
                ), unsafe_allow_html=True)


else:
    st.write("Enter some text and hit search. The results might surprise you.")

