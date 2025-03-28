import streamlit as st

def compute_detector_grade(time_sec, growth_rate, power_w, output_impurity, net_impurity_added):
    # Scaling constants from training data
    MEANS = {
        'time': 11547.993,
        'growth_rate': 0.768411,
        'power': 8270.349,
        'output_impurity': -3.245738e12,
        'net_impurity_added': 6.295747e14,
    }
    STDS = {
        'time': 1680.1296,
        'growth_rate': 0.184491,
        'power': 2066.1872,
        'output_impurity': 5.651268e12,
        'net_impurity_added': 2.613553e15,
    }

    try:
        # Scale inputs
        T = (time_sec - MEANS['time']) / STDS['time']
        G = (growth_rate - MEANS['growth_rate']) / STDS['growth_rate']
        P = (power_w - MEANS['power']) / STDS['power']
        O = (output_impurity - MEANS['output_impurity']) / STDS['output_impurity']
        N = (net_impurity_added - MEANS['net_impurity_added']) / STDS['net_impurity_added']

        # Symbolic regression equation (scaled input domain)
        numerator1 = (T * O) - (T * N) - ((T / N) * (G - N))
        denominator1 = (N * T) + (O * G) + (P - O - G - 0.858)
        term1 = numerator1 / denominator1

        numerator2 = (O * G) - ((T / N) * (G - N))
        denominator2 = ((T / N) * N) + (O * G) + (0.478 / N)
        term2 = numerator2 / denominator2

        term3 = (T / N) * (G - N)
        term4 = O * G
        term5 = G * 0.992

        DG = term1 + term2 + term3 + term4 + term5

        # Physically constrain output between 0% and 100%
        DG = max(0.0, min(DG, 100.0))

        return round(DG, 3)

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
    output_impurity = st.number_input("Output Net Impurity", min_value=-1e13, value=4.7e11)
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
