# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /Yt_Video_Summarization

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Set environment variable for Streamlit to run in production mode
ENV STREAMLIT_SERVER_PORT=8501

# Run the Streamlit app
CMD ["streamlit", "run", "Yt_Video_Summarization.py"]
