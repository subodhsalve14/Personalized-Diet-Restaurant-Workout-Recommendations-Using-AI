import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
import re
from dotenv import load_dotenv

# --- CORE LOGIC (No changes here) ---

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama3-70b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.0
    )

prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template=(
        "Diet Recommendation System:\n"
        "I want you to provide output in the following format using the input criteria:\n\n"
        "Restaurants:\n- name1\n- name2\n- name3\n- name4\n- name5\n\n"
        "Breakfast:\n- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Dinner:\n- item1\n- item2\n- item3\n- item4\n- item5\n\n"
        "Workouts:\n- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n\n"
        "Criteria:\nAge: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
        "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
        "Allergics: {allergics}, Food Preference: {foodtype}.\n"
    )
)

def clean_list(block):
    cleaned_lines = []
    for line in block.strip().split("\n"):
        cleaned_line = line.strip("- *• ") 
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    return cleaned_lines

# --- NEW: PROFESSIONAL TWO-COLUMN UI ---

st.set_page_config(page_title="NutriNavigator", page_icon="🍽️", layout="wide")

st.title("🍽️ NutriNavigator: Your AI Health Assistant")

# NEW: Create a two-column layout. Adjust the ratio as needed.
left_column, right_column = st.columns([2, 3])

# --- LEFT COLUMN for Inputs ---
with left_column:
    st.header("👤 Your Details")
    with st.form("recommendation_form"):
        age = st.slider("Age", 1, 120, 25)
        height = st.slider("Height (ft)", 1.0, 8.0, 6.0, 0.1)
        weight = st.slider("Weight (kg)", 10.0, 300.0, 70.0, 0.5)
        gender = st.selectbox("Gender", ("Male", "Female"))
        veg_or_nonveg = st.selectbox("Dietary Preference", ("Veg", "Non-Veg"))
        
        st.write("---") # Visual separator
        
        disease = st.text_input("Any existing diseases?", "None")
        region = st.text_input("Region (e.g., Kalyan, India)", "Kalyan, India")
        allergics = st.text_input("Any allergies?", "None")
        foodtype = st.text_input("Food Type (e.g., Indian, Italian)", "Indian")
        
        submit_button = st.form_submit_button("🍱 Get Recommendations", use_container_width=True)

# --- RIGHT COLUMN for Outputs ---
with right_column:
    if submit_button:
        with st.spinner("🧠 Your AI assistant is thinking..."):
            llm = get_llm()
            chain = LLMChain(llm=llm, prompt=prompt_template_resto)
            
            input_data = {
                'age': age, 'gender': gender.lower(), 'weight': weight, 'height': height,
                'veg_or_nonveg': veg_or_nonveg.lower(), 'disease': disease, 'region': region,
                'allergics': allergics, 'foodtype': foodtype
            }
            
            results = chain.run(input_data)
            
            restaurant_names = re.findall(r'Restaurants:\s*(.*?)\n\n', results, re.DOTALL)
            breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
            dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
            workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)
            
            restaurant_list = clean_list(restaurant_names[0]) if restaurant_names else []
            breakfast_list = clean_list(breakfast_names[0]) if breakfast_names else []
            dinner_list = clean_list(dinner_names[0]) if dinner_names else []
            workout_list = clean_list(workout_names[0]) if workout_names else []

        st.success("Here are your personalized recommendations!")
        st.balloons()
        
        tab1, tab2, tab3 = st.tabs(["🍴 Restaurants", "🥗 Meals", "💪 Workouts"])

        with tab1:
            st.header("Recommended Restaurants in " + region)
            for item in restaurant_list:
                with st.container(border=True):
                    st.write(f"**🍽️ {item}**")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("☀️ Breakfast")
                for item in breakfast_list:
                    with st.container(border=True):
                        st.write(f"**🥞 {item}**")
            with col2:
                st.subheader("🌙 Dinner")
                for item in dinner_list:
                    with st.container(border=True):
                        st.write(f"**🍲 {item}**")

        with tab3:
            st.header("Recommended Workouts")
            for item in workout_list:
                with st.container(border=True):
                    st.write(f"**🏋️ {item}**")
    else:
        # NEW: Show a placeholder message before submission
        st.info("Your personalized recommendations will appear here once you submit your details.")


# EARLIER CODE

# import streamlit as st
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain_groq import ChatGroq
# import os
# import re
# from dotenv import load_dotenv

# # --- CORE LOGIC (No changes here) ---

# load_dotenv()

# def get_llm():
#     return ChatGroq(
#         model="llama3-70b-8192",
#         groq_api_key=os.getenv("GROQ_API_KEY"),
#         temperature=0.0
#     )

# prompt_template_resto = PromptTemplate(
#     input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
#     template=(
#         "Diet Recommendation System:\n"
#         "I want you to provide output in the following format using the input criteria:\n\n"
#         "Restaurants:\n- name1\n- name2\n- name3\n- name4\n- name5\n\n"
#         "Breakfast:\n- item1\n- item2\n- item3\n- item4\n- item5\n\n"
#         "Dinner:\n- item1\n- item2\n- item3\n- item4\n- item5\n\n"
#         "Workouts:\n- workout1\n- workout2\n- workout3\n- workout4\n- workout5\n\n"
#         "Criteria:\nAge: {age}, Gender: {gender}, Weight: {weight} kg, Height: {height} ft, "
#         "Vegetarian: {veg_or_nonveg}, Disease: {disease}, Region: {region}, "
#         "Allergics: {allergics}, Food Preference: {foodtype}.\n"
#     )
# )

# # --- Replace this function in your streamlit_app.py ---

# def clean_list(block):
#     cleaned_lines = []
#     for line in block.strip().split("\n"):
#         # First, strip away any bullet characters and whitespace
#         cleaned_line = line.strip("- *• ") 
        
#         # THEN, check if there's any actual content left
#         if cleaned_line:
#             cleaned_lines.append(cleaned_line)
            
#     return cleaned_lines

# # --- NEW FORM-BASED UI ---

# st.set_page_config(page_title="NutriNavigator", page_icon="🍽️", layout="centered")

# st.title("🍽️ NutriNavigator: Your AI Health Assistant")
# st.write("Fill in your details in the form below to get your personalized plan.")

# # NEW: Use an expander to create a collapsible form section
# with st.expander("📝 Enter Your Details", expanded=True):
#     # NEW: Use a form on the main page
#     with st.form("recommendation_form"):
#         st.subheader("Personal Information")
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.slider("Age", 1, 120, 25)
#             weight = st.slider("Weight (kg)", 10.0, 300.0, 70.0, 0.5)
#             veg_or_nonveg = st.selectbox("Dietary Preference", ("Veg", "Non-Veg"))
            
#         with col2:
#             gender = st.selectbox("Gender", ("Male", "Female"))
#             height = st.slider("Height (ft)", 1.0, 8.0, 6.0, 0.1)
            
#         st.subheader("Additional Info")
#         disease = st.text_input("Any existing diseases?", "None")
#         region = st.text_input("Region (e.g., Mumbai, India)", "Mumbai, India")
#         allergics = st.text_input("Any allergies?", "None")
#         foodtype = st.text_input("Food Type (e.g., Indian, Italian)", "Indian")
        
#         submit_button = st.form_submit_button("🍱 Get Recommendations", use_container_width=True)

# # This block runs only when the form is submitted
# if submit_button:
#     with st.spinner("🧠 Your AI assistant is thinking..."):
#         llm = get_llm()
#         chain = LLMChain(llm=llm, prompt=prompt_template_resto)
        
#         input_data = {
#             'age': age, 'gender': gender.lower(), 'weight': weight, 'height': height,
#             'veg_or_nonveg': veg_or_nonveg.lower(), 'disease': disease, 'region': region,
#             'allergics': allergics, 'foodtype': foodtype
#         }
        
#         results = chain.run(input_data)
        
#         restaurant_names = re.findall(r'Restaurants:\s*(.*?)\n\n', results, re.DOTALL)
#         breakfast_names = re.findall(r'Breakfast:\s*(.*?)\n\n', results, re.DOTALL)
#         dinner_names = re.findall(r'Dinner:\s*(.*?)\n\n', results, re.DOTALL)
#         workout_names = re.findall(r'Workouts:\s*(.*?)\n\n', results, re.DOTALL)
        
#         restaurant_list = clean_list(restaurant_names[0]) if restaurant_names else []
#         breakfast_list = clean_list(breakfast_names[0]) if breakfast_names else []
#         dinner_list = clean_list(dinner_names[0]) if dinner_names else []
#         workout_list = clean_list(workout_names[0]) if workout_names else []

#     st.success("Here are your personalized recommendations!")
#     st.balloons()
    
#     # The clean, tabbed output remains the same
#     tab1, tab2, tab3 = st.tabs(["🍴 Restaurants", "🥗 Meals", "💪 Workouts"])

#     with tab1:
#         st.header("Recommended Restaurants")
#         for item in restaurant_list:
#             st.markdown(f"• {item}")

#     with tab2:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("☀️ Breakfast")
#             for item in breakfast_list:
#                 st.markdown(f"• {item}")
#         with col2:
#             st.subheader("🌙 Dinner")
#             for item in dinner_list:
#                 st.markdown(f"• {item}")

#     with tab3:
#         st.header("Recommended Workouts")
#         for item in workout_list:
#             st.markdown(f"• {item}")


