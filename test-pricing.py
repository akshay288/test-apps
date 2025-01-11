import streamlit as st

plan_details = {
    "Free": {"base_price": 0, "credits": 3000, "browsers": 5},
    "Startup": {"base_price": 30, "credits": 18000, "browsers": 25},
    "Scale": {"base_price": 100, "credits": 60000, "browsers": 100},
    "Ultra": {"base_price": 1000, "credits": 600000, "browsers": 250},
}

def calculate_total_price(plan, total_browsers, used_credits):
    additional_browser_price = 2.50

    base_price = plan_details[plan]["base_price"]
    included_credits = plan_details[plan]["credits"]
    included_browsers = plan_details[plan]["browsers"]

    overage_credits = max(0, used_credits - included_credits)
    overage_cost = overage_credits * 0.002  # $0.002 per overage credit

    extra_browsers = max(0, total_browsers - included_browsers)
    browser_cost = extra_browsers * additional_browser_price

    # Total price calculation
    total_price = base_price + overage_cost + browser_cost

    breakdown = {
        "Base Price": base_price,
        "Overage Credits Cost": overage_cost,
        "Additional Browsers Cost": browser_cost
    }

    return total_price, breakdown

def main():
    st.title("Hyperbrowser Pricing Calculator")

    st.sidebar.header("Choose a Plan")
    plan = st.sidebar.selectbox("Select your plan:", ["Free", "Startup", "Scale", "Ultra"])

    st.sidebar.header("Total Usage")
    total_browsers = st.sidebar.slider(
        "Total concurrent browsers:", min_value=0, max_value=1000, step=1, value=0
    )
    used_credits = st.sidebar.slider(
        "Total credits used (for data and browser hours):", min_value=0, max_value=1000000, step=1, value=0
    )

    st.header("Plan Details")
    st.write(f"**Plan:** {plan}")
    st.write(f"Base Price: ${plan_details[plan]['base_price']:.2f}")
    st.write(f"Included Credits: {plan_details[plan]['credits']} credits")
    st.write(f"Included Browsers: {plan_details[plan]['browsers']}")

    total_price, breakdown = calculate_total_price(plan, total_browsers, used_credits)

    st.header(f"Selected Plan: {plan}")

    st.subheader("Calculation Breakdown")
    for key, value in breakdown.items():
        st.write(f"{key}: ${value:.2f}")

    st.subheader("Total Price")
    st.write(f"**Total Price: ${total_price:.2f}**")

if __name__ == "__main__":
    main()

