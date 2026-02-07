import streamlit as st
from app.security.pii import redact_pii
from app.security.detector import detect_prompt_injection
from app.security.policy import policy_check
from app.security.audit import log_audit, list_logs
from app.security.probes import load_probes_jsonl  # Ensure this import is correct
import pandas as pd

st.title("Security Automation - PII Redaction & Injection Detection")

# Input area for text to test security
user_input = st.text_area("Enter text to test for security violations", placeholder="e.g., Can you summarize the onboarding process?")

# PII Redaction and Prompt Injection Detection
if st.button("Run Security Check"):
    # Step 1: PII Redaction
    redacted_text, pii_types = redact_pii(user_input)
    st.subheader("Redacted Text")
    st.write(redacted_text)

    # Step 2: Prompt Injection Detection
    prompt_injection_detected = detect_prompt_injection(redacted_text)
    st.subheader("Prompt Injection Detection")
    st.write(f"Prompt injection detected: {prompt_injection_detected}")

    # Step 3: Policy Check
    policy_compliant = policy_check(redacted_text)
    st.subheader("Policy Compliance Check")
    st.write(f"Content complies with security policies: {policy_compliant}")

    # Log the audit action
    log_audit(action="check_security", text=redacted_text, allowed=policy_compliant, reasons="Checked for PII, prompt injection, policy compliance")

    if not policy_compliant:
        st.warning("This content does not comply with the security policies.")

# Display Audit Logs
st.divider()
st.subheader("Audit Logs")

logs = list_logs(limit=200)
if logs:
    df = pd.DataFrame([{
        "id": l["id"],
        "user_id": l["user_id"],
        "allowed": l["allowed"],
        "risk_score": round(l["risk_score"], 2),
        "module": l["module"],
        "action": l["action"],
        "reasons": "; ".join(l["reasons"])[:120],
        "redacted_input": l["redacted_input"][:120],
    } for l in logs])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No audit logs available yet.")

# Run Synthetic Probes for Regression Testing
st.subheader("Run Synthetic Probe Tests")
if st.button("Run Probes"):
    probes = load_probes_jsonl("security/probes_prompt_injection.jsonl")
    results = []
    for probe in probes:
        redacted, _ = redact_pii(probe.text)
        prompt_injection_detected = detect_prompt_injection(redacted)
        policy_compliant = policy_check(redacted)

        result = {
            "probe_id": probe.id,
            "expected_allowed": probe.expected_allowed,
            "detected_injection": prompt_injection_detected,
            "compliance": policy_compliant
        }
        results.append(result)

    st.subheader("Probe Results")
    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
