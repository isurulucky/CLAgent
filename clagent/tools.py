import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
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


def read_html_web_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.text.encode('ascii', errors='ignore').decode(), False


def read_js_web_page(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, "html.parser")

        for script_or_style in soup(["script", "style", "noscript"]):
            script_or_style.decompose()

        raw_text = soup.get_text(separator=' ', strip=True)
        clean_text = raw_text.encode('ascii', errors='ignore').decode()

        return clean_text, False

    except PlaywrightTimeoutError:
        return f"Error: Page load timed out for {url}", False
    except Exception as e:
        return f"Error reading JS page: {str(e)}", False


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
