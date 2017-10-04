FROM ubuntu:14.04

# Set the working directory to /analyser
WORKDIR /analyser
RUN sudo apt-get update

# Install python and tools
RUN apt-get install -y --force-yes python python-dev python-setuptools software-properties-common gcc python-pip
RUN pip install psutil
#RUN pip install pyzmq
RUN pip install Flask

# Zmq Sub Server
#EXPOSE 5100
EXPOSE 5000
# Copy the current directory contents into the container at /analyser
ADD . /analyser
CMD ["python", "analyser.py"]


