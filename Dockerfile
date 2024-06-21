# Use the `python:3.7` as a source image from the Amazon ECR Public Gallery
# We are not using `python:3.7.2-slim` from Dockerhub because it has put a  pull rate limit. 
# FROM public.ecr.aws/sam/build-python3.12:latest as builder

# # Set up an app directory for your code
# COPY . /app
# WORKDIR /app

# # Install `pip` and needed Python packages from `requirements.txt`
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt


FROM python:3.9.19-slim as app
# COPY --from=builder /root/.local /root/.local1
# COPY --from=builder /app .
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PATH=/root/.local:$PATH

ENTRYPOINT ["python", "app.py"]
