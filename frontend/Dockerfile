# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Environment variable for the backend URL (can be overridden in docker-compose)
ENV BACKEND_URL="http://backend:8000"

# Command to run Streamlit
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]