FROM python:3.12-slim

# Install system-level dependencies:
#   build-essential  – C compiler for Python packages with native extensions
#   dnsutils         – dig/nslookup for DNS debugging inside the container
#   curl             – health checks and general network debugging
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        dnsutils \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

EXPOSE 8501

# Default command: run the Streamlit app.
# The devcontainer overrides this with "sleep infinity" for interactive dev.
CMD ["streamlit", "run", "streamlit_email.py", "--server.port=8501", "--server.address=0.0.0.0"]
