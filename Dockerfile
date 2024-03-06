#FROM python:3.7

#WORKDIR /app

#COPY requirements.txt /app/requirements.txt

#RUN pip install -r /app/requirements.txt

#COPY . /app

#EXPOSE 5000

#WORKDIR /app/FastBridgeApp
#CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}








#NEW TRY
# Use an official Python runtime as a parent image
FROM python:3.8.17

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app 
#COPY FastBridge/FastBridgeApp /app/FastBridgeApp

#install all the requirements
RUN pip install -r /app/requirements.txt

#change the working container directory to FastBridgeApp, so that the run command
#can find the app in main.py
WORKDIR /app/FastBridgeApp

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable for the port
ENV PORT 5001

# Command to run the application
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=5001"]
