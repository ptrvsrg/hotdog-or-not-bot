FROM ultralytics/ultralytics:latest-cpu
#FROM ultralytics/ultralytics:latest

WORKDIR /opt/bot

COPY app app
COPY locales locales
COPY models models

RUN apt update \
    && apt install -y libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r app/requirements.txt

ENV PYTHONPATH=.
ENV MAJOR_VERSION=0
ENV MINOR_VERSION=1
ENV PATCH_VERSION=0
ENV LOCALE_DIR=locales
ENV DETECT_MODEL_PATH=models/yolov8n.pt
ENV PREDICT_MODEL_PATH=models/yolov8n-hotdog-cls.pt

ENTRYPOINT [ "python3", "app/main.py" ]