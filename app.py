import streamlit as st
from PIL import Image
import requests
from streamlit_juxtapose import juxtapose
import pathlib
import uuid

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static


st.markdown(
    """
    # IDC Detection
    *Created by Jack Claar, Elizabeth Feldeverd, and Nadia Yap*
"""
)


png = st.file_uploader("Upload a breast cancer histology image", type=([".png"]))


if png:
    # save png
    myuuid = uuid.uuid4()
    IMG1 = f"{myuuid}.png"

    # url = "http://127.0.0.1:8000/annotate"  # local
    url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (png.name, png, "multipart/form-data")}
    response = requests.post(url, files=files).json()

    # How to download image from url
    IMG2 = response["url"]

    # put a spinny wheel while waiting for the response

    original = Image.open(png)
    width, height = original.size
    height = 705 / width * height
    original.save(STREAMLIT_STATIC_PATH / IMG1)  # this overwites
    juxtapose(IMG1, IMG2, height)

    # display legend
    legend = Image.open("legend.PNG")
    st.image(legend, use_column_width=True)
    report = response["report"]

    # Severity metrics
    st.markdown("<h4 style='text-align: left;'>Percentage of IDC severity across image</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("IDC-free", f"""{report['no_IDC_regions']}%""")
    col2.metric("Low Severity", f"""{report['low_IDC_regions']}%""")
    col3.metric("Medium Severity", f"""{report['medium_IDC_regions']}%""")
    col4.metric("High Severity", f"""{report['high_IDC_regions']}%""")

    with st.expander("See recommendation"):
        recommendation = response["recommendation"]
        st.write(recommendation)