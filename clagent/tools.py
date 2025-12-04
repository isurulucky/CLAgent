import os
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def list_files(path):
    return os.listdir(path)


def read_file(file_path):
    content = ''
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += f'{page.extract_text()}\n'
        reader.close()
    else:
        file = open(file_path, "r")
        content = file.read()
        file.close()
    return content.encode('ascii', errors='ignore').decode()


def read_web_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.text.encode('ascii', errors='ignore').decode()


def get_user_input(question):
    return input(question)


def today():
    t = date.today()
    return t.strftime("%B %d, %Y")


def write_cover_letter(content):
    print(content)
    return "cover letter content written"


def terminate(message):
    print(message)
    sys.exit(0)
