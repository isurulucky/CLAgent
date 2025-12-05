import logging
import os

from agent import CLAgent
from cmdline import parse_args
from llm import OpenAILLM

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

if __name__ == '__main__':
    # parse commandline args
    args = parse_args()
    # mandatory environment variable LLM_API_KEY
    api_key = os.getenv("LLM_API_KEY")
    if api_key is None:
        raise ValueError("Environment variable LLM_API_KEY must be set.")

    llm = OpenAILLM(api_key)
    agent = CLAgent(args.sys_prompt_file_path, llm)
    agent.loop(args.vacancy_url)
