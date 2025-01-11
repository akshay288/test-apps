import streamlit as st

def calculate_total_price(plan, additional_browsers, total_credits):
    plan_details = {
        "Free": {"base_price": 0, "credits": 3000, "browsers": 5},
        "Startup": {"base_price": 30, "credits": 18000, "browsers": 25},
        "Scale": {"base_price": 100, "credits": 60000, "browsers": 100},
        "Ultra": {"base_price": 1000, "credits": 600000, "browsers": 250},
    }

    additional_browser_price = 2.50
    credit_cost_per_gb = 6  # 6 credits per GB
    credit_cost_per_browser_hour = 1  # 1 credit per browser hour

    base_price = plan_details[plan]["base_price"]
    included_credits = plan_details[plan]["credits"]

    used_credits = (total_credits["gb"] * credit_cost_per_gb) + (total_credits["hours"] * credit_cost_per_browser_hour)
    overage_credits = max(0, used_credits - included_credits)
    overage_cost = overage_credits * 0.002  # $0.002 per overage credit

    total_price = base_price + (additional_browsers * additional_browser_price) + overage_cost

    return total_price, overage_credits, used_credits

def main():
    st.title("Hyperbrowser Pricing Calculator")

    st.sidebar.header("Choose a Plan")
    plan = st.sidebar.selectbox("Select your plan:", ["Free", "Startup", "Scale", "Ultra"])

    st.sidebar.header("Customize Your Plan")
    additional_browsers = 0
    if plan != "Free":
        additional_browsers = st.sidebar.number_input(
            "Number of additional concurrent browsers:", min_value=0, step=1, value=0
        )

    st.sidebar.header("Total Usage")
    total_gb = st.sidebar.slider(
        "Total data usage (GB):", min_value=0.0, max_value=1000.0, step=0.1, value=0.0
    )
    total_browser_hours = st.sidebar.slider(
        "Total browser usage (hours):", min_value=0, max_value=10000, step=1, value=0
    )

    total_credits = {"gb": total_gb, "hours": total_browser_hours}

    total_price, overage_credits, used_credits = calculate_total_price(plan, additional_browsers, total_credits)

    st.header(f"Selected Plan: {plan}")
    st.write(f"Base Price: ${plan_details[plan]['base_price']:.2f}")
    st.write(f"Included Credits: {plan_details[plan]['credits']} credits")
    st.write(f"Used Credits: {used_credits:.2f} credits")
    st.write(f"Overage Credits: {overage_credits:.2f} credits")
    st.write(f"Additional Browsers: {additional_browsers}")
    st.write(f"Total Data Usage: {total_gb} GB")
    st.write(f"Total Browser Hours: {total_browser_hours} hours")
    st.write(f"Total Price: ${total_price:.2f}")

if __name__ == "__main__":
    main()

