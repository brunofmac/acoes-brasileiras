---
name: run
description: Launch the Streamlit dashboard locally and confirm it's running. Use when asked to start, run, or preview the app.
---

Launch the app with:

```bash
streamlit run app.py
```

The app starts on http://localhost:8501. Run this command in the background and confirm the server started by checking for the "You can now view your Streamlit app" message in output. Tell the user the URL and which port it's on. If port 8501 is already in use, Streamlit will try 8502 — note whichever port it picked.

If dependencies are missing, run `pip install -r requirements.txt` first.
