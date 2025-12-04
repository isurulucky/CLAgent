import json
from time import sleep

from const import *
from tools import *


class LLMResponseFormatError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnkownActionError(Exception):
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
            raise UnkownActionError(f"Unknown tool: {json.dumps(action)}")
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
                # return {
                #     TOOL_NAME: "error",
                #     "args": {
                #         "message": "Invalid response. "
                #                    "You must respond in JSON format tool invocation with 'tool_name' and 'args'."
                #     }
                # }
                raise LLMResponseFormatError(f"Invalid response. You must respond in JSON format tool invocation "
                                             f"with {TOOL_NAME} and {ARGS}")
        except json.JSONDecodeError:
            # return {
            #     TOOL_NAME: "error",
            #     "args": {
            #         "message": "Invalid JSON. "
            #                    "You must respond in JSON format tool invocation with 'tool_name' and 'args'."
            #     }
            # }
            raise LLMResponseFormatError(f"Invalid JSON. You must respond in JSON format tool invocation "
                                         f"with {TOOL_NAME} and {ARGS}")

    def loop(self, vacancy_url):
        iteration = 0
        print(f'Vacancy URL: {vacancy_url}')
        self.extend_memory(USER, vacancy_url)

        while iteration < self.max_iterations:
            # 1. Construct prompt: Combine agent rules with memory
            prompt = self.sys_prompt + self.memory

            # 2. Generate response from LLM
            response = self.llm.invoke(prompt)
            print(f"Agent response: {response}")
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
                result = self.execute_action(action)
            except UnkownActionError as e:
                self.extend_user_and_assistant_memory(
                    response,
                    {
                        RESULT: f"error: {e.message}"
                    })
                continue

            print(f"Action result: {result}")

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
