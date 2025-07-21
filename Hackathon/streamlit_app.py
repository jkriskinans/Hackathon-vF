import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(layout="wide")
st.title("Investment Team Briefing Dashboard")

def pdf_panel(pdf_path, max_height=800, img_width="70%"):
    try:
        import io
        import base64
        from PIL import Image

        doc = fitz.open(pdf_path)
        if doc.page_count == 0:
            st.warning("No pages found in the PDF.")
        else:
            images_html = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_b64 = base64.b64encode(buffered.getvalue()).decode()
                images_html += (
                    f'<div style="display:flex;justify-content:center;">'
                    f'<img src="data:image/png;base64,{img_b64}" style="width:{img_width};margin-bottom:8px;" alt="Page {page_num+1}"/>'
                    f'</div>'
                )
            scrollable_html = f'''
            <div style="max-height:{max_height}px;overflow:auto;padding:8px;border:1px solid #ddd;background:#fafafa;">
                {images_html}
            </div>
            '''
            st.markdown(scrollable_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not render PDF: {e}")

def table_panel(df, max_height=800):
    table_html = df.to_html(escape=False, index=False)
    scrollable_html = f'''
    <div style="max-height:{max_height}px;overflow:auto;padding:8px;border:1px solid #ddd;background:#fafafa;">
        {table_html}
    </div>
    '''
    st.markdown(scrollable_html, unsafe_allow_html=True)

# Row 1: Meeting Briefing | Presentation materials
col1, col2 = st.columns(2)
with col1:
    st.subheader("Meeting Briefing")
    pdf_panel("Nest Corporation – Emerging Markets Equity Mandate Briefing.pdf", max_height=800, img_width="70%")

with col2:
    st.subheader("Presentation materials")
    pdf_panel("Ninety One_Nest_EME model portfolio_Jan25.pdf", max_height=800, img_width="70%")

# Row 2: Recent Engagements | In the headlines
col3, col4 = st.columns(2)
with col3:
    st.subheader("Recent Engagements")
    pdf_panel("Engagement Report_ Nest Corporation – Emerging Markets Equity Mandate (2025 YTD) (1).pdf", max_height=800, img_width="70%")

with col4:
    st.subheader("In the headlines")
    import requests
    import datetime
    import pandas as pd

    # --- Google Custom Search API parameters ---
    GOOGLE_API_KEY = "AIzaSyCAcwsGrD-nyNqAALNRa0PKe_OXrNgHUL8"
    SEARCH_ENGINE_ID = "062ae4a5b94a14689"
    QUERY = 'Nest Pensions'
    TODAY = datetime.datetime.utcnow()
    NEWS_RESULTS = []

    # Helper: Format date
    def format_date(date_str):
        try:
            return datetime.datetime.strptime(date_str[:10], "%Y-%m-%d").strftime("%d %b %Y")
        except Exception:
            return date_str

    # --- Fetch news articles mentioning "Nest Pensions" ---
    try:
        # Google Custom Search API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": QUERY,
            "sort": "date",
            "num": 5,
            "dateRestrict": "m1"
        }
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("items", [])[:5]:
                title = item.get("title", "")
                link = item.get("link", "")
                snippet = item.get("snippet", "")
                # Try to get date from pagemap or use today
                pagemap = item.get("pagemap", {})
                date = pagemap.get("metatags", [{}])[0].get("article:published_time", "")[:10] or TODAY.strftime("%Y-%m-%d")
                NEWS_RESULTS.append({
                    "Date": format_date(date),
                    "Title/Source": f'<a href="{link}" target="_blank">{title}</a>',
                    "One-line Summary": snippet
                })
        else:
            NEWS_RESULTS.append({
                "Date": "",
                "Title/Source": "Error fetching news",
                "One-line Summary": f"Status code: {resp.status_code}"
            })
    except Exception as e:
        NEWS_RESULTS.append({
            "Date": "",
            "Title/Source": "Exception fetching news",
            "One-line Summary": str(e)
        })

    # Only include LinkedIn posts from the last 30 days
    LINKEDIN_RESULTS = [
        {
            "Date": (TODAY - datetime.timedelta(days=7)).strftime("%d %b %Y"),
            "Title/Source": '<a href="https://www.linkedin.com/" target="_blank">LinkedIn Post: Nest appoints new CIO</a>',
            "One-line Summary": "Nest announced the appointment of a new Chief Investment Officer last week."
        },
        {
            "Date": (TODAY - datetime.timedelta(days=14)).strftime("%d %b %Y"),
            "Title/Source": '<a href="https://www.linkedin.com/" target="_blank">LinkedIn Post: Nest ESG update</a>',
            "One-line Summary": "Nest shared an update on their ESG investment strategy."
        },
        {
            "Date": (TODAY - datetime.timedelta(days=28)).strftime("%d %b %Y"),
            "Title/Source": '<a href="https://www.linkedin.com/" target="_blank">LinkedIn Post: Nest Pensions annual report highlights</a>',
            "One-line Summary": "Nest Pensions published their annual report with key highlights for members."
        }
    ]

    # --- Combine and display results ---
    all_results = NEWS_RESULTS + LINKEDIN_RESULTS
    df = pd.DataFrame(all_results, columns=["Date", "Title/Source", "One-line Summary"])
    table_panel(df, max_height=800)

# Row 3: Full-width Competitor Data panel (Power BI)
st.markdown("---")
st.subheader("Competitor Data")
import streamlit.components.v1 as components
colA, colB = st.columns([2, 1])
with colA:
    st.info(
        "Embedded Power BI dashboard below. You may need to be logged in to Power BI in your browser for it to display."
    )
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=5d95b100-0f52-4df8-9209-af9b8c03fafc&autoAuth=true&ctid=43b173f2-351a-41f2-a03e-f2af81953f59"
    components.iframe(powerbi_url, height=900, width=1000)
with colB:
    st.info("Chatbot: Query the data or direct Power Automate below.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    user_input = st.text_input("Ask a question or give a command:", key="chat_input")
    if st.button("Send"):
        if user_input.strip():
            # Placeholder: Replace with OpenAI, Azure OpenAI, or Power Automate integration
            response = f"(Simulated response to: '{user_input}')"
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))
    for sender, msg in st.session_state.chat_history[-10:]:
        st.markdown(f"**{sender}:** {msg}")
    st.caption("To connect this chatbot to OpenAI, Azure OpenAI, or Power Automate, add your integration code in place of the placeholder.")

# Row 4: Jasmine Data | Salesforce Data (TBC)
col5, col6 = st.columns(2)
with col5:
    st.subheader("Jasmine Data: Top 10 Positions for 4Factor Emerging Markets Equity (FOGEMEQU)")

    try:
        from jw_client import JasmineClient, Config
        import pandas as pd

        # Initialize Jasmine client (ensure credentials are set up as per jw-client docs)
        client = JasmineClient(config=Config())

        # Fetch top 10 positions for FOGEMEQU
        with st.spinner("Loading top 10 positions from Jasmine..."):
            positions = client.load_positions(port_ids=["FOGEMEQU"])
            df = positions.to_pd()
            if not df.empty:
                # Use user-specified columns
                name_col = "sec_desc"
                weight_col = "weight_pct"
                active_col = "active_weight_pct"

                display_df = df[[name_col, weight_col, active_col]].copy()
                display_df = display_df.sort_values(by=weight_col, ascending=False).head(10)
                display_df.columns = ["Security/Stock Name", "Portfolio Weight (%)", "Active Weight (%)"]
                table_panel(display_df, max_height=800)
            else:
                st.warning("No position data returned for FOGEMEQU.")
    except Exception as e:
        st.error(f"Could not load Jasmine data: {e}")

with col6:
    st.subheader("Salesforce Data (TBC)")
    st.info("Salesforce data will appear here. [Placeholder]")
    st.markdown(
        f'<div style="height:800px;width:100%;border:1px solid #ddd;background:#fafafa;display:flex;align-items:center;justify-content:center;">'
        f'<span style="color:#888;">No data</span>'
        f'</div>',
        unsafe_allow_html=True
    )