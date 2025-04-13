import streamlit as st

# Setup
st.set_page_config(page_title="Calculator", layout="centered")
st.title("🧮 NAVTTC Calculator")

# Initialize expression
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Evaluate expression safely
def evaluate_expression(expr):
    try:
        expr = expr.replace("x", "*").replace("^", "**").replace("\u00A0", "")
        result = eval(expr)
        return str(result)
    except:
        return "Error"

# Handle button click
def on_click(val):
    if val in ["+\u00A0", "-\u00A0"]:
        val = val.strip()  # remove non-breaking space
    if val == "C":
        st.session_state.expression = ""
    elif val == "=":
        st.session_state.expression = evaluate_expression(st.session_state.expression)
    else:
        st.session_state.expression += val

# Display expression
st.text_input("Expression", value=st.session_state.expression, disabled=True)

# Buttons layout
button_rows = [
    ["C", "(", ")", "^"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "x"],
    ["1", "2", "3", "-\u00A0"],
    ["0", ".", "=", "+\u00A0"]
]

# Render buttons
for row in button_rows:
    cols = st.columns(4)
    for col, btn in zip(cols, row):
        with col:
            st.button(btn, use_container_width=True, on_click=on_click, args=(btn,))

# Optional keyboard input
with st.expander("⌨️ Or use keyboard input"):
    manual = st.text_input("Enter expression")
    if st.button("Calculate"):
        st.success(f"Result: {evaluate_expression(manual)}")
