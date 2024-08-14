# Use the Python image
FROM python:3.12-slim

# Set the work directory to /app
WORKDIR /app

# Copy the requirements from the txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code from the app
COPY app/ ./app/
COPY tests/ ./tests/

# Copy other necessary files
COPY run.py .
COPY README.md .

# Expose the port that will run the app
EXPOSE 5000

# Command for executing the app
CMD ["python", "run.py"]