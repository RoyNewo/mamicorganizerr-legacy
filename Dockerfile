FROM python:3
WORKDIR /app
ADD requirements.txt .
ADD app /app

WORKDIR /
# install FreeTDS and dependencies
RUN apt-get update \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && apt-get install android-tools-adb=1:8.1.0+r23-5 -y \
    && apt-get install nmap -y \
    && apt-get install poppler-utils -y \
    && git clone https://github.com/wangoloj/python3-nmap.git\
    # && mkdir -p /media/cristian/Datos/Comics\
    # && mkdir /config\
    && cd /python3-nmap\
    && pip install -r requirements.txt\
    && cd /app\
    && pip install -r requirements.txt\
    && rm -rf /python3-nmap\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


# CMD ["python","-i","MangaExporter.py"]
CMD tail -f /dev/null