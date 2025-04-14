# Use an official Python image with Debian (supports apt-get)
FROM python:3.10-slim

# Install Poppler (for pdf2image)
RUN apt-get update && apt-get install -y poppler-utils

# Set working directory
WORKDIR /app

# Copy app files
COPY ./pdf_to_image /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render
ENV PORT=10000
EXPOSE $PORT

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
