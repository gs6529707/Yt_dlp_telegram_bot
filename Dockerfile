# Use a base Python image
FROM python:3.9-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy your requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port (if needed, for example, if you're running a web server)
EXPOSE 8080

# Run your application
CMD ["python", "your_script.py"]
