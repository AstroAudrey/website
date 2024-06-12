FROM python:3.10-bookworm

# Update the package lists and install necessary dependencies
RUN apt-get update 

# Install Python dependencies
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Copy the application code
COPY ./src /app

# Expose port if needed
EXPOSE 5050

# Set the display number to use Xvfb
ENV DISPLAY=:99
ENV TZ=America/Denver

# Define the command to run the application with Xvfb
CMD xvfb-run --auto-servernum --server-args='-screen 0 1280x1024x24' python /app/main.py