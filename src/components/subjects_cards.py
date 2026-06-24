import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
    <div style="
        background: white;
        border-left: 8px solid #EB459E;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    ">
        <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 1.4rem;">{name}</h3>
        <p style="margin: 0 0 12px 0; color: #64748b;">
            Code : <span style="background:#E0E3FF; padding: 2px 8px; border-radius: 5px; color: #5865F2;">{code}</span>
            &nbsp;| Section : {section}
        </p>
    """

    if stats:
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">'
        for icon, label, value in stats:
            html += (
                f'<div style="background:rgba(235,69,158,0.1); padding:5px 12px; '
                f'border-radius:12px; font-size:0.9rem; color:#EB459E;">'
                f'{icon} <b>{value}</b> {label}'
                f'</div>'
            )
        html += '</div>'  # close stats div

    html += '</div>'  # close card div

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()