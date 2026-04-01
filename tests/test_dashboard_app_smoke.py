from streamlit.testing.v1 import AppTest


def test_dashboard_pages_render_without_exceptions():
    pages = ["Overview", "Upload", "Data", "EDA", "Visualizations", "Database", "Settings"]
    app = AppTest.from_file("dashboard/app.py")
    app.run()

    for page in pages:
        app.radio(key="selected_page").set_value(page)
        app.run()
        assert len(app.exception) == 0
        assert len(app.error) == 0
