FROM python:3.12-slim

# Match host UID/GID so bind-mounted files stay editable outside the container.
# A real home directory is required for Cursor/VS Code server installation.
ARG UID=1000
ARG GID=1000
RUN groupadd --gid "${GID}" dev \
    && useradd --uid "${UID}" --gid "${GID}" --create-home --shell /bin/bash dev

# Install system-level dependencies:
#   build-essential  – C compiler for Python packages with native extensions
#   dnsutils         – dig/nslookup for DNS debugging inside the container
#   curl             – health checks and general network debugging
#   git              – version control (required by Cursor/VS Code)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        dnsutils \
        curl \
        git \
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
