]import streamlit as st

def compute_detector_grade(time_sec, growth_rate, power_w, output_impurity, net_impurity_added):
    T = time_sec
    G = growth_rate
    P = power_w
    O = output_impurity
    N = net_impurity_added

    try:
        # First term
        numerator1 = (T * O) - (T * N) - ((T / N) * (G - N))
        denominator1 = (N * T) + (O * G) + (P - O - G - 0.858)
        term1 = numerator1 / denominator1

        # Second term
        numerator2 = (O * G) - ((T / N) * (G - N))
        denominator2 = ((T / N) * N) + (O * G) + (0.478 / N)
        term2 = numerator2 / denominator2

        # Additional terms
        term3 = (T / N) * (G - N)
        term4 = O * G
        term5 = G * 0.992

        DG = term1 + term2 + term3 + term4 + term5
        return round(DG, 3)
    
    except Exception as e:
        return f"Error: {e}"

st.title("Detector Grade Predictor")
st.write("Enter experimental values to estimate Detector Grade (%)")

# Input fields
time_sec = st.number_input("Time (Sec)", min_value=0.0)
growth_rate = st.number_input("Growth Rate (gm/sec)", min_value=0.0)
power_w = st.number_input("Power (W)", min_value=0.0)
output_impurity = st.number_input("Output Net Impurity", min_value=0.0)
net_impurity_added = st.number_input("No. of Net Impurity Atoms Added", min_value=0.0001)

if st.button("Predict Detector Grade"):
    result = compute_detector_grade(
        time_sec, growth_rate, power_w, output_impurity, net_impurity_added
    )
    st.success(f"Predicted Detector Grade: {result} %")
