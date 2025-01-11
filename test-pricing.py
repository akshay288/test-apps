import streamlit as st

plan_details = {
    "Startup": {"base_price": 30, "credits": 18000, "browsers": 25},
    "Scale": {"base_price": 100, "credits": 60000, "browsers": 100},
    "Ultra": {"base_price": 1000, "credits": 600000, "browsers": 250},
}

def calculate_total_price(plan, total_browsers, total_gb, total_browser_hours):
    additional_browser_price = 2.50
    credit_cost_per_mb = 6  # 6 credits per MB
    credit_cost_per_browser_minute = 1  # 1 credit per browser minute

    base_price = plan_details[plan]["base_price"]
    included_credits = plan_details[plan]["credits"]
    included_browsers = plan_details[plan]["browsers"]

    # Calculate credits used for data and browser hours separately
    total_mb = total_gb * 1024  # Convert GB to MB
    used_credits_gb = total_mb * credit_cost_per_mb
    browser_minutes = total_browser_hours * 60  # Convert hours to minutes
    used_credits_hours = browser_minutes * credit_cost_per_browser_minute
    used_credits = used_credits_gb + used_credits_hours
    
    overage_credits = max(0, used_credits - included_credits)
    overage_cost = overage_credits * 0.002  # $0.002 per overage credit

    extra_browsers = max(0, total_browsers - included_browsers)
    browser_cost = extra_browsers * additional_browser_price

    # Total price calculation
    total_price = base_price + overage_cost + browser_cost

    breakdown = {
        "Base Plan Details": {
            "Base Price": f"${base_price:.2f}",
            "Included Credits": f"{included_credits:,} credits",
            "Included Browsers": f"{plan_details[plan]['browsers']} browsers"
        },
        "Usage Breakdown": {
            "Data Credits": f"{total_gb:,.1f} GB ({total_mb:,.1f} MB) × {credit_cost_per_mb} credits/MB = {used_credits_gb:,} credits",
            "Browser Minutes Credits": f"{browser_minutes:,} minutes × {credit_cost_per_browser_minute} credit/minute = {used_credits_hours:,} credits",
            "Total Credits Used": f"{used_credits:,} credits"
        },
        "Overage Calculations": {
            "Credit Overage": f"{overage_credits:,} credits",
            "Credit Overage Cost": f"${overage_cost:.2f}",
            "Extra Browsers": f"{extra_browsers:,} browsers",
            "Extra Browser Cost": f"${browser_cost:.2f}"
        }
    }

    return total_price, breakdown

def main():
    st.title("Hyperbrowser Pricing Calculator")

    st.header("Select Your Plan")
    plan = st.selectbox("Select your plan:", ["Startup", "Scale", "Ultra"])

    st.header("Plan Details")
    st.write(f"**Plan:** {plan}")
    st.write(f"Base Price: ${plan_details[plan]['base_price']:.2f}")
    st.write(f"Included Credits: {plan_details[plan]['credits']} credits")
    st.write(f"Included Browsers: {plan_details[plan]['browsers']}")

    st.header("Enter Your Usage")

    # Initialize session state
    if 'browsers' not in st.session_state:
        st.session_state.browsers = 0
    if 'gb' not in st.session_state:
        st.session_state.gb = 0.0
    if 'hours' not in st.session_state:
        st.session_state.hours = 0

    def update_browsers():
        st.session_state.browsers = st.session_state.browsers_slider
    
    def update_browsers_slider():
        st.session_state.browsers_slider = st.session_state.browsers

    def update_gb():
        st.session_state.gb = st.session_state.gb_slider
    
    def update_gb_slider():
        st.session_state.gb_slider = st.session_state.gb

    def update_hours():
        st.session_state.hours = st.session_state.hours_slider
    
    def update_hours_slider():
        st.session_state.hours_slider = st.session_state.hours

    col1, col2 = st.columns([2, 1])
    with col1:
        total_browsers = st.slider(
            "Total concurrent browsers:",
            min_value=0,
            max_value=2500,
            step=1,
            value=st.session_state.browsers,
            key="browsers_slider",
            on_change=update_browsers
        )
    with col2:
        total_browsers = st.number_input(
            "Input total browsers:",
            min_value=0,
            max_value=2500,
            step=1,
            value=st.session_state.browsers,
            key="browsers",
            on_change=update_browsers_slider
        )

    col3, col4 = st.columns([2, 1])
    with col3:
        total_gb = st.slider(
            "Total proxy data usage (GB):",
            min_value=0.0,
            max_value=10000.0,
            step=0.1,
            value=st.session_state.gb,
            key="gb_slider",
            on_change=update_gb
        )
    with col4:
        total_gb = st.number_input(
            "Input total GB:",
            min_value=0.0,
            max_value=10000.0,
            step=0.1,
            value=st.session_state.gb,
            key="gb",
            on_change=update_gb_slider
        )

    col5, col6 = st.columns([2, 1])
    with col5:
        total_browser_hours = st.slider(
            "Total browser usage (hours):",
            min_value=0,
            max_value=100000,
            step=1,
            value=st.session_state.hours,
            key="hours_slider",
            on_change=update_hours
        )
    with col6:
        total_browser_hours = st.number_input(
            "Input browser hours:",
            min_value=0,
            max_value=100000,
            step=1,
            value=st.session_state.hours,
            key="hours",
            on_change=update_hours_slider
        )

    total_price, breakdown = calculate_total_price(plan, total_browsers, total_gb, total_browser_hours)

    st.header(f"Selected Plan: {plan}")

    st.subheader("📊 Pricing Breakdown")
    
    # Create columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🏢 Base Plan")
        for key, value in breakdown["Base Plan Details"].items():
            st.markdown(f"**{key}:** {value}")
    
    st.markdown("### 📈 Usage Details")
    for key, value in breakdown["Usage Breakdown"].items():
        if key == "Total Credits Used":
            st.markdown(f"**{key}:** :red[{value}]", unsafe_allow_html=True)
        else:
            st.markdown(f"**{key}:** {value}", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💰 Additional Costs")
        for key, value in breakdown["Overage Calculations"].items():
            if "Cost" in key:
                st.markdown(f"**{key}:** :red[{value}]")
            else:
                st.markdown(f"**{key}:** {value}")

    st.markdown("---")
    st.subheader("💵 Total Price")
    st.markdown(f"## :blue[${total_price:,.2f}]")

if __name__ == "__main__":
    main()

