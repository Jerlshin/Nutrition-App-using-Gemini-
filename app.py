import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Sidebar for navigation and inputs
st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to navigate through the app.")
st.sidebar.image("https://clipground.com/images/logos-png-8.png", width=200)


st.sidebar.subheader("Upload an Image")
uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

st.sidebar.subheader("Select a Scenario or Write Your Own Query")
scenarios = {
    "Scenario 1: Weight Loss Journey": """
    A user with a goal to lose weight uses Nutritionist AI to aid in their weight loss journey. 
    With specific dietary preferences and a certain activity level, they input their dietary preferences and health goals into the app. 
    Nutritionist AI creates a calorie-controlled, nutrient-dense meal plan tailored to their diet. 
    The user logs their meals by taking photos or scanning barcodes, and the app provides feedback on their calorie intake 
    and nutritional balance, suggesting necessary adjustments. By syncing their fitness tracker, the app integrates their 
    physical activity data, offering comprehensive insights to help the user stay on track with their weight loss while 
    maintaining proper nutrition.
    """,
    "Scenario 2: Managing Diabetes": """
    A user with Type 2 Diabetes relies on Nutritionist AI to manage their condition through diet. 
    They input their dietary preferences and diabetes condition, and the app generates meal plans that focus 
    on low carbohydrate and high fiber content to help control their blood sugar levels. The user uses the app to log their meals, 
    receiving immediate feedback on their suitability for diabetes management. Detailed nutritional breakdowns 
    highlight carbohydrate content and glycemic index, aiding the user in making informed food choices. Additionally, 
    the app provides educational resources about managing diabetes through diet, keeping the user well-informed and empowered 
    to handle their condition better.
    """,
    "Scenario 3: Building Muscle": """
    A user who is a strength training enthusiast uses Nutritionist AI to support their goal of gaining muscle mass. 
    With a preference for high-protein meals and an intense workout regime, they input their dietary preferences and fitness 
    goals into the app. Nutritionist AI generates meal plans rich in protein and essential nutrients necessary for muscle growth. 
    The user benefits from a variety of high-protein recipes that cater to their needs, with each recipe including detailed 
    instructions and nutritional information. By connecting their fitness tracker, the app accounts for their caloric expenditure 
    and provides insights on balancing their protein intake with their workouts, optimizing their muscle-building efforts.
    """
}

scenario_options = list(scenarios.keys()) + ["Write your own query"]
scenario_choice = st.sidebar.selectbox("Choose a scenario:", scenario_options)

# Main title and description
st.title("Nutritionist AI")
st.markdown("""
**Nutritionist AI** is an innovative mobile application designed to provide personalized dietary recommendations 
and nutritional advice using the advanced capabilities of the **Gemini Pro model**. The app leverages artificial 
intelligence to analyze user data, dietary preferences, and health goals, delivering tailored meal plans, 
nutritional insights, and wellness tips. The primary aim of Nutritionist AI is to promote healthier eating habits 
and improve overall well-being through intelligent and data-driven recommendations.
""")

if scenario_choice == "Write your own query":
    prompt = st.text_area("Enter your query here:")
else:
    prompt = scenarios[scenario_choice]

# Display uploaded image
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # System prompt 
    input_prompt = """
    You are an expert in nutritionist where you need to see the food items from the image
    and estimate approximately the total calories, also provide the details of every food items with calories intake 
    is below format

    1. Item 1 no of calories
    2. Item 2 no of calories
    ----
    ----

    and 
        Answer according to the givin in double quotes. Give your point of view based on the Image input and the Prompt.

    """

    if st.button("Generate Nutrition Advice"):
        with st.spinner('Generating response...'):
            response = model.generate_content([input_prompt, img, prompt])
            st.write("### Nutrition Advice:")
            st.write(response.text)
else:
    st.info("Please upload an image to proceed.")
