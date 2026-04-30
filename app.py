import streamlit as st
import pickle
import json

# --- Load Models ---
with open("diabetes_model.pickle", "rb") as f:
    diabetes_model = pickle.load(f)
with open("heart_model.pickle", "rb") as f:
    heart_model = pickle.load(f)
with open("parkinsons_model.pkl", "rb") as f:
    parkinsons_model = pickle.load(f)

# --- Load Columns from JSON and Extract Lists ---
with open("diabetes_columns.json", "r") as f:
    diabetes_columns_dict = json.load(f)
diabetes_columns = diabetes_columns_dict["data_columns"]

with open("heart_columns.json", "r") as f:
    heart_columns_dict = json.load(f)
heart_columns = heart_columns_dict["data_columns"]

with open("parkinsons_columns.json", "r") as f:
    parkinsons_columns_dict = json.load(f)
parkinsons_columns = parkinsons_columns_dict["data_columns"]

# --- Optional: Custom CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception:
        pass
local_css('app_style.css')

# --- Sidebar Navigation ---
st.sidebar.title("Multiple Disease Prediction System")
page = st.sidebar.radio("Choose Prediction", ["Diabetes", "Heart Disease", "Parkinson's"])

# --- Diabetes Form ---
def diabetes_form():
    st.markdown("<h1 style='margin-top:32px;'>Diabetes Prediction using ML</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)
    user_input = {}
    user_input[diabetes_columns[0]] = col1.number_input("Number of Pregnancies", value=None, key="pregnancies")
    user_input[diabetes_columns[1]] = col2.number_input("Glucose Level", value=None, key="glucose")
    user_input[diabetes_columns[2]] = col3.number_input("Blood Pressure", value=None, key="bloodpressure")
    user_input[diabetes_columns[3]] = col4.number_input("Skin Thickness Value", value=None, key="skinthickness")
    user_input[diabetes_columns[4]] = col5.number_input("Insulin Level", value=None, key="insulin")
    user_input[diabetes_columns[5]] = col6.number_input("BMI", value=None, key="bmi")
    user_input[diabetes_columns[6]] = col7.number_input("Diabetes Pedigree Function Value",value=None, key="diabetespedigreefunction")
    user_input[diabetes_columns[7]] = col8.number_input("Age of the person",value=None, key="age")
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("Diabetes Test Result", key="diabetes_submit")
    if submitted:
        if any(user_input[col] is None for col in diabetes_columns):
            st.warning("Fill all the Fields.")
        else:
            features = [user_input[col] for col in diabetes_columns]
            pred = diabetes_model.predict([features])
            result = "Diabetes Detected" if pred[0] == 1 else "No Diabetes"
            st.success(result)

# --- Heart Disease Form ---
def heart_form():
    st.markdown("<h1 style='margin-top:32px;'>Heart Disease Prediction using ML</h1>", unsafe_allow_html=True)
    cols = st.columns(4)
    user_input = {}
    for i, colname in enumerate(heart_columns):
        idx = i % 4
        row = i // 4
        if idx == 0 and i != 0:
            cols = st.columns(4)
        pretty_label = colname.replace("_", " ").replace("cp", "Chest Pain Type").replace("trestbps", "Resting Blood Pressure").replace("chol", "Serum Cholesterol (mg/dl)").replace("fbs", "Fasting Blood Sugar > 120 mg/dl").replace("restecg", "Resting ECG Results").replace("thalach", "Max Heart Rate Achieved").replace("exang", "Exercise Induced Angina").replace("oldpeak", "ST Depression by Exercise").replace("slope", "Slope of Peak Exercise ST Segment").replace("ca", "Major Vessels Colored by Fluoroscopy").replace("thal", "Thal (0=normal;1=fixed defect;2=reversible defect)")
        user_input[colname] = cols[idx].number_input(pretty_label, value=None, key=f"heart_{colname}")
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("Heart Test Result", key="heart_submit")
    if submitted:
        if any(user_input[col] is None for col in heart_columns):
            st.warning("Fill all the Fields.")
        else:
            features = [user_input[col] for col in heart_columns]
            pred = heart_model.predict([features])
            result = "Heart Disease Detected" if pred[0] == 1 else "No Heart Disease"
            st.success(result)

# --- Parkinson's Disease Form ---
def parkinsons_form():
    st.markdown("<h1 style='margin-top:32px;'>Parkinson's Disease Prediction using ML</h1>", unsafe_allow_html=True)
    user_input = {}
    total = len(parkinsons_columns)
    for r in range(0, total, 4):
        cols = st.columns(4)
        for i in range(4):
            if r+i < total:
                colname = parkinsons_columns[r+i]
                pretty_label = colname.replace("mdvp:", "MDVP:").replace("jitter:", "Jitter:").replace("shimmer:", "Shimmer:").replace("(", "").replace(")", "").replace("_", " ")
                user_input[colname] = cols[i].number_input(pretty_label, value=None, key=f"parkinsons_{colname}")
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.button("Parkinson's Test Result", key="parkinsons_submit")
    if submitted:
        if any(user_input[col] is None for col in parkinsons_columns):
            st.warning("Fill all the Fields.")
        else:
            features = [user_input[col] for col in parkinsons_columns]
            pred = parkinsons_model.predict([features])
            result = "Parkinson's Detected" if pred[0] == 1 else "No Parkinson's Disease"
            st.success(result)

# --- Routing ---
if page == "Diabetes":
    diabetes_form()
elif page == "Heart Disease":
    heart_form()
elif page == "Parkinson's":
    parkinsons_form()
