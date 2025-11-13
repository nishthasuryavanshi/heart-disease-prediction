import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open('lr_model3.pkl', 'rb'))

# App title
st.title("❤️ Heart Disease Prediction App")
st.markdown("Enter your health details below to check your risk of heart disease.")

# --- Input Fields (Real-World Friendly) ---
HighBP = st.radio("Do you have high blood pressure?", ("Yes", "No"))
HighChol = st.radio("Do you have high cholesterol?", ("Yes", "No"))
CholCheck = st.radio("Have you done a cholesterol check in the last 5 years?", ("Yes", "No"))
BMI = st.number_input("Enter your Body Mass Index (BMI)", min_value=10.0, max_value=60.0, step=0.1)
Smoker = st.radio("Have you smoked at least 100 cigarettes in your life?", ("Yes", "No"))
Stroke = st.radio("Have you ever had a stroke?", ("Yes", "No"))
Diabetes = st.selectbox("Do you have diabetes?", 
                        ["No", "Yes", "Borderline Diabetes", "During Pregnancy"])
PhysActivity = st.radio("Did you have any physical activity in the past 30 days (excluding job)?", ("Yes", "No"))
HvyAlcoholConsump = st.radio("Do you consume alcohol heavily (14+ drinks/week for men or 7+ for women)?", ("Yes", "No"))
MentHlth = st.slider("Days your mental health was not good (last 30 days)", 0, 30, 0)
PhysHlth = st.slider("Days your physical health was not good (last 30 days)", 0, 30, 0)
Sex = st.radio("Select your sex:", ("Male", "Female"))
Age = st.selectbox("Select your age group:",
                   ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
                    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
Education = st.selectbox("Select your education level:",
                         ["Never attended school", "Elementary", "Some high school",
                          "High school graduate", "Some college", "College graduate"])
Income = st.selectbox("Select your income range:",
                      ["Less than $10,000", "$10,000–$15,000", "$15,000–$20,000", "$20,000–$25,000",
                       "$25,000–$35,000", "$35,000–$50,000", "$50,000–$75,000", "$75,000 or more"])

# --- Convert to numeric format for the model ---
def encode_inputs():
    return [
        1 if HighBP == "Yes" else 0,
        1 if HighChol == "Yes" else 0,
        1 if CholCheck == "Yes" else 0,
        BMI,
        1 if Smoker == "Yes" else 0,
        1 if Stroke == "Yes" else 0,
        {"No": 0, "Yes": 1, "Borderline Diabetes": 2, "During Pregnancy": 3}[Diabetes],
        1 if PhysActivity == "Yes" else 0,
        1 if HvyAlcoholConsump == "Yes" else 0,
        MentHlth,
        PhysHlth,
        1 if Sex == "Male" else 0,
        ["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64",
         "65-69","70-74","75-79","80 or older"].index(Age) + 1,
        ["Never attended school","Elementary","Some high school","High school graduate",
         "Some college","College graduate"].index(Education) + 1,
        ["Less than $10,000", "$10,000–$15,000", "$15,000–$20,000", "$20,000–$25,000",
         "$25,000–$35,000", "$35,000–$50,000", "$50,000–$75,000", "$75,000 or more"].index(Income) + 1
    ]

# Prepare input data
if st.button("🔍 Predict"):
    input_data = pd.DataFrame([encode_inputs()],
        columns=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                 'Diabetes', 'PhysActivity', 'HvyAlcoholConsump', 'MentHlth',
                 'PhysHlth', 'Sex', 'Age', 'Education', 'Income'])
    
    prediction = model.predict(input_data)[0]

    st.subheader("📊 Prediction Result:")
    if prediction == 1:
        st.error("🚨 High Risk: The person is likely to have heart disease. Please consult a doctor.")
    else:
        st.success("✅ Low Risk: The person is unlikely to have heart disease. Stay healthy and active!")
