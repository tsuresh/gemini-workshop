# Use a slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Command to run the app (assuming your entry point is app.py)
CMD [ "python", "basic_prompt_ui.py" ]