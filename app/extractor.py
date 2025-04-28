"""
extractor.py
Core extraction logic for PDF/image to markdown (and JSON for multi-sheet PDFs).
No UI code. Designed for Lambda or CLI use.
"""
import os
import time
import uuid
import zipfile
from pathlib import Path
import pymupdf
from loguru import logger
from magic_pdf.data.data_reader_writer import FileBasedDataReader
from magic_pdf.libs.hash_utils import compute_sha256
from magic_pdf.tools.common import do_parse, prepare_env


def read_fn(path):
    disk_rw = FileBasedDataReader(os.path.dirname(path))
    return disk_rw.read(os.path.basename(path))


def parse_pdf(doc_path, output_dir, end_page_id, is_ocr, layout_mode, formula_enable, table_enable, language):
    os.makedirs(output_dir, exist_ok=True)
    try:
        file_name = f"{str(Path(doc_path).stem)}_{time.time()}"
        pdf_data = read_fn(doc_path)
        parse_method = "ocr" if is_ocr else "auto"
        local_image_dir, local_md_dir = prepare_env(output_dir, file_name, parse_method)
        do_parse(
            output_dir,
            file_name,
            pdf_data,
            [],
            parse_method,
            False,
            end_page_id=end_page_id,
            layout_model=layout_mode,
            formula_enable=formula_enable,
            table_enable=table_enable,
            lang=language,
            f_dump_orig_pdf=False,
        )
        return local_md_dir, file_name
    except Exception as e:
        logger.exception(e)
        raise


def compress_directory_to_zip(directory_path, output_zip_path):
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)
        return 0
    except Exception as e:
        logger.exception(e)
        return -1


def to_pdf(file_path):
    with pymupdf.open(file_path) as f:
        if f.is_pdf:
            return file_path
        else:
            pdf_bytes = f.convert_to_pdf()
            unique_filename = f"{uuid.uuid4()}.pdf"
            tmp_file_path = os.path.join(os.path.dirname(file_path), unique_filename)
            with open(tmp_file_path, 'wb') as tmp_pdf_file:
                tmp_pdf_file.write(pdf_bytes)
            return tmp_file_path


def extract_to_markdown(
    file_path,
    end_pages=20,
    is_ocr=False,
    layout_mode="doclayout_yolo",
    formula_enable=True,
    table_enable=True,
    language="ch"
):
    file_path = to_pdf(file_path)
    if end_pages > 20:
        end_pages = 20
    local_md_dir, file_name = parse_pdf(
        file_path, './output', end_pages - 1, is_ocr,
        layout_mode, formula_enable, table_enable, language
    )
    archive_zip_path = os.path.join("./output", compute_sha256(local_md_dir) + ".zip")
    zip_archive_success = compress_directory_to_zip(local_md_dir, archive_zip_path)
    if zip_archive_success == 0:
        logger.info("Archive success")
    else:
        logger.error("Archive failed")
    md_path = os.path.join(local_md_dir, file_name + ".md")
    with open(md_path, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    # For multi-sheet PDFs, you could split here and return a dict
    return {
        "markdown": txt_content,
        "archive_zip": archive_zip_path,
        "md_path": md_path,
        "output_pdf": os.path.join(local_md_dir, file_name + "_layout.pdf")
    }
