FROM python:3.9
WORKDIR .
COPY pythonCode1.py pythonCode1.py
COPY requirements.txt requirements.txt
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt
CMD [ "python", "pythonCode1.py"]