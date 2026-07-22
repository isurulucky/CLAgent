import os
import unittest

from agent import CLAgent
from llm import LLM


class HardcodedLLM(LLM):
    def __init__(self):
        self.memory_item_count_to_tool = {
            2: '''
            ```action
                {
                    "tool_name": "read_web_page",
                    "args": {
                        "url": "https://gist.githubusercontent.com/isurulucky/28f38eeb1cf37763390ae6074093b735/raw/0e2035dbf6e5d82cade37fb90d0d94f6ab4d166d/gistfile1.txt"
                    }
                }```
            ''',
            4: '''
            ```action
                {
                    "tool_name": "list_files",
                    "args": {
                        "path": "./resources/cvs"
                    }
                }```
            ''',
            6: '''
            ```action
                {
                    "tool_name": "read_file",
                    "args": {
                        "file_path": "./resources/cvs/CV-John_Snow.pdf"
                    }
                }```
            ''',
            8: '''
            ```action
                {
                    "tool_name": "directory_exists",
                    "args": {
                        "path": "./resources/sample_cover_letters"
                    }
                }
            ```
            ''',
            10: '''
            ```action
                {
                    "tool_name": "list_files",
                    "args": {
                        "path": "./resources/sample_cover_letters"
                    }
                }```
            ''',
            12: '''
            ```action
                {
                    "tool_name": "read_file",
                    "args": {
                        "file_path": "./resources/sample_cover_letters/CL-John_Snow.txt"
                    }
                }```
            ''',
            14: '''
            ```action
                {
                    "tool_name": "get_date_today",
                    "args": {}
                }```
            ''',
            16: '''
            ```action
                {
                    "tool_name": "output_cover_letter",
                    "args": {
                        "content": "John Snow, M.D. \\nDear Hiring Committee, \\nI am writing to express my interest in the Clinical Research Physician–Epidemiologist position. \\nWith extensive experience as a physician, epidemiologist, and anesthesiologist, I bring a unique combination of clinical expertise, scientific rigor, and population-health insight that aligns strongly with the interdisciplinary nature of this role. \\nSincerely, \\nJohn Snow, M.D."
                    }
                }```
            ''',
            18: '''
            ```action
                {
                    "tool_name": "terminate",
                    "args": {
                        "message": "The cover letter for John Snow has been created and includes relevant details tailored to the Vacancy. Task completed successfully."
                    }
                }```
            '''
        }

    def invoke(self, messages):
        return self.memory_item_count_to_tool[len(messages)]


class TestAgent(unittest.TestCase):
    def test_loop(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        vacancy_url = 'https://gist.github.com/isurulucky/28f38eeb1cf37763390ae6074093b735'
        cv = './resources/CV-John_Snow.pdf'
        sample_cover_letters = './resources/sample_cover_letters'
        llm = HardcodedLLM()
        agent = CLAgent('./system.prompt', llm)
        agent.loop(vacancy_url, cv, sample_cover_letters)
