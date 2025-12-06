# CLAgent
A simple agentic commandline app to create cover letters, given a CV and a public vacancy URL. 
Currently, the app depends on OpenAI GPT APIs to access LLM functionality. 
The finalized cover letter is written to the standard output. 

### How to Use

- Install the dependencies with ```pip install -r requirements.txt```.
- Navigate to ```clagent``` directory.
- Generate your OpenAI API key, and set it as the value of the environment variable ```LLM_API_KEY``` by running ```export LLM_API_KEY=xxx```.
- Run as a commandline app, using ```python clagent_app.py```. The following arguments are supported:

    - Mandatory ```--vacancy-url```: URL of the public vacancy post.
    - Mandatory ```--cv```: absolute path to the CV file. Currently only PDF and text files are accepted.
    - Optional ```--sample-cover-letter-dir```: absolute path to a directory containing sample cover letters.
    - Optional ```--llm-model```: LLM mode to use, for example ```openai/gpt-5.1```. Defaults to ```gpt-4o``` for OpenAI.
    - Optional ```--sys-prompt-file-path```: path to a file containing main system prompt. See the existing system prompt in ```system.prompt``` file for modifications.

If the application is unable to read the vacancy URL or the CV for any reason, it will prompt the user to enter the information manually via standard input.
In such cases, the content of the vacancy page or CV should be copied and reformatted to remove line breaks before being provided as input to the application. 
This can be done using any online text-formatting tool available through a web search.

A sample command for reference:

```python clagent_app.py --cv ./resources/cvs/CV-John_Snow.pdf --vacancy-url https://gist.githubusercontent.com/isurulucky/28f38eeb1cf37763390ae6074093b735/raw/0e2035dbf6e5d82cade37fb90d0d94f6ab4d166d/gistfile1.txt --sample-cover-letter-dir ./resources/sample_cover_letters```

Tested with Python 3.11.5.
