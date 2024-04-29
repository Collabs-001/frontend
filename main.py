import requests
import streamlit as st

# Load JSON data from API
try:
    response = requests.get('https://backend-oj59.onrender.com/get')
    response.raise_for_status()  # Raise an exception for bad status codes
    json_data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Error: {e}")
    json_data = None

# Render search form
st.title("Find the Best Jobs")
query_string = st.text_input("Search jobs, companies, positions...")

if st.button("Search"):
    queries = [q.strip() for q in query_string.replace(',', '+').split('+')]

    locations = []
    query_terms = []
    for query in queries:
        if ',' in query:
            locs = [loc.strip() for loc in query.split(',')]
            locations.extend(locs)
        else:
            query_terms.append(query)

    filtered_items = json_data[:]
    for query in query_terms:
        filtered_items = [item for item in filtered_items if any(query.lower() in value.lower() for value in item.values())]
    for loc in locations:
        filtered_items = [item for item in filtered_items if any(loc.lower() in value.lower() for value in item.values())]

    count = len(filtered_items)

    st.subheader(f"Search Results for '{query_string}' - {count} found")

    if filtered_items:
        for result in filtered_items:
            st.markdown(f"**{result['position']} at {result['company']}**", unsafe_allow_html=True)
            st.markdown(result['description'], unsafe_allow_html=True)
            st.markdown(f"Location: {result['location']}")
            st.markdown(f"[More info]({result['url']})")
            st.write("---")
    else:
        st.warning(f"No results found for '{query_string}'")

