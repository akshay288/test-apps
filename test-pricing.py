import streamlit as st

plan_details = {
    "Free": {"base_price": 0, "credits": 3000, "browsers": 5},
    "Startup": {"base_price": 30, "credits": 18000, "browsers": 25},
    "Scale": {"base_price": 100, "credits": 60000, "browsers": 100},
    "Ultra": {"base_price": 1000, "credits": 600000, "browsers": 250},
}

def calculate_total_price(plan, total_browsers, total_credits):
    additional_browser_price = 2.50
    credit_cost_per_gb = 6  # 6 credits per GB
    credit_cost_per_browser_hour = 1  # 1 credit per browser hour

    base_price = plan_details[plan]["base_price"]
    included_credits = plan_details[plan]["credits"]
    included_browsers = plan_details[plan]["browsers"]

    used_credits = (total_credits["gb"] * credit_cost_per_gb) + (total_credits["hours"] * credit_cost_per_browser_hour)
    overage_credits = max(0, used_credits - included_credits)
    overage_cost = overage_credits * 0.002  # $0.002 per overage credit

    extra_browsers = max(0, total_browsers - included_browsers)
    browser_cost = extra_browsers * additional_browser_price

    total_price = base_price + browser_cost + overage_cost

    return total_price, overage_credits, used_credits, extra_browsers

def main():
    st.title("Hyperbrowser Pricing Calculator")

    st.sidebar.header("Choose a Plan")
    plan = st.sidebar.selectbox("Select your plan:", ["Free", "Startup", "Scale", "Ultra"])

    st.sidebar.header("Total Usage")
    total_browsers = st.sidebar.slider(
        "Total concurrent browsers:", min_value=0, max_value=1000, step=1, value=0
    )
    total_gb = st.sidebar.slider(
        "Total data usage (GB):", min_value=0.0, max_value=1000.0, step=0.1, value=0.0
    )
    total_browser_hours = st.sidebar.slider(
        "Total browser usage (hours):", min_value=0, max_value=10000, step=1, value=0
    )

    total_credits = {"gb": total_gb, "hours": total_browser_hours}

    total_price, overage_credits, used_credits, extra_browsers = calculate_total_price(plan, total_browsers, total_credits)

    st.header(f"Selected Plan: {plan}")
    st.write(f"Base Price: ${plan_details[plan]['base_price']:.2f}")
    st.write(f"Included Credits: {plan_details[plan]['credits']} credits")

    st.subheader("Calculation Details")
    st.write(f"Credits Used for Data: {total_credits['gb']} GB x 6 credits/GB = {total_credits['gb'] * 6:.2f} credits")
    st.write(f"Credits Used for Browser Hours: {total_credits['hours']} hours x 1 credit/hour = {total_credits['hours']:.2f} credits")
    st.write(f"Total Used Credits: {used_credits:.2f} credits")
    st.write(f"Overage Credits: {overage_credits:.2f} credits x $0.002 = ${overage_credits * 0.002:.2f}")
    st.write(f"Extra Browsers: {extra_browsers} x $2.50 = ${extra_browsers * 2.50:.2f}")

    st.write(f"Included Browsers: {plan_details[plan]['browsers']}")
    st.write(f"Total Browsers: {total_browsers}")
    st.write(f"Total Data Usage: {total_gb} GB")
    st.write(f"Total Browser Hours: {total_browser_hours} hours")

    st.subheader("Total Price")
    st.write(f"Total Price: ${total_price:.2f}")

if __name__ == "__main__":
    main()

