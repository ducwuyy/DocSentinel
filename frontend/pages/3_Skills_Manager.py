import streamlit as st
from utils import ApiClient

st.set_page_config(page_title="Skills Management", page_icon="🎭", layout="wide")

st.title("🎭 Skills & Personas Management")
st.markdown("Define and customize the AI personas used for security assessments.")

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

client = ApiClient(st.session_state.api_url)

# Load Skills
try:
    skills = client.fetch_api(f"{st.session_state.api_url}/api/v1/skills/")
except Exception as e:
    st.error(f"Failed to load skills: {e}")
    skills = []

# Tabs
tab_list, tab_create = st.tabs(["📜 Available Skills", "➕ Create Custom Skill"])

with tab_list:
    if not skills:
        st.info("No skills found.")
    else:
        for skill in skills:
            with st.expander(f"{'🔒' if skill.get('is_builtin') else '✏️'} {skill['name']}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**Description**: {skill['description']}")
                    st.markdown(f"**System Prompt**:\n```\n{skill['system_prompt']}\n```")
                    st.caption(f"**ID**: `{skill['id']}`")
                with c2:
                    st.markdown("**Focus Areas:**")
                    for f in skill.get("risk_focus", []):
                        st.markdown(f"- {f}")
                    st.markdown("**Frameworks:**")
                    for f in skill.get("compliance_frameworks", []):
                        st.markdown(f"- {f}")
                    
                    if not skill.get("is_builtin"):
                        if st.button("Delete", key=f"del_{skill['id']}", type="primary"):
                            try:
                                # We need a delete method in ApiClient, or use requests directly
                                import requests
                                res = requests.delete(f"{st.session_state.api_url}/api/v1/skills/{skill['id']}")
                                if res.status_code == 200:
                                    st.success("Deleted!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed: {res.text}")
                            except Exception as e:
                                st.error(str(e))

with tab_create:
    st.header("Define a New Persona")
    with st.form("create_skill_form"):
        new_id = st.text_input("Skill ID (unique)", placeholder="e.g. pci-dss-auditor")
        new_name = st.text_input("Display Name", placeholder="e.g. PCI DSS Auditor")
        new_desc = st.text_input("Description", placeholder="Short summary of this role")
        new_prompt = st.text_area(
            "System Prompt", 
            placeholder="You are a PCI DSS Auditor. Focus on cardholder data environment...",
            height=150
        )
        new_focus = st.text_input("Risk Focus (comma separated)", placeholder="Encryption, Network Segmentation")
        new_frameworks = st.text_input("Frameworks (comma separated)", placeholder="PCI DSS v4.0")
        
        submitted = st.form_submit_button("Create Skill")
        
        if submitted:
            if not new_id or not new_name or not new_prompt:
                st.error("ID, Name, and System Prompt are required.")
            else:
                payload = {
                    "id": new_id,
                    "name": new_name,
                    "description": new_desc,
                    "system_prompt": new_prompt,
                    "risk_focus": [x.strip() for x in new_focus.split(",") if x.strip()],
                    "compliance_frameworks": [x.strip() for x in new_frameworks.split(",") if x.strip()],
                }
                try:
                    import requests
                    res = requests.post(f"{st.session_state.api_url}/api/v1/skills/", json=payload)
                    if res.status_code == 200:
                        st.success("Skill created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(str(e))
