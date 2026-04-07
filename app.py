import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Diabetes Prediction", page_icon="", layout="centered")

st.title(" Diabetes Prediction App")
st.markdown("**Model:** `diabetes_model.pkl` (SVC)")

# Load the model
@st.cache_resource
def load_model():
    with open('diabetes_model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

st.subheader("Enter Patient Details")

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.slider("Pregnancies", 0, 17, 3, help="Number of times pregnant")
    glucose = st.slider("Glucose (mg/dL)", 0, 200, 120, help="Plasma glucose concentration")
    bloodpressure = st.slider("Blood Pressure (mm Hg)", 0, 130, 72, help="Diastolic blood pressure")
    skinthickness = st.slider("Skin Thickness (mm)", 0, 100, 29, help="Triceps skin fold thickness")

with col2:
    insulin = st.slider("Insulin (mu U/ml)", 0, 850, 140, help="2-Hour serum insulin")
    bmi = st.slider("BMI (kg/m²)", 0.0, 70.0, 32.4, step=0.1, help="Body Mass Index")
    dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.47, step=0.01, help="Genetic risk score")
    age = st.slider("Age (years)", 0, 120, 33, help="Age of the patient")

if st.button(" Predict Diabetes Risk", type="primary", use_container_width=True):
    # Prepare input for model (exactly 8 features in correct order)
    input_data = np.array([[pregnancies, glucose, bloodpressure, skinthickness, 
                            insulin, bmi, dpf, age]])
    
    # Predict class (0 = No Diabetes, 1 = Diabetes)
    prediction = model.predict(input_data)[0]
    
    # For SVC without probability, we show confidence based on decision function
    decision_score = model.decision_function(input_data)[0]
    
    # Convert decision score to a pseudo-probability (between 0 and 1)
    probability = 1 / (1 + np.exp(-decision_score))   # Sigmoid transformation
    
    st.success(" Prediction Complete!")
    
    if prediction == 1:
        st.error(f" **DIABETIC (Positive)**\n\nProbability ≈ {probability:.1%}")
    else:
        st.success(f"**NOT DIABETIC (Negative)**\n\nProbability of Diabetes ≈ {probability:.1%}")
    
    # Optional: Show raw decision score
    with st.expander("Model Details"):
        st.write(f"**Model Type:** {type(model).__name__}")
        st.write(f"**Decision Score:** {decision_score:.4f}")
        st.caption("Note: Since this is an SVC model, probability is approximated using the decision function.")

st.caption("All features clearly labelled • Predefined sample values can be added via sliders")