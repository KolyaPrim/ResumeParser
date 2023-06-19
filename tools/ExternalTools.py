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


def convert_doc2docx(path: str, path_save: str = None) -> None:
    """
    Method convert doc to docx.
    :param path: Path to file.
    :param path_save: Path to save.
    :return: None.
    """

    if sys.platform in ("darwin", 'linux'):
        bashCommand = f"lowriter --convert-to docx {path} --outdir {path_save}"
        os.system(bashCommand)
    elif sys.platform == "win32":
        convert(path, path_save)


def get_list_files(path: str) -> List[str]:
    """
    Get list name from folder.
    :param path: Path to folder.
    :return: List with files name.
    """
    filelist = os.listdir(path)
    return filelist


def clear_folder(path: str) -> None:
    """
    Delete all files in folder.
    :param path: Path to folder.
    :return: None.
    """
    filelist = get_list_files(path=path)
    for file in filelist:
        os.remove(os.path.join(path, file))


def save_json(path: str, json_data) -> None:
    """
    Method for save data as json file.
    :param path: Path where the file will be created.
    :param json_data: Json data.
    :return: None
    """
    with open(path, "w", encoding="utf-8") as outfile:
        # print(json_data, file=outfile)
        json.dump(json_data, outfile)


def read_docx(path: str, path_save: str = None) -> str:
    """
    Method return a text from .doc or .docx
    :param path: Path to file.
    :param path_save: Path to save file.
    :return: Text from docx file.
    """
    if path.endswith(".doc"):
        convert_doc2docx(path=path, path_save=path_save)
        docx_text = docx2txt.process(path + "x")
    else:
        docx_text = docx2txt.process(path)
    return docx_text.strip()


def read_pdf(path: str) -> str:
    """
    Method return text from pdf.
    :param path: Path to file.
    :return: Text from pdf.
    """
    pdf_reader = PdfReader(path)
    pages_list = [page.extract_text() for page in pdf_reader.pages]
    pdf_text = "\n".join(pages_list)
    pdf_text = re.sub(REGEX_FOR_END_PAGE, '', pdf_text)
    return pdf_text.strip()


def read_rtf(path: str) -> str:
    """
    Method for read rtf.
    :param path: Path to file.
    :return Text from rtf.
    """
    with open(path, "r") as file:
        rtf_text = rtf_to_text(file.read())
    rtf_text = rtf_text.replace("|", "")
    return rtf_text.strip()


def get_text_from_file(file_path: str) -> str:
    """
    Method for get text from file with extension such as .doc, .docx, .pdf, .rtf
    :param file_path:
    :return:
    """
    text = ""
    if file_path.endswith(".doc") or file_path.endswith(".docx"):
        text = read_docx(file_path)
    elif file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.endswith(".rtf"):
        text = read_rtf(file_path)
    else:
        raise Exception("This extension is not supported")
    return text
