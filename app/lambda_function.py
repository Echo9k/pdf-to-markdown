"""
lambda_function.py
AWS Lambda handler for PDF/image text extraction using extractor.py and utils.py.
Supports 'sync', 'store', and 'async' (stub) modes.
"""
import os
import json
import uuid
from loguru import logger
from extractor import extract_to_markdown
from utils import download_from_s3, upload_to_s3, is_s3_uri

def lambda_handler(event, context):
    """
    Lambda handler for text extraction.
    Event must include:
      - 'input_file': local path or S3 URI
      - 'mode': 'sync', 'store', or 'async'
      - Extraction options (optional): end_pages, is_ocr, layout_mode, formula_enable, table_enable, language
      - For 'store' mode: 'output_s3_uri' (where to store the markdown)
    """
    logger.info(f"Received event: {json.dumps(event)}")
    mode = event.get('mode', 'sync')
    input_file = event.get('input_file')
    if not input_file:
        return {'statusCode': 400, 'body': 'Missing input_file'}

    # Download from S3 if needed
    if is_s3_uri(input_file):
        local_path = download_from_s3(input_file)
    else:
        local_path = input_file

    # Extraction options
    opts = {
        'end_pages': int(event.get('end_pages', 20)),
        'is_ocr': bool(event.get('is_ocr', False)),
        'layout_mode': event.get('layout_mode', 'doclayout_yolo'),
        'formula_enable': bool(event.get('formula_enable', True)),
        'table_enable': bool(event.get('table_enable', True)),
        'language': event.get('language', 'ch'),
    }

    # Extraction
    result = extract_to_markdown(local_path, **opts)
    markdown = result['markdown']
    md_path = result['md_path']

    if mode == 'sync':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/markdown; charset=utf-8'},
            'body': markdown
        }
    elif mode == 'store':
        output_s3_uri = event.get('output_s3_uri')
        if not output_s3_uri:
            return {'statusCode': 400, 'body': 'Missing output_s3_uri for store mode'}
        upload_to_s3(md_path, output_s3_uri)
        return {
            'statusCode': 200,
            'body': json.dumps({'output_s3_uri': output_s3_uri})
        }
    elif mode == 'async':
        # Stub: In production, trigger a background job and return a job ID
        job_id = str(uuid.uuid4())
        return {
            'statusCode': 202,
            'body': json.dumps({'job_id': job_id, 'status': 'queued'})
        }
    else:
        return {'statusCode': 400, 'body': f'Unknown mode: {mode}'}
