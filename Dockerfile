# Use official samtools base image
FROM --platform=linux/arm64 staphb/samtools:1.18

# Set working directory
WORKDIR /app

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files
COPY pyproject.toml ./
COPY samtools_mcp.py ./
COPY main.py ./

# Install Python dependencies
RUN pip3 install --no-cache-dir typer pydantic

# Create a non-root user
RUN useradd -m -s /bin/bash mcp_user && \
    chown -R mcp_user:mcp_user /app

# Switch to non-root user
USER mcp_user

# Set environment variables
ENV PYTHONPATH=/app

# Command to run the MCP
CMD ["python3", "main.py"]