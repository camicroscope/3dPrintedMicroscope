from python

workdir /src

copy requirements.txt .
run pip install -r requirements.txt

copy * .

EXPOSE 8020

cmd ["python", "uploading.py"]