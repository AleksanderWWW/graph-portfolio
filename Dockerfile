FROM python:3.11-alpine

# Set environment variables for security & non-root execution
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create a non-root user and group + add the user to this group
RUN addgroup --system appgroup && adduser --system appuser appgroup

# Set working directory
WORKDIR /app

COPY deploy/requirements.txt requirements.txt

# Install dependencies first, so they are cached
RUN pip install -r requirements.txt

# Copy remaining files - neccesary to build and run
COPY pyproject.toml README.md ./
ADD src src

# Install graph_portfolio package
RUN pip install .

# Change ownership of the working directory & switch to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Entrypoint - litserve server
ENTRYPOINT ["python", "-u", "src/graph_portfolio/api.py"]
