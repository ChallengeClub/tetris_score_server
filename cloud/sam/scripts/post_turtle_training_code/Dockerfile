FROM python:3.10-slim-bullseye
ARG FUNCTION_DIR="/function"
RUN apt-get update && apt-get install -y \
    xvfb python-tk x11-apps
ENV PYTHONUNBUFFERED 1

# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric CairoSVG

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy function code
COPY post_turtle_training_code.py ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "post_tetris_training_code.lambda_handler" ]