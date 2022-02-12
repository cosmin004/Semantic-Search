import streamlit as st
from PIL import Image
from searcher import Searcher
icon = Image.open('assets/favicon.ico')
st.set_page_config(page_title='Kogni', page_icon=icon)
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

img = Image.open('assets/logo.png')
col1, mid, col2 = st.columns([1,3,20])
with col1:
    st.image(img, width=100)
with col2:
    st.write('Welcome to the demo for Kogni!')

search_engine = Searcher.load_models()

search_db = st.sidebar.selectbox(
    label='Select a folder to search in 📁', 
    options=(
        '📂 International contracts',
        '📂 Civil codes multiple languages',
        '📂 Technical documentation'
    )
)
# 128193	1F4C1	
# 128194	1F4C2	

results_num = st.sidebar.slider(
    label='Number of documents to return from the query', 
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

print(search_db)
print(results_num)

query = st.text_area(
    "Search query",
    value="",
)
if st.button("Search 🔎"):
    results = Searcher.search(
        query=query,
        db = search_db,
        topk = results_num
    )

    st.success('Search finished successfully. 💪🏻')

    for result in results:
        if 'language' in result:
            with st.expander("Results for {}".format(languages_mapping[result['language']])):
                for i in range(results_num):
                    st.markdown("""
                        Document number {} got a matching score of **{:.2f}** and a relevance score of **{:.2f}**.
                        > <p style='background-color: {}'>{}</p>
                    """.format(
                        i+1,
                        result['match_score_{}'.format(i+1)],
                        result['relevance_{}'.format(i+1)],
                        languages_colours[result['language']],
                        result['original_content_{}'.format(i+1)].replace('<', '').replace('>', '')
                    ), unsafe_allow_html=True)
        else:
            for i in range(results_num):
                if "page_{}".format(i+1) in result:
                    content = "{} at page {} got a matching score of {:.2f} and a relevance score of {:.2f}".format(
                        result['document_{}'.format(i+1)],
                        result['page_{}'.format(i+1)],
                        result['match_score_{}'.format(i+1)],
                        result['relevance_{}'.format(i+1)],
                    )
                else:
                    content = "{} got a matching score of {:.2f} and a relevance score of {:.2f}".format(
                        result['document_{}'.format(i+1)],
                        result['match_score_{}'.format(i+1)],
                        result['relevance_{}'.format(i+1)],
                    )
                with st.expander(content):
                    st.markdown("""
                        > {}
                    """.format(
                        result['content_{}'.format(i+1)].replace('<', '').replace('>', '')
                    ), unsafe_allow_html=True)


else:
    st.write("Enter some text and hit search. The results might surprise you.")

