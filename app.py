import streamlit as st

def compute_detector_grade(time_sec, growth_rate, power_w, output_impurity, net_impurity_added):
    T = time_sec
    G = growth_rate
    P = power_w
    O = output_impurity
    N = net_impurity_added

    try:
        # Main equation (simplified symbolic regression)
        numerator1 = (T * O) - (T * N) - ((T / N) * (G - N))
        denominator1 = (N * T) + (O * G) + (P - O - G - 0.858)
        term1 = numerator1 / denominator1

        numerator2 = (O * G) - ((T / N) * (G - N))
        denominator2 = ((T / N) * N) + (O * G) + (0.478 / N)
        term2 = numerator2 / denominator2

        term3 = (T / N) * (G - N)
        term4 = O * G
        term5 = G * 0.992

        detector_grade = term1 + term2 + term3 + term4 + term5
        return round(detector_grade, 3)

    except Exception as e:
        return f"Error: {e}"

# Web app layout
st.set_page_config(page_title="Detector Grade Predictor", layout="centered")
st.title("🔬 Detector Grade Predictor")
st.markdown("This tool predicts the **Detector Grade (%)** from zone refining and crystal growth inputs using a symbolic model.")

# Input form
with st.form("input_form"):
    time_sec = st.number_input("Time (Sec)", min_value=0.0, value=3600.0)
    growth_rate = st.number_input("Growth Rate (gm/sec)", min_value=0.0, value=0.05)
    power_w = st.number_input("Power (W)", min_value=0.0, value=8700.0)
    output_impurity = st.number_input("Output Net Impurity", min_value=0.0, value=4.7e11)
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

