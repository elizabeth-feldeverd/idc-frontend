import streamlit as st
from PIL import Image
import requests
import requests
from streamlit_juxtapose import juxtapose
import pathlib
from random import randrange

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static


you_want = False

png = st.file_uploader("Upload a PNG image", type=([".png"]))


if png:
    input = randrange(100, 1000, 2)
    output = input + 1

    IMG1 = f"img{input}.png"
    IMG2 = f"img{output}.png"

    # st.image(png)  # display image

    # url = "http://127.0.0.1:8000/annotate"  # local
    url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (png.name, png, "multipart/form-data")}
    response = requests.post(url, files=files)

    # put a spinny wheel while waiting for the response

    # st.image(response._content)  # display heatmap

    original = Image.open(png)
    original.save(STREAMLIT_STATIC_PATH / IMG1)  # this overwites

    # if push comes to shove vvv
    file = open(f"{STREAMLIT_STATIC_PATH}/{IMG2}", "wb")  # this overwites
    file.write(response.content)
    file.close()

    # juxtapose(
    #     f"../{STREAMLIT_STATIC_PATH}/{IMG1}", f"../{STREAMLIT_STATIC_PATH}/{IMG2}"
    # )
    juxtapose(IMG1, IMG2)
