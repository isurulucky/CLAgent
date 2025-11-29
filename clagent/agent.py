import json
import logging
from time import sleep

from tools import today, list_files, write_cover_letter, read_file, read_web_page, get_user_input

# logger = logging.getLogger('CLAgent')
# logging.basicConfig(level=logging.INFO)


class CLAgent:
    def __init__(self, sys_prompt_file_path, llm, max_iterations=10):
        self.max_iterations = max_iterations
        self.llm = llm
        with open(sys_prompt_file_path, "r") as file:
            sys_prompt_content = file.read()

        self.sys_prompt = [{
            "role": "system",
            "content": sys_prompt_content
        }]
        self.memory = []

    @staticmethod
    def extract_markdown_block(response, block_type="json"):
        if not '```' in response:
            return response

        code_block = response.split('```')[1].strip()

        if code_block.startswith(block_type):
            code_block = code_block[len(block_type):].strip()

        return code_block

    def parse_llm_response(self, response: str):
        try:
            response = self.extract_markdown_block(response, "action")
            response_json = json.loads(response)
            if "tool_name" in response_json and "args" in response_json:
                return response_json
            else:
                return {
                    "tool_name": "error",
                    "args": {
                        "message": "Invalid response. "
                                   "You must respond in JSON format tool invocation with 'tool_name' and 'args'."
                    }
                }
        except json.JSONDecodeError:
            return {
                "tool_name": "error",
                "args": {
                    "message": "Invalid JSON. "
                               "You must respond in JSON format tool invocation with 'tool_name' and 'args'."
                }
            }

    def loop(self, vacancy_url):
        iteration = 0
        print(f'Vacancy URL: {vacancy_url}')
        self.memory.extend([{"role": "user", "content": vacancy_url}])

        while iteration < self.max_iterations:
            # 1. Construct prompt: Combine agent rules with memory
            prompt = self.sys_prompt + self.memory
            # 2. Generate response from LLM
            response = self.llm.invoke(prompt)
            print(f"Agent response: {response}")
            sleep(2)
            # 3. Parse response to determine action
            action = self.parse_llm_response(response)
            tool_name = action["tool_name"]
            if tool_name == "list_files":
                result = {"result": list_files(action["args"]["path"])}
            elif tool_name == "read_file":
                result = {"result": read_file(action["args"]["file_path"])}
            elif tool_name == "read_web_page":
                result = {"result": read_web_page(action["args"]["url"])}
            elif tool_name == "ask_user":
                result = {"result": get_user_input(action["args"]["question"])}
            elif tool_name == "get_date_today":
                result = {"result": today()}
            elif tool_name == "output_cover_letter":
                result = {"result": write_cover_letter(action["args"]["content"])}
            elif tool_name == "terminate":
                print(action["args"]["message"])
                break
            elif tool_name == "error":
                result = {"error": action["args"]["message"]}
            else:
                result = {"error": "Unknown action: " + json.dumps(action)}

            print(f"Action result: {result}")

            # 6. Update memory with response and results
            self.memory.extend([
                {"role": "assistant", "content": response},
                {"role": "user", "content": json.dumps(result)}
            ])

            iteration += 1
