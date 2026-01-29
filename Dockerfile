FROM python:3.10-slim

# Hugging Face Spaces expects uid 1000
RUN useradd -m -u 1000 user
USER user
WORKDIR /app
ENV PATH="/home/user/.local/bin:$PATH" PORT=7860

# Single unified requirements file at repo root
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt


# Copy entire repo 
COPY --chown=user . /app

# Launch Streamlit from root directory
CMD ["streamlit", "run", "ui/Overview.py", "--server.port", "7860", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
