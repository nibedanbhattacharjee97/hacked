import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Universal Link Guard", page_icon="🔒", layout="centered")

# 2. The Popup Logic
@st.dialog("⚠️ Link Permission Required")
def show_permission_gate(url):
    st.markdown("### A link is requesting to open")
    st.info(f"**Destination:** {url}")
    st.write("Do you want to leave this app and go to the link?")
    
    st.divider()
    
    # Yes and No buttons side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ YES, Open", use_container_width=True, type="primary"):
            st.success("Redirecting...")
            # Use JavaScript to override the browser location
            js_script = f"""
                <script>
                    window.top.location.href = "{url}";
                </script>
            """
            components.html(js_script, height=0)
            
    with col2:
        if st.button("❌ NO, Block", use_container_width=True):
            # Clear the link and refresh the app state
            st.query_params.clear()
            st.rerun()

# 3. Backend Listener
# This part "listens" for any link coming from WhatsApp
params = st.query_params

if "target" in params:
    # We grab the link passed in the URL
    target_link = params["target"]
    # Trigger the popup immediately upon page load
    show_permission_gate(target_link)
else:
    # Home screen if no link is clicked
    st.title("🛡️ Secure Gateway Active")
    st.write("The app is waiting for a link from WhatsApp.")
    st.divider()
    st.markdown("""
    **How to use:**
    Wrap any link (FB, Insta, YouTube) using your app URL like this:
    """)
    st.code("https://your-app.streamlit.app/?target=https://facebook.com/xyz")