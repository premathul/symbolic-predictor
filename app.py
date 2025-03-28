import streamlit as st

def compute_detector_grade(time_sec, growth_rate, power_w, output_impurity, net_impurity_added):
    try:
        # New raw-input symbolic regression model
        term1 = (time_sec * output_impurity - power_w) / net_impurity_added
        term2 = growth_rate * 0.87
        DG = term1 + term2

        # Physically constrain output between 0% and 100%
        DG = max(0.0, min(DG, 100.0))

        return round(DG, 3)

    except Exception as e:
        return f"Error: {e}"

# Web app layout
st.set_page_config(page_title="Detector Grade Predictor(Test/Beta)", layout="centered")
st.title("🔬Detector Grade Predictor(Beta)")
st.markdown("This tool predicts the **Detector Grade (%)** crystal growth inputs using a symbolic model trained on raw experimental data. This is a simple test model")

# Input form
with st.form("input_form"):
    time_sec = st.number_input("Time (Sec)", min_value=0.0, value=3600.0)
    growth_rate = st.number_input("Growth Rate (gm/sec)", min_value=0.0, value=0.05)
    power_w = st.number_input("Power (W)", min_value=0.0, value=8700.0)
    output_impurity = st.number_input("Output Net Impurity", value=4.7e11)
    net_impurity_added = st.number_input("No. of Net Impurity Atoms Added", min_value=0.0001, value=3.5e13)
    submitted = st.form_submit_button("🚀 Predict Detector Grade")

if submitted:
    result = compute_detector_grade(
        time_sec,
        growth_rate,
        power_w,
        output_impurity,
        net_impurity_added
    )
    st.success(f"Predicted Detector Grade: **{result} %**")

