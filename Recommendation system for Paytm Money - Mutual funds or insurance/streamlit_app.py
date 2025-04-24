import streamlit as st
import pandas as pd

# Load mutual fund data
fund_data = pd.read_excel("mutual_funds.xlsx")

# Clean/normalize the Risk column
fund_data["Risk"] = fund_data["Risk"].str.strip().str.capitalize()

# Mapping for user goals → suitable fund categories
goal_map = {
    "Growth": ["Equity", "Hybrid"],
    "Tax Saving": ["ELSS"],
    "Retirement": ["Debt", "Hybrid"]
}

risk_order = {"Low": 1, "Medium": 2, "High": 3}

# Streamlit UI
st.set_page_config(page_title="Mutual Fund Recommender", page_icon="💰")
st.title("📊 Paytm-Style Mutual Fund Recommendation System")

st.markdown("Enter your profile to get personalized mutual fund suggestions:")

# Input form
with st.form("user_profile_form"):
    age = st.slider("Age", 18, 70, 30)
    income = st.number_input("Annual Income (₹)", min_value=100000, value=1000000, step=50000)
    risk = st.selectbox("Risk Tolerance", options=["Low", "Medium", "High"])
    horizon = st.slider("Investment Horizon (Years)", 1, 30, 5)
    goal = st.selectbox("Investment Goal", options=["Growth", "Tax Saving", "Retirement"])
    
    submitted = st.form_submit_button("Recommend Funds")

# Recommendation logic
def recommend_funds(user_profile, top_n=3):
    preferred_categories = goal_map.get(user_profile["Investment Goal"], [])
    user_risk_level = risk_order[user_profile["Risk Tolerance"]]

    # Filter funds based on user preferences
    filtered = fund_data[
        (fund_data["Category"].isin(preferred_categories)) &
        (fund_data["Risk"].map(risk_order) <= user_risk_level)
    ]

    # Rank by 3-year return
    ranked = filtered.sort_values(by="Return_3Y", ascending=False)
    return ranked.head(top_n)

if submitted:
    user_profile = {
        "Age": age,
        "Income": income,
        "Risk Tolerance": risk,
        "Investment Horizon": horizon,
        "Investment Goal": goal
    }

    st.subheader("🎯 Recommended Mutual Funds:")
    results = recommend_funds(user_profile)
    st.table(results[["Fund", "Category", "Risk", "Return_3Y", "Volatility"]])