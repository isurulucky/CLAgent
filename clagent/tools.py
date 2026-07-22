import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from datetime import date
import os


def directory_exists(path):
    return os.path.isdir(path), False


def list_files(path):
    return os.listdir(path), False


def read_file(file_path):
    content = ''
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += f'{page.extract_text()}\n'
        reader.close()
    elif file_path.endswith(".txt"):
        file = open(file_path, "r")
        content = file.read()
        file.close()
    else:
        return "", False
    return content.encode('ascii', errors='ignore').decode(), False


def read_web_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.text.encode('ascii', errors='ignore').decode(), False


def get_user_input(question):
    return input(question), False


def today():
    t = date.today()
    return t.strftime("%B %d, %Y"), False


def write_cover_letter(content):
    print(content)
    return "cover letter content written", False


def terminate(message):
    print(message)
    return None, True
