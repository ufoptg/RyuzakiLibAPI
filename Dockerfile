FROM rendyprojects/python:latest

WORKDIR /app/

 RUN apt -qq update
 RUN apt -qq install -y --no-install-recommends \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    python3-pip \
    ffmpeg \
    neofetch

COPY . .

RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
