FROM python:3
WORKDIR /app
ADD requirements.txt .
ADD app /app

WORKDIR /
# install FreeTDS and dependencies
RUN apt-get update \
    && apt-get install apt-utils -y \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && apt-get install android-tools-adb>=1:8.1.0+r23-5 -y \
    && apt-get install poppler-utils -y \
    && cd /app\
    && pip install -r requirements.txt\
    && pyppeteer-install \
    && rm -rf /var/lib/apt/lists/*
    
RUN BASE_URL=https://github.com/mozilla/geckodriver/releases/download \
  && VERSION=v0.32.1 \
  && curl -sL "$BASE_URL/$VERSION/geckodriver-$VERSION-linux64.tar.gz" | \
    tar -xz -C /usr/local/bin

WORKDIR /app


# CMD ["python","-i","MangaExporter.py"]
CMD tail -f /dev/null