import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Universal Link Guard", page_icon="🔒", layout="centered")

# 2. The Popup Logic
@st.dialog("⚠️ Link Permission Required")
def show_permission_gate(url):
    # Decode the URL in case it was passed with %20, %3A, etc.
    decoded_url = urllib.parse.unquote(url)
    
    st.markdown("### A link is requesting to open")
    st.info(f"**Destination:** {decoded_url}")
    st.write("Do you want to leave this app and go to the link?")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ YES, Open", use_container_width=True, type="primary"):
            st.success("Redirecting...")
            # JavaScript to trigger the redirect
            js_script = f"""
                <script>
                    window.parent.location.href = "{decoded_url}";
                </script>
            """
            components.html(js_script, height=0)
            
    with col2:
        if st.button("❌ NO, Block", use_container_width=True):
            # Clear params and refresh
            st.query_params.clear()
            st.rerun()

# 3. Backend Listener
params = st.query_params

if "target" in params:
    target_link = params["target"]
    show_permission_gate(target_link)
else:
    st.title("🛡️ Secure Gateway Active")
    st.write("The app is waiting for a link from WhatsApp.")
    st.divider()
    
    # Example generator to help you test properly
    st.markdown("### Generate a Secure Link")
    test_url = st.text_input("Enter a URL to wrap:", "https://www.google.com")
    
    # This encodes the URL correctly for use as a parameter
    encoded_test = urllib.parse.quote(test_url, safe='')
    base_url = "https://your-app.streamlit.app/" # Change this to your actual URL
    final_link = f"{base_url}?target={encoded_test}"
    
    st.markdown("**Your Protected Link:**")
    st.code(final_link)