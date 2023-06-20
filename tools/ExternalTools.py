import json
import os
import re
from typing import List
import sys
import docx2txt
from PyPDF2 import PdfReader
from doc2docx import convert
from striprtf.striprtf import rtf_to_text

REGEX_FOR_END_PAGE = r'(\n|\s)Резюме обновлено\s.+'


def convert_doc2docx(file: str, path_save: str = None) -> None:
    """
    Method convert doc to docx.
    :param file: Path to file.
    :param path_save: Path to save.
    :return: None.
    """
    temp_dir = os.path.join(path_save, 'temp_files')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if sys.platform in ("darwin", 'linux'):
        bash_command = f"soffice --convert-to docx {file} --outdir {temp_dir}"
        os.system(bash_command)
    elif sys.platform == "win32":
        convert(file, temp_dir)


def get_list_files(path: str) -> List[str]:
    """
    Get list name from folder.
    :param path: Path to folder.
    :return: List with files name.
    """
    filelist = os.listdir(path)
    return filelist


def delete_file(path: str) -> None:
    """
    Delete file.
    :param path: Path to file.
    :return: None.
    """
    os.remove(path)


def clear_folder(path: str) -> None:
    """
    Delete all files in folder.
    :param path: Path to folder.
    :return: None.
    """
    filelist = get_list_files(path=path)
    for file in filelist:
        delete_file(os.path.join(path, file))


def delete_folder(path: str) -> None:
    """
    Delete all files in folder.
    :param path: Path to folder.
    :return: None.
    """
    clear_folder(path=path)
    os.rmdir(path=path)


def save_json(path: str, json_data) -> None:
    """
    Method for save data as json file.
    :param path: Path where the file will be created.
    :param json_data: Json data.
    :return: None
    """
    with open(path, "w", encoding="utf-8") as outfile:
        json.dump(json_data, outfile)


def read_docx(file: str, path_save: str = None) -> str:
    """
    Method return a text from .doc or .docx
    :param path: Path to file.
    :param path_save: Path to save file.
    :return: Text from docx file.
    """
    if file.endswith(".doc"):
        convert_doc2docx(file=file, path_save=path_save)

        file_name = os.path.basename(file)
        temp_dir = os.path.join(path_save, 'temp_files')
        path_to_file = os.path.join(temp_dir, file_name)

        docx_text = docx2txt.process(path_to_file + "x")
        delete_folder(temp_dir)

    else:
        docx_text = docx2txt.process(file)
    return docx_text.strip()


def read_pdf(file: str) -> str:
    """
    Method return text from pdf.
    :param file: Path to file.
    :return: Text from pdf.
    """
    pdf_reader = PdfReader(file)
    pages_list = [page.extract_text() for page in pdf_reader.pages]
    pdf_text = "\n".join(pages_list)
    pdf_text = re.sub(REGEX_FOR_END_PAGE, '', pdf_text)
    return pdf_text.strip()


def read_rtf(file: str) -> str:
    """
    Method for read rtf.
    :param file: Path to file.
    :return Text from rtf.
    """
    with open(file, "r") as file:
        rtf_text = rtf_to_text(file.read())
    rtf_text = rtf_text.replace("|", "")
    return rtf_text.strip()


def get_text_from_file(file_path: str, path_save: str) -> str:
    """
    Method for get text from file with extension such as .doc, .docx, .pdf, .rtf
    :param file_path: Path to file.
    :param path_save: Path where file will be save.
    :return:
    """
    if file_path.endswith(".doc") or file_path.endswith(".docx"):
        text = read_docx(file=file_path, path_save=path_save)
    elif file_path.endswith(".pdf"):
        text = read_pdf(file=file_path)
    elif file_path.endswith(".rtf"):
        text = read_rtf(file=file_path)
    else:
        raise Exception("This extension is not supported")
    return text
