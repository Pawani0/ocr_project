FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 10000

# Run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
