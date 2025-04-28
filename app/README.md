# MinerU Lambda PDF/Image Extraction

This project provides a serverless (AWS Lambda-ready) and Dockerizable solution for extracting text and structure from PDFs and images using MinerU (magic-pdf). It supports synchronous, asynchronous (stub), and S3 storage modes, and can be run locally for testing or deployed as a Lambda container.

---

## 1. Setup & Configuration

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- Docker (for containerization)
- AWS credentials (for S3 access, if using S3)

### Install Python Dependencies
```bash
cd app
pip install -r requirements.txt
```

### Download Models & Patch Config
Run the setup script to download required models and patch `magic-pdf.json`:
```bash
python setup_magic_pdf.py
```
- This will download models and update `magic-pdf.json` with device and LLM API key if set in environment variables.

### Configuration Files
- `magic-pdf.json`: Main config for magic-pdf (device, LLM, etc.)
- `mineru_config.json`: Language lists and LaTeX delimiters for UI

You can edit these files to customize behavior.

---

## 2. Local Testing

### Test Lambda Handler Locally
You can run the Lambda handler locally using the provided test script:
```bash
python test_lambda_local.py
```
- This will process a sample file (by default `examples/scanned.pdf`) and print results.
- Adjust environment variables in `test_lambda_local.py` as needed (e.g., S3 bucket, language, etc).

---

## 3. Running the Gradio UI (Optional)
If you want to use the web UI for manual testing:
```bash
python app.py
```
- This launches a Gradio web app for interactive PDF/image extraction.

---

## 4. Dockerization & Lambda Deployment

### Build Docker Image
From the project root:
```bash
docker build -t mineru-lambda .
```

### (Optional) Test Docker Image Locally
```bash
docker run --rm -it mineru-lambda
```

### Deploy to AWS Lambda
- Push the image to ECR and create a Lambda function using the container image.
- Set environment variables as needed (e.g., `MAGIC_PDF_CONFIG_PATH`, `DEVICE_MODE`, `LLM_API_KEY`, etc).

---

## 5. Lambda Handler Usage

The Lambda handler (`lambda_function.lambda_handler`) supports three modes:
- **sync**: Returns markdown in the response.
- **store**: Uploads markdown to S3 and returns the S3 URI.
- **async**: Returns a job ID (stub for future async processing).

**Example event for sync mode:**
```json
{
  "input_file": "s3://your-bucket/input.pdf",
  "mode": "sync",
  "end_pages": 10,
  "is_ocr": false,
  "layout_mode": "doclayout_yolo",
  "formula_enable": true,
  "table_enable": true,
  "language": "en"
}
```

---

## 6. Customization
- Edit `magic-pdf.json` and `mineru_config.json` for advanced configuration.
- Add your own test files to the `examples/` directory.

---

## 7. Troubleshooting
- Ensure all models are downloaded (rerun `python setup_magic_pdf.py` if needed).
- Check environment variables for correct config paths and device settings.
- Review logs for errors (set `LOG_LEVEL=DEBUG` for more details).

---

## References
- [MinerU GitHub](https://github.com/opendatalab/MinerU)
- [magic-pdf](https://github.com/opendatalab/MinerU/tree/dev/magic_pdf)
- [Gradio](https://gradio.app/)
- [AWS Lambda Container Images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)