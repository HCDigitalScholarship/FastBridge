# Use an official Python runtime as a parent image
FROM python:3.11.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app 
#COPY FastBridge/FastBridgeApp /app/FastBridgeApp

#install all the requirements
RUN pip install --upgrade pip
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
