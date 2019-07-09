FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update \
    && apt-get install software-properties-common -y\
    && apt-get install python-pip -y\
    && pip install pydicom \
    && pip install numpy \
    && pip install scikit-image \
    && pip install matplotlib
COPY . /code/
COPY /brainDicom /home/
CMD [ "python","main.py" ]