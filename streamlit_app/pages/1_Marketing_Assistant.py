import streamlit as st
import json
from app.marketing.store import create_draft, list_items, update_status, get_item
import pandas as pd
from app.marketing.generate import generate_marketing_content
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.title("Marketing Automation Assistant")

# Marketing Content Input
prompt_file = st.selectbox("Select Prompt Version", ["marketing_email_v1.yaml", "marketing_push_v1.yaml", "marketing_blog_v1.yaml"])

content_type = st.selectbox("Content Type", ["email", "push", "blog"])
brief = st.text_area("Content Brief", placeholder="Describe the campaign, feature, offer, etc.")
audience = st.text_input("Audience", placeholder="e.g., New traders, active traders, partners")
goal = st.text_input("Goal", placeholder="e.g., announce feature, increase activation")
offer = st.text_input("Offer (optional)", placeholder="e.g., bonus terms, discount, webinar")

# Generate Marketing Content
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Content"):
        if brief:
            content = generate_marketing_content(prompt_file, content_type, brief, audience, goal, offer)
            st.session_state["generated_content"] = content
            st.subheader("Generated Content")
            st.json(content.dict(), expanded=True)

with col2:
    if "generated_content" in st.session_state:
        content = st.session_state["generated_content"]
        if st.button("Save as Draft"):
            create_draft(content.content_type, brief, content)
            st.success("Draft saved successfully!")

# Approval Workflow
st.divider()

st.subheader("Approval Workflow: Draft → Approved → Published")

items = list_items()
if items:
    df = pd.DataFrame([{
        "id": i.id,
        "status": i.status,
        "type": i.content_type,
        "prompt": i.prompt_file,
        "brief": (i.brief[:60] + "...") if len(i.brief) > 60 else i.brief,
    } for i in items])
    st.dataframe(df, use_container_width=True)

    selected_id = st.number_input("Select Draft ID", min_value=1, step=1)
    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("View Item"):
            item = get_item(int(selected_id))
            if item:
                st.write(f"**Status:** {item.status}")
                st.code(item.payload_json, language="json")
            else:
                st.warning("Item not found.")

    with colB:
        if st.button("Approve"):
            update_status(int(selected_id), "APPROVED")
            st.success("Item approved.")

    with colC:
        if st.button("Publish"):
            update_status(int(selected_id), "PUBLISHED")
            st.success("Item published.")

else:
    st.info("No drafts available. Generate content and save as draft.")
