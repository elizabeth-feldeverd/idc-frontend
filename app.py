import streamlit as st
from PIL import Image
import requests
from streamlit_juxtapose import juxtapose
import pathlib
from random import randrange
import uuid


st.write(
    "Upload a breast cancer histology image, and see regions of interest highlighted"
)

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static


you_want = False

png = st.file_uploader("Upload a PNG image", type=([".png"]))


if png:
    # input = randrange(100, 1000, 2)
    # output = input + 1

    # IMG1 = f"img{input}.png"

    myuuid = uuid.uuid4()
    IMG1 = f"{myuuid}.png"

    # url = "http://127.0.0.1:8000/annotate"  # local
    url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (png.name, png, "multipart/form-data")}
    response = requests.post(url, files=files)

    # How to download image from url
    IMG2 = response.json()["url"]

    # put a spinny wheel while waiting for the response

    original = Image.open(png)
    original.save(STREAMLIT_STATIC_PATH / IMG1)  # this overwites

    juxtapose(IMG1, IMG2)
