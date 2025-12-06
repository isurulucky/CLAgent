import json
import logging
import os
from datetime import date
from time import sleep

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

logger = logging.getLogger(__name__)

# tools
OUTPUT_COVER_LETTER = "output_cover_letter"
DATE_TODAY = "get_date_today"
ASK_USER = "ask_user"
READ_WEB_PAGE = "read_web_page"
READ_FILE = "read_file"
LIST_FILES = "list_files"
DIRECTORY_EXISTS = "directory_exists"
TERMINATE = "terminate"

# other constants
ARGS = "args"
ACTION = "action"
USER = "user"
RESULT = "result"
TOOL_NAME = "tool_name"
SYSTEM = "system"
CONTENT = "content"
ROLE = "role"
ASSISTANT = "assistant"


class LLMResponseFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownActionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CLAgent:
    def __init__(self, sys_prompt_file_path, llm, max_iterations=10):
        self.max_iterations = max_iterations
        self.llm = llm
        with open(sys_prompt_file_path, "r") as file:
            sys_prompt_content = file.read()

        self.sys_prompt = [{
            ROLE: SYSTEM,
            CONTENT: sys_prompt_content
        }]
        self.memory = []
        self.tool_to_action = {
            DIRECTORY_EXISTS: directory_exists,
            LIST_FILES: list_files,
            READ_FILE: read_file,
            READ_WEB_PAGE: read_web_page,
            ASK_USER: get_user_input,
            DATE_TODAY: today,
            OUTPUT_COVER_LETTER: write_cover_letter,
            TERMINATE: terminate,
        }

    def execute_action(self, action):
        tool_name = action[TOOL_NAME]
        args = action[ARGS]
        if tool_name not in self.tool_to_action:
            raise UnknownActionError(f"Unknown tool: {json.dumps(action)}")
        return self.tool_to_action[tool_name](**args)

    @staticmethod
    def extract_markdown_block(response, block_type="json"):
        if not '```' in response:
            return response

        code_block = response.split('```')[1].strip()

        if code_block.startswith(block_type):
            code_block = code_block[len(block_type):].strip()

        return code_block

    def parse_llm_response(self, response):
        try:
            response = self.extract_markdown_block(response, ACTION)
            response_json = json.loads(response)
            if TOOL_NAME in response_json and ARGS in response_json:
                return response_json
            else:
                raise LLMResponseFormatError(f"Invalid response. You must respond in JSON format tool invocation "
                                             f"with {TOOL_NAME} and {ARGS}")
        except json.JSONDecodeError:
            raise LLMResponseFormatError(f"Invalid JSON. You must respond in JSON format tool invocation "
                                         f"with {TOOL_NAME} and {ARGS}")

    def loop(self, vacancy_url, cv_path, sample_cover_letter_dir):
        iteration = 0

        self.sys_prompt[0][CONTENT] = (self.sys_prompt[0][CONTENT].
                                       replace('__CV_PATH__', cv_path))
        if sample_cover_letter_dir.strip() == '':
            # specify a non-existing directory, the existence will be checked by the agent
            sample_cover_letter_dir = './non_existing_cover_letter_dir'
        self.sys_prompt[0][CONTENT] = (self.sys_prompt[0][CONTENT].
                                       replace('__SAMPLE_COVER_LETTER_DIR__', sample_cover_letter_dir))

        self.extend_memory(USER, vacancy_url)

        while iteration < self.max_iterations:
            # 1. Construct prompt: Combine agent rules with memory
            prompt = self.sys_prompt + self.memory

            # 2. Generate response from LLM
            response = self.llm.invoke(prompt)
            logger.info(f"LLM response: {response}")
            iteration += 1

            # 3. Parse response to determine action
            try:
                action = self.parse_llm_response(response)
            except LLMResponseFormatError as e:
                self.extend_user_and_assistant_memory(
                    response,
                    {
                        RESULT: f"error: {e.message}"
                    })
                continue

            # 4. Carry out the action and capture the result
            try:
                result, terminate_loop = self.execute_action(action)
            except UnknownActionError as e:
                self.extend_user_and_assistant_memory(
                    response,
                    {
                        RESULT: f"error: {e.message}"
                    })
                continue
            if terminate_loop:
                break

            logger.info(f"Action result: {result}")

            # 5. Update memory with response and results
            self.extend_user_and_assistant_memory(response, json.dumps(result))

            # Keep a time gap between API calls
            sleep(2)

    def extend_user_and_assistant_memory(self, asst_msg, user_msg):
        self.extend_memory(ASSISTANT, asst_msg)
        self.extend_memory(USER, user_msg)

    def extend_memory(self, role_name, content):
        self.memory.extend([
            {
                ROLE: role_name, CONTENT: content
            },
        ])


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
