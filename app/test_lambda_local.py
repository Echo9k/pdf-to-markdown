import json
import os
import sys
from lambda_function import lambda_handler # Import the handler

# --- Configuration ---
# Set environment variables needed by the lambda function
# Adjust these values according to your setup
os.environ['OUTPUT_BUCKET'] = 'your-output-s3-bucket-name' # CHANGE THIS
os.environ['OUTPUT_PREFIX'] = 'lambda-test-output/'      # CHANGE THIS (Optional)
os.environ['MAX_PAGES'] = '5'                            # Example: Limit pages for testing
os.environ['FORCE_OCR'] = 'False'
os.environ['LAYOUT_MODE'] = 'doclayout_yolo'
os.environ['FORMULA_ENABLE'] = 'True'
os.environ['TABLE_ENABLE'] = 'True'
os.environ['LANGUAGE'] = 'en'                            # Example: Use 'en' or 'ch' etc.
os.environ['LOG_LEVEL'] = 'DEBUG'                        # More verbose logging for testing
os.environ['MINERU_TOOLS_CONFIG_JSON'] = os.path.abspath('magic-pdf.json')
os.environ['MAGIC_PDF_CONFIG_PATH'] = 'magic-pdf.json'  # Correct config path for local test
# os.environ['LLM_API_KEY'] = 'your_llm_api_key' # If using LLM features

# --- Simulate S3 Event ---
# For local testing, use a real file from examples and set LOCAL_TEST_INPUT_PATH
os.environ['LOCAL_TEST_INPUT_PATH'] = 'examples/scanned.pdf'  # Use a real local file for autonomous test
input_bucket_name = 'dummy-bucket'  # Not used in local mode
input_object_key = 'dummy-key'      # Not used in local mode

# Use direct event for local test (bypass S3 event)
event = {
    "input_file": os.environ['LOCAL_TEST_INPUT_PATH'],
    "mode": "sync",
    "end_pages": int(os.environ['MAX_PAGES']),
    "is_ocr": os.environ['FORCE_OCR'].lower() == 'true',
    "layout_mode": os.environ['LAYOUT_MODE'],
    "formula_enable": os.environ['FORMULA_ENABLE'].lower() == 'true',
    "table_enable": os.environ['TABLE_ENABLE'].lower() == 'true',
    "language": os.environ['LANGUAGE']
}

# --- Simulate Lambda Context (Optional) ---
# The lambda_function.py doesn't seem to use the context object,
# but you can create a dummy one if needed.
class DummyContext:
    def __init__(self):
        self.function_name = 'local_test_function'
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:local_test_function'
        self.aws_request_id = 'local_test_request_id'

lambda_context = DummyContext()

# --- Execute the Handler ---
if __name__ == "__main__":
    print(f"--- Starting local Lambda test (sync mode, local file) ---")
    print(f"Input File: {event['input_file']}")
    print(f"--- Calling lambda_handler ---")
    try:
        result = lambda_handler(event, lambda_context)
        print(f"--- Lambda handler finished ---")
        print(f"Result: {json.dumps(result, indent=2)}")
        if result.get('statusCode') == 200:
            print("\nSuccess! Markdown output (truncated):\n")
            print(result['body'][:1000] + ('...' if len(result['body']) > 1000 else ''))
        else:
            print("\nError occurred during execution. Check logs above.")
    except Exception as e:
        print(f"--- Unhandled exception during test execution ---")
        import traceback
        traceback.print_exc()
