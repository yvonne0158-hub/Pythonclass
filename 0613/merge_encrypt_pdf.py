#!/usr/bin/env python3
from pathlib import Path
import argparse
from pypdf import PdfReader, PdfWriter


def collect_pdfs(inputs):
    files = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            files.extend(sorted(p.glob("*.pdf")))
        elif p.is_file() and p.suffix.lower() == ".pdf":
            files.append(p)
    return [f for f in files if f.exists()]


def merge_and_encrypt(pdf_files, output_file, password=None):
    writer = PdfWriter()

    for pdf_path in pdf_files:
        reader = PdfReader(str(pdf_path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as e:
                raise RuntimeError(f"無法解密檔案：{pdf_path}") from e

        for page in reader.pages:
            writer.add_page(page)

    if password:
        writer.encrypt(password)

    with open(output_file, "wb") as f:
        writer.write(f)


def main():
    parser = argparse.ArgumentParser(
        description="合併多個 PDF，並可選擇將輸出檔加密"
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="輸入 PDF 檔案或資料夾"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="merged.pdf",
        help="輸出檔名，預設 merged.pdf"
    )
    parser.add_argument(
        "-p",
        "--password",
        default=None,
        help="輸出 PDF 的密碼，若不填則不加密"
    )
    args = parser.parse_args()

    pdf_files = collect_pdfs(args.inputs)

    if not pdf_files:
        raise SystemExit("找不到可用的 PDF 檔案")

    merge_and_encrypt(pdf_files, args.output, args.password)
    print(f"完成：{args.output}")


if __name__ == "__main__":
    main()