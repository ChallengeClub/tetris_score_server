FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY post_tetris_training_code.py ${LAMBDA_TASK_ROOT}
COPY tetris/ ${LAMBDA_TASK_ROOT}

# Copy requirements.subprocess.txt and install
COPY requirements.subprocess.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.subprocess.txt

# Copy requirements.txt and install
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "post_tetris_training_code.lambda_handler" ]