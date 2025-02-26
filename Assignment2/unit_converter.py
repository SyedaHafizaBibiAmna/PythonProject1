import streamlit as st

# Organize conversions by category
CATEGORIES = {
    "Area": ["Square Kilometers", "Square Meters", "Hectares", "Acres", "Square Yards", "Square Feet", "Square Inches"],
    "Data Transfer": ["Bits per second", "Kilobits per second", "Megabits per second", "Gigabits per second",
                     "Kilobytes per second", "Megabytes per second", "Gigabytes per second", "Terabytes per second"],
    "Digital Storage": ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes", "Bits"],
    "Energy": ["Joules", "Kilojoules", "Calories", "Kilocalories", "Watt Hours", "Kilowatt Hours", "British Thermal Units"],
    "Length": ["Kilometers", "Meters", "Centimeters", "Millimeters", "Miles", "Yards", "Feet", "Inches", "Nautical Miles"],
    "Mass": ["Kilograms", "Grams", "Milligrams", "Metric Tons", "Pounds", "Ounces"],
    "Pressure": ["Pascal", "Kilopascal", "Bar", "Atmosphere", "Millimeter of Mercury", "Pound per Square Inch"],
    "Speed": ["Meters per Second", "Kilometers per Hour", "Miles per Hour", "Knots"],
    "Temperature": ["Celsius", "Fahrenheit"],
    "Time": ["Seconds", "Milliseconds", "Microseconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"],
    "Volume": ["Cubic Meters", "Liters", "Milliliters", "Gallons (US)", "Quarts (US)", "Pints (US)", "Cups (US)", "Fluid Ounces (US)"]
}

conversion_map={
    "Miles":{"Kilometers": lambda x:x * 1.60934},
    "Kilometers":{"Miles": lambda x:x / 1.60934},
    "Pounds":{"Kilograms": lambda x:x * 0.453592},
    "Kilograms":{"Pounds": lambda x:x / 0.453592},
    "Inches":{"Centimeters": lambda x:x * 2.54},
    "Centimeter":{"Inches": lambda x:x / 2.54},
    "Fahrenheit":{"Celsius": lambda x:(x-32)*5/9},
    "Celsius":{"Fahrenheit": lambda x:(x*9/5)+32},
    # Data Transfer Rate conversions
    "Kilobytes per second": {
        "Megabytes per second": lambda x: x / 1024,
        "Gigabytes per second": lambda x: x / (1024 * 1024),
        "Terabytes per second": lambda x: x / (1024 * 1024 * 1024),
        "Bits per second": lambda x: x * 8192,
        "Kilobits per second": lambda x: x * 8,
        "Megabits per second": lambda x: x / 128,
        "Gigabits per second": lambda x: x / 131072
    },
    "Megabytes per second": {
        "Kilobytes per second": lambda x: x * 1024,
        "Gigabytes per second": lambda x: x / 1024,
        "Terabytes per second": lambda x: x / (1024 * 1024),
        "Bits per second": lambda x: x * 8388608,
        "Kilobits per second": lambda x: x * 8192,
        "Megabits per second": lambda x: x * 8,
        "Gigabits per second": lambda x: x / 128
    },
    "Gigabytes per second": {
        "Kilobytes per second": lambda x: x * 1024 * 1024,
        "Megabytes per second": lambda x: x * 1024,
        "Terabytes per second": lambda x: x / 1024,
        "Bits per second": lambda x: x * 8589934592,
        "Kilobits per second": lambda x: x * 8388608,
        "Megabits per second": lambda x: x * 8192,
        "Gigabits per second": lambda x: x * 8
    },
    "Terabytes per second": {
        "Kilobytes per second": lambda x: x * 1024 * 1024 * 1024,
        "Megabytes per second": lambda x: x * 1024 * 1024,
        "Gigabytes per second": lambda x: x * 1024,
        "Bits per second": lambda x: x * 8796093022208,
        "Kilobits per second": lambda x: x * 8589934592,
        "Megabits per second": lambda x: x * 8388608,
        "Gigabits per second": lambda x: x * 8192
    },
    "Bits per second": {
        "Kilobytes per second": lambda x: x / 8192,
        "Megabytes per second": lambda x: x / 8388608,
        "Gigabytes per second": lambda x: x / 8589934592,
        "Terabytes per second": lambda x: x / 8796093022208,
        "Kilobits per second": lambda x: x / 1024,
        "Megabits per second": lambda x: x / (1024 * 1024),
        "Gigabits per second": lambda x: x / (1024 * 1024 * 1024)
    },
    "Kilobits per second": {
        "Kilobytes per second": lambda x: x / 8,
        "Megabytes per second": lambda x: x / 8192,
        "Gigabytes per second": lambda x: x / 8388608,
        "Terabytes per second": lambda x: x / 8589934592,
        "Bits per second": lambda x: x * 1024,
        "Megabits per second": lambda x: x / 1024,
        "Gigabits per second": lambda x: x / (1024 * 1024)
    },
    "Megabits per second": {
        "Kilobytes per second": lambda x: x * 128,
        "Megabytes per second": lambda x: x / 8,
        "Gigabytes per second": lambda x: x / 8192,
        "Terabytes per second": lambda x: x / 8388608,
        "Bits per second": lambda x: x * 1024 * 1024,
        "Kilobits per second": lambda x: x * 1024,
        "Gigabits per second": lambda x: x / 1024
    },
    "Gigabits per second": {
        "Kilobytes per second": lambda x: x * 131072,
        "Megabytes per second": lambda x: x * 128,
        "Gigabytes per second": lambda x: x / 8,
        "Terabytes per second": lambda x: x / 8192,
        "Bits per second": lambda x: x * 1024 * 1024 * 1024,
        "Kilobits per second": lambda x: x * 1024 * 1024,
        "Megabits per second": lambda x: x * 1024
    },
    # Length conversions
    "Meters": {
        "Nanometers": lambda x: x * 1e9,
        "Millimeters": lambda x: x * 1000,
        "Centimeters": lambda x: x * 100,
        "Miles": lambda x: x * 0.000621371,
        "Yards": lambda x: x * 1.09361,
        "Feet": lambda x: x * 3.28084,
        "Inches": lambda x: x * 39.3701,
        "Nautical Miles": lambda x: x * 0.000539957
    },
    "Nanometers": {
        "Meters": lambda x: x / 1e9,
        "Millimeters": lambda x: x / 1e6,
        "Centimeters": lambda x: x / 1e7
    },
    "Millimeters": {
        "Meters": lambda x: x / 1000,
        "Nanometers": lambda x: x * 1e6,
        "Centimeters": lambda x: x / 10
    },
    "Yards": {
        "Meters": lambda x: x * 0.9144,
        "Feet": lambda x: x * 3,
        "Inches": lambda x: x * 36
    },
    "Feet": {
        "Meters": lambda x: x * 0.3048,
        "Yards": lambda x: x / 3,
        "Inches": lambda x: x * 12
    },
    "Nautical Miles": {
        "Meters": lambda x: x * 1852,
        "Miles": lambda x: x * 1.15078
    },
    
    # Area conversions
    "Square Kilometers": {
        "Square Meters": lambda x: x * 1e6,
        "Hectares": lambda x: x * 100,
        "Acres": lambda x: x * 247.105,
        "Square Yards": lambda x: x * 1.196e6,
        "Square Feet": lambda x: x * 1.076e7,
        "Square Inches": lambda x: x * 1.55e9
    },
    "Square Meters": {
        "Square Kilometers": lambda x: x / 1e6,
        "Hectares": lambda x: x / 10000,
        "Square Yards": lambda x: x * 1.19599,
        "Square Feet": lambda x: x * 10.7639,
        "Square Inches": lambda x: x * 1550
    },
    "Square Yards": {
        "Square Meters": lambda x: x * 0.836127,
        "Square Feet": lambda x: x * 9,
        "Square Inches": lambda x: x * 1296
    },
    "Square Feet": {
        "Square Meters": lambda x: x * 0.092903,
        "Square Yards": lambda x: x / 9,
        "Square Inches": lambda x: x * 144
    },
    "Square Inches": {
        "Square Meters": lambda x: x * 0.00064516,
        "Square Yards": lambda x: x / 1296,
        "Square Feet": lambda x: x / 144
    },
    "Hectares": {
        "Square Kilometers": lambda x: x / 100,
        "Square Meters": lambda x: x * 10000,
        "Acres": lambda x: x * 2.47105
    },
    "Acres": {
        "Square Kilometers": lambda x: x * 0.00404686,
        "Hectares": lambda x: x * 0.404686,
        "Square Meters": lambda x: x * 4046.86
    },
    
    # Volume conversions
    "Cubic Meters": {
        "Cubic Centimeters": lambda x: x * 1e6,
        "Cubic Millimeters": lambda x: x * 1e9,
        "Liters": lambda x: x * 1000,
        "Milliliters": lambda x: x * 1e6,
        "Gallons (US)": lambda x: x * 264.172,
        "Quarts (US)": lambda x: x * 1056.69,
        "Pints (US)": lambda x: x * 2113.38,
        "Cups (US)": lambda x: x * 4226.75,
        "Fluid Ounces (US)": lambda x: x * 33814
    },
    "Liters": {
        "Cubic Meters": lambda x: x / 1000,
        "Milliliters": lambda x: x * 1000,
        "Gallons (US)": lambda x: x * 0.264172,
        "Quarts (US)": lambda x: x * 1.05669,
        "Pints (US)": lambda x: x * 2.11338,
        "Cups (US)": lambda x: x * 4.22675,
        "Fluid Ounces (US)": lambda x: x * 33.814
    },
    
    # Time conversions
    "Seconds": {
        "Milliseconds": lambda x: x * 1000,
        "Microseconds": lambda x: x * 1e6,
        "Minutes": lambda x: x / 60,
        "Hours": lambda x: x / 3600,
        "Days": lambda x: x / 86400,
        "Weeks": lambda x: x / 604800,
        "Months": lambda x: x / 2.628e6,
        "Years": lambda x: x / 3.1536e7
    },
    
    # Energy conversions
    "Joules": {
        "Kilojoules": lambda x: x / 1000,
        "Calories": lambda x: x / 4.184,
        "Kilocalories": lambda x: x / 4184,
        "Watt Hours": lambda x: x / 3600,
        "Kilowatt Hours": lambda x: x / 3.6e6,
        "Electron Volts": lambda x: x * 6.242e18,
        "British Thermal Units": lambda x: x / 1055.06
    },
    
    # Pressure conversions
    "Pascal": {
        "Kilopascal": lambda x: x / 1000,
        "Bar": lambda x: x / 100000,
        "Atmosphere": lambda x: x / 101325,
        "Millimeter of Mercury": lambda x: x / 133.322,
        "Pound per Square Inch": lambda x: x / 6894.76
    },
    
    # Speed conversions
    "Meters per Second": {
        "Kilometers per Hour": lambda x: x * 3.6,
        "Miles per Hour": lambda x: x * 2.23694,
        "Knots": lambda x: x * 1.94384,
        "Feet per Second": lambda x: x * 3.28084
    },
    
    # Digital Storage conversions
    "Bytes": {
        "Kilobytes": lambda x: x / 1024,
        "Megabytes": lambda x: x / (1024 ** 2),
        "Gigabytes": lambda x: x / (1024 ** 3),
        "Terabytes": lambda x: x / (1024 ** 4),
        "Bits": lambda x: x * 8
    },
    
    # Mass conversions (expanded)
    "Grams": {
        "Kilograms": lambda x: x / 1000,
        "Milligrams": lambda x: x * 1000,
        "Metric Tons": lambda x: x / 1e6,
        "Pounds": lambda x: x / 453.592,
        "Ounces": lambda x: x / 28.3495,
        "Carats": lambda x: x * 5
    },
    
    # Currency conversions (Note: These are static rates, should be updated with real-time data)
    "USD": {
        "EUR": lambda x: x * 0.85,
        "GBP": lambda x: x * 0.73,
        "JPY": lambda x: x * 110.0,
        "CAD": lambda x: x * 1.25,
        "AUD": lambda x: x * 1.35,
        "CHF": lambda x: x * 0.92
    }

}

def main():
    # Configure the page
    st.set_page_config(
        page_title="Unit Converter",
        page_icon="🔄",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            color: #2E4053;
            font-size: 3rem !important;
            text-align: center;
            margin-bottom: 2rem !important;
        }
        .stSelectbox {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 5px;
        }
        .stButton > button {
            width: 100%;
            background-color: #2E86C1;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-size: 1.2rem;
        }
        .stButton > button:hover {
            background-color: #21618C;
        }
        .success-message {
            background-color: #D4EFDF;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            color: #196F3D;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with icon and title
    st.markdown("<h1 style='text-align: center;'>🔄 Unit Converter</h1>", unsafe_allow_html=True)
    
    # Add a subtle divider
    st.markdown("---")

    # Category selection with icon
    st.markdown("### 📊 Select Category")
    category = st.selectbox("", options=list(CATEGORIES.keys()))
    
    # Create container for main conversion interface
    with st.container():
        # Create three columns with better spacing
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Input value with better styling
        with col1:
            st.markdown("### 📝 Enter Value")
            value = st.number_input("", value=0.0, format="%.8f")
        
        # From unit selection
        with col2:
            st.markdown("### 📥 From")
            from_unit = st.selectbox("", options=CATEGORIES[category], key="from_unit")
        
        # To unit selection
        with col3:
            st.markdown("### 📤 To")
            to_unit_options = [unit for unit in CATEGORIES[category] if unit != from_unit]
            to_unit = st.selectbox("", options=to_unit_options, key="to_unit")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centered convert button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        convert_clicked = st.button("Convert ⚡")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Result display
    if convert_clicked:
        try:
            if from_unit in conversion_map and to_unit in conversion_map[from_unit]:
                result = conversion_map[from_unit][to_unit](value)
                st.markdown(f"""
                    <div class='success-message'>
                        {value:,} {from_unit} = {result:,.4f} {to_unit}
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Try reverse conversion
                if to_unit in conversion_map and from_unit in conversion_map[to_unit]:
                    result = 1 / conversion_map[to_unit][from_unit](1/value) if value != 0 else 0
                    st.markdown(f"""
                        <div class='success-message'>
                            {value:,} {from_unit} = {result:,.4f} {to_unit}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("⚠️ This conversion is not available")
        except Exception as e:
            st.error(f"⚠️ Error during conversion: {str(e)}")
    
    # Footer with helpful information
    st.markdown("---")
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        ### Quick Guide
        1. 📊 Select a category of measurement
        2. 📝 Enter the value you want to convert
        3. 📥 Choose the unit to convert from
        4. 📤 Choose the unit to convert to
        5. ⚡ Click Convert to see the result
        
        ### Tips
        - Use decimal points for precise values
        - Results are rounded to 4 decimal places
        - Some conversions may be approximate
        """)

if __name__ == "__main__":
    main()

    
