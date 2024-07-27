FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000

# Set the entry point to run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]