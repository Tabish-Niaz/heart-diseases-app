import streamlit as st
import pandas as pd
import pickle

# 1. Page ki Setting
st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Bottom-right Creator Badge aur Icons ko hide karne ke liye */
            [class^="viewerBadge_container"] {display: none !important;}
            [class^="styles_viewerBadge"] {display: none !important;}
            [class^="viewerBadge_link"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Model Load karna
try:
    with open('heart_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("⚠️ Error: 'heart_model.pkl' file not found! First, save the model from your notebook and place it in the same folder as app.py.")
    st.stop()

# 3. App ka Title aur Description
st.title("❤️ Heart Disease Prediction App")
st.markdown("Enter your medical details here and check whether you are at risk of heart disease or not.")
st.markdown("---")

# 4. Input Fields
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("1. Age ", min_value=1, max_value=120, value=50)
    sex = st.selectbox("2. Sex ", options=[1, 0], format_func=lambda x: "Male (1)" if x==1 else "Female (0)")
    cp = st.selectbox("3. Chest Pain Type (cp)", options=[0, 1, 2, 3])
    trestbps = st.number_input("4. Resting Blood Pressure (trestbps)", min_value=50, max_value=250, value=120)
    chol = st.number_input("5. Cholesterol (chol)", min_value=100, max_value=600, value=200)

with col2:
    fbs = st.selectbox("6. Fasting Blood Sugar > 120 (fbs)", options=[1, 0], format_func=lambda x: "True (1)" if x==1 else "False (0)")
    restecg = st.selectbox("7. Resting ECG (restecg)", options=[0, 1, 2])
    thalach = st.number_input("8. Max Heart Rate Achieved (thalach)", min_value=60, max_value=250, value=150)
    exang = st.selectbox("9. Exercise Induced Angina (exang)", options=[1, 0], format_func=lambda x: "Yes (1)" if x==1 else "No (0)")

with col3:
    oldpeak = st.number_input("10. ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    slope = st.selectbox("11. Slope of ST Segment (slope)", options=[0, 1, 2])
    ca = st.selectbox("12. Number of Major Vessels (ca)", options=[0, 1, 2, 3, 4])
    thal = st.selectbox("13. Thalassemia (thal)", options=[0, 1, 2, 3])

st.markdown("---")

# 5. Prediction Button aur Logic
if st.button("Predict Heart Disease", type="primary"):
    
    # Feature names exactly dataset waley hone chahiye
    feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                     'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    
    # DataFrame banana taake Scikit-Learn warning na de
    user_input = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, 
                                thalach, exang, oldpeak, slope, ca, thal]], 
                              columns=feature_names)
    
    # Model se output nikalna
    prediction = model.predict(user_input)
    
    # Nateeja (Result) dikhana
    if prediction[0] == 0:
        st.error("⚠️ **Result:** According to the model, you may be at risk of heart disease. Please consult a doctor (cardiologist) for a checkup.")
    else:
        st.success("✅ **Result:** According to the model, your heart appears to be healthy. There is no indication of heart disease risk!")
