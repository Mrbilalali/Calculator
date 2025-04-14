import streamlit as st
import streamlit.components.v1 as components

# Setup
st.set_page_config(page_title="Calculator", layout="centered")
st.title("🧮 NAVTTC Calculator")

# Custom CSS Styling
st.markdown("""
    <style>
    /* Center the calculator and style the text input and buttons */
    .stTextInput, .stButton {
        font-size: 20px;
    }
    input[type="text"] {
        background-color: #f0f2f6;
        padding: 12px;
        border: 2px solid #ccc;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        text-align: right;
        font-size: 22px;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        font-size: 22px;
        padding: 16px;
        border: none;
        border-radius: 12px;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1abc9c;
        color: black;
        font-weight: bold;
    }
    .stButton>button:active {
        background-color: #16a085 !important;
        transform: scale(0.98);
    }
    .stError {
        color: red;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Inject JavaScript with a slight delay to auto-focus the text input field.
components.html(
    """
    <script>
    setTimeout(function(){
        // Using window.parent.document to access the Streamlit container
        const inputField = window.parent.document.querySelector('input[type="text"]');
        if (inputField) {
            inputField.focus();
        }
    }, 500);
    </script>
    """,
    height=0
)

# Initialize session state variables
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""

# Evaluate expression safely
def evaluate_expression(expr):
    try:
        expr = expr.replace("x", "*").replace("^", "**").replace("\u00A0", "")
        result = eval(expr)
        st.session_state.error_msg = ""
        return str(result)
    except:
        st.session_state.error_msg = "❌ Invalid expression. Please check your input."
        return st.session_state.expression

# Handle Enter or text field changes
def on_enter_callback():
    st.session_state.expression = evaluate_expression(st.session_state.expression)

# Handle button clicks
def on_click(val):
    if val in ["+\u00A0", "-\u00A0"]:
        val = val.strip()

    operators = {"+", "-", "*", "/", "^", "x"}

    if val == "C":
        st.session_state.expression = ""
        st.session_state.error_msg = ""
    elif val == "=":
        st.session_state.expression = evaluate_expression(st.session_state.expression)
    else:
        expr = st.session_state.expression
        if val in operators:
            if expr:
                # Replace the last operator if there's already one
                if expr[-1] in operators:
                    st.session_state.expression = expr[:-1] + val
                else:
                    st.session_state.expression += val
            else:
                # Allow starting with a minus for negative numbers
                if val == "-":
                    st.session_state.expression += val
        else:
            st.session_state.expression += val

# Text input for expression with on_change callback (Enter key press will trigger evaluation)
st.text_input("Expression", key="expression", on_change=on_enter_callback, label_visibility="collapsed")

# Display error message below the input if any
if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# Calculator buttons layout
button_rows = [
    ["C", "(", ")", "^"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "x"],
    ["1", "2", "3", "-\u00A0"],
    ["0", ".", "=", "+\u00A0"]
]

# Render the buttons
for row in button_rows:
    cols = st.columns(4)
    for col, btn in zip(cols, row):
        with col:
            st.button(btn, use_container_width=True, on_click=on_click, args=(btn,))
