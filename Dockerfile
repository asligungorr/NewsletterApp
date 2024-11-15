# Use an official Python image as a base
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install python-dotenv to handle .env files
RUN pip install python-dotenv

# Copy the rest of the application code into the container
COPY . .
COPY .env .env


# Expose the port that Streamlit will run on
EXPOSE 8501

# Set Streamlit-specific environment variables to configure it for headless mode
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
