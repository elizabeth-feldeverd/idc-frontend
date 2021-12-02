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

    st.markdown(
        f"""
        - The mean probability of IDC across the image is {report['mean_whole_slide']}%.
        - The percentage of high severity IDC regions across the image is {report['high_IDC_regions']}%.
        - The percentage of medium severity IDC regions across the image is {report['medium_IDC_regions']}%.
        - The percentage of low severity IDC regions across the image is {report['low_IDC_regions']}%.
        - The percentage of IDC-free regions across the image is {report['no_IDC_regions']}%.
        """
    )

    recommendation = response["recommendation"]

    recom_html = f'<p style="color:Blue; font-size: 36px;">{recommendation}</p>'

    st.markdown(recom_html, unsafe_allow_html=True)
