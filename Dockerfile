# Dockerfile for AWS Lambda Python 3.12 with magic-pdf and dependencies
FROM public.ecr.aws/lambda/python:3.12

# Install system dependencies (if needed)
RUN yum install -y gcc git && rm -rf /var/cache/yum

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . ./
RUN python setup_magic_pdf.py
# Set environment variables (override as needed in Lambda console)
ENV MAGIC_PDF_CONFIG_PATH=magic-pdf.json

# Set the Lambda handler
CMD ["lambda_function.lambda_handler"]
