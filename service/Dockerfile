# Use an official Python runtime as a parent image
FROM python:3.6-slim

# run as user prod
RUN useradd prod -d /home/prod && mkdir /home/prod && chown -R prod.prod /home/prod
USER prod

# Set the working directory to /app
WORKDIR /home/prod

# Copy contents into the container at /app
COPY is_flappy.py /home/prod
COPY requirements.txt /home/prod

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt --user
ENV PATH /home/prod/.local/bin

# Make port 9001 available to the world outside this container
EXPOSE 9001

# Run is_flappy when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9001", "is_flappy:app", "--log-level", "debug"]
