import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import base64

# Streamlit page configuration
st.set_page_config(page_title="Data Collection App", layout="wide")

# Hiding the header of Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Background image function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        base64_img = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_img}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


add_bg_from_local("photo.jpg")

# Sidebar for graph options
graph_options = ["Home", "Bar graph", "Line graph", "Pie chart"]
selected_graph = st.sidebar.selectbox("Graphs", graph_options)


# Function to plot graphs
def plot_graph(graph_type, data):
    if graph_type == "Bar graph":
        st.bar_chart(data["Favorite Animal"].value_counts())
    elif graph_type == "Line graph":
        st.line_chart(data["Favorite Animal"].value_counts())
    elif graph_type == "Pie chart":
        plt.figure(figsize=(5, 5))
        plt.pie(
            data["Favorite Animal"].value_counts(),
            labels=data["Favorite Animal"].value_counts().index,
            autopct="%1.1f%%",
        )
        st.pyplot(plt)


# Main application page
if selected_graph == "Home":
    st.title("EcoCAR FORM")

    # Streamlit form
    with st.form("data_form"):
        st.header("Please enter your details:")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        favorite_animal = st.selectbox(
            "Favorite Animal",
            ["Bird", "T-rex", "Pikachu", "Cat", "Dog", "Fish", "Chicken"],
        )
        submitted = st.form_submit_button("Submit")

    # Dataframe handling
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(
            columns=["First Name", "Last Name", "Favorite Animal"]
        )

    if submitted:
        new_data = pd.DataFrame(
            {
                "First Name": [first_name],
                "Last Name": [last_name],
                "Favorite Animal": [favorite_animal],
            }
        )
        st.session_state.data = pd.concat(
            [st.session_state.data, new_data], ignore_index=True
        )

    # Display dataframe only if there is at least one entry
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data)

# Graph pages
else:
    if not st.session_state.data.empty:
        plot_graph(selected_graph, st.session_state.data)
    else:
        st.write(
            "No data available to display the graph. Please add some data in the Home page."
        )
