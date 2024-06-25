from python


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

workdir /src

copy requirements.txt .
run pip install -r requirements.txt

copy ./ /src/

EXPOSE 8020

cmd ["python", "uploading.py"]