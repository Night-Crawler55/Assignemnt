import requests
import streamlit as st

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"


def fetch_data(api_url):
    responses = []
    page = 1
    total_pages = 1
    while True:
        response = requests.get(api_url, params={'page': page})
        data = response.json()
        if not data:
            break
        responses.extend(data)
        page += 1
        total_pages = page
    return responses, total_pages


def find_citations(responses):
    results = []
    for item in responses:
        response_text = item['response']
        sources = item['source']
        citations = []
        for source in sources:
            if source['context'] in response_text:
                citations.append({"id": source["id"], "link": source["link"]})
        results.append({"response": response_text, "citations": citations})
    return results


def main():
    st.title("API Response Citation Finder")

    # Fetch data with a progress bar
    st.write("Fetching data from API...")
    progress_bar = st.progress(0)
    responses = []
    total_pages = 1

    try:
        responses, total_pages = fetch_data(API_URL)
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return

    progress_bar.progress(1.0)  # Set progress to 100% after data fetch is complete
    st.write("Data fetched successfully.")

    # Process data with a progress bar
    st.write("Processing data to find citations...")
    citations = []
    total_responses = len(responses)
    progress_bar = st.progress(0)

    for i, item in enumerate(responses):
        response_text = item['response']
        sources = item['source']
        item_citations = []
        for source in sources:
            if source['context'] in response_text:
                item_citations.append({"id": source["id"], "link": source["link"]})
        citations.append({"response": response_text, "citations": item_citations})
        progress_bar.progress((i + 1) / total_responses)

    st.write("Data processed successfully.")

    # Display the results
    st.write("## Results")
    for item in citations:
        st.write(f"**Response:** {item['response']}")
        st.write("**Citations:**")
        for citation in item['citations']:
            st.write(f"- ID: {citation['id']}, Link: {citation['link']}")
        st.write("---")


if __name__ == "__main__":
    main()
