import streamlit as st
import json

# Load the JSON data
with open("./data/youssef/json.json", "r") as file:
    data = json.load(file)
items = data["items"]

st.set_page_config(page_title="Nature Inclusive Measures", layout='wide', initial_sidebar_state="expanded")

# Sidebar filters for Category and Target Group
st.sidebar.header("Filter Options")
available_categories = list(set([item["categories"] for item in items]))
available_target_groups = list(set([group for item in items if "Target group" in item for group in item["Target group"]]))

selected_category = st.sidebar.selectbox("Select Category", ["All"] + available_categories)
selected_target_group = st.sidebar.selectbox("Select Target Group", ["All"] + available_target_groups)

# Filter items based on selected category and target group
filtered_items = [
    item for item in items
    if (selected_category == "All" or item["categories"] == selected_category) and
       (selected_target_group == "All" or selected_target_group in item.get("Target group", []))  # Safely handle missing "Target group" key
]

# Initialize session state to track the selected item
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

# Display header and information section
st.header("📋 Nature Inclusive Measures")
st.info("Select an item from the grid below to see its details displayed at the top.")

st.markdown("""
    <div style="background-color: #FFF3CD; padding: 1rem; border-radius: 5px; color: #856404; font-size: 1rem;">
        <strong>For more information on nature inclusive measures, discover the NEST inclusive platform.</strong>
        <br>
        <a href="https://natuurinclusiefontwikkelen.nl/" target="_blank" style="color: #856404; text-decoration: underline;">
            Explore actions you can take!
        </a>
        <br>   
        <a href="https://nestnatuurinclusief.nl/referenties/" target="_blank" style="color: #856404; text-decoration: underline;">
            Explore NEST projects!
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid gray;'>", unsafe_allow_html=True)

# Display the selected item details above the grid if an item is selected
if st.session_state.selected_item:
    selected_item = st.session_state.selected_item
    st.markdown("<hr style='border:1px solid gray;'>", unsafe_allow_html=True)
    st.header("Selected: " + selected_item["name"])

    # Sections
    st.subheader("Description")
    for section in selected_item["sections"]:
        if section['header'].strip():  # Only display the header if it's not empty or just whitespace
            st.write(f"*{section['header']}*") 
        st.write(section["text"])  # Always display the text

    # Guidelines
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.subheader("Guidelines")
    for guideline in selected_item["guidelines"]["options"]:
        st.write(f"*{guideline['title']}*")
        st.write(guideline["text"])

# Display grid layout of items
for i in range(0, len(filtered_items), 4):  # Loop through items with a step of 4 (one row per loop)
    cols = st.columns(4)  # Create exactly 4 columns per row
    for j, item in enumerate(filtered_items[i:i+4]):  # Populate the row with up to 4 items
        with cols[j]:
            # Display the image in the column, ensuring a consistent size
            st.image(item["image"], use_column_width=True)

            # Display the name of the item as a button
            if st.button(item["name"], key=item["name"]):
                st.session_state.selected_item = item  # Store selected item in session state
