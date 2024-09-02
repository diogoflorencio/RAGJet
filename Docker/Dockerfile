FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

# maintainer
LABEL maintainer="diogo.lima@ccc.ufcg.edu.br"

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Expose port 8883
EXPOSE 8883

# Work directory
WORKDIR /workspace

# Install dependencies
COPY llm-requirements.txt .
RUN pip install --no-cache-dir -r llm-requirements.txt

# Copy application code
COPY . .

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8883"]
