#!/sbin/python3
import os
import subprocess
import sys

from absl import app
from absl import flags
from absl import logging
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from rich.console import Console
from rich.markdown import Markdown

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "ollama_base_url",
    "http://localhost:11434",
    "The URL of the ollama server",
)
flags.DEFINE_string("llm", "ollama", "The LLM to use: either 'ollama' or 'gemini'")
flags.DEFINE_string(
    "model",
    "mistral-small3.2:latest",
    "The LLM model to use, e.g. 'gemini-2.5-flash'",
)
flags.DEFINE_string("api_key", "", "The API key to use when querying Gemini")
flags.DEFINE_bool("debug", False, "Activate debug logging")


prompt = """
You are an expert developer and git super user.
You do code reviews based on the git diff output between two commits.
Complete the following tasks, write in markdown, and be extremely critical and precise in your review:
* [Description] Describe the code change.
* [Obvious errors] Look for obvious errors in the code.
* [Improvements] Suggest improvements where relevant.
* [Friendly advice] Give some friendly advice or heads up where relevant.
* [Stop when done] Stop when you are done with the review.

This is the git diff output between two commits: \n\n {diff}

AI OUTPUT:

"""


def new_llm() -> ChatGoogleGenerativeAI | ChatOllama:
    if FLAGS.llm == "gemini":
        if not FLAGS.api_key:
            raise ValueError('--api_key must be set when --llm is "gemini"')
        return ChatGoogleGenerativeAI(
            model=FLAGS.model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key=FLAGS.api_key,
        )
    elif FLAGS.llm == "ollama":
        return ChatOllama(
            base_url=FLAGS.ollama_base_url,
            model=FLAGS.model,
            reasoning=False,
        )
    raise ValueError('--llm should be either "gemini" or "ollama"')


def set_logging_verbosity():
    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
    else:
        logging.set_verbosity(logging.ERROR)


def git_diff(prev: str, next: str) -> str:
    git_diff_command = f"git diff {prev} {next}"
    raw_output = subprocess.check_output(git_diff_command, shell=True, cwd=os.getcwd())
    return raw_output.decode("utf-8")


def main(argv):
    del argv
    print(os.environ)
    set_logging_verbosity()

    console = Console()
    try:
        diff_output = git_diff(prev=sys.argv[1], next=sys.argv[2])
    except subprocess.CalledProcessError as e:
        logging.error("Calling 'git diff' failed with error: %s", e.output)
        exit(1)

    try:
        llm = new_llm()
    except ValueError as e:
        logging.error("Cannot instantiate LLM: %s", e)
        exit(1)

    output_parser = StrOutputParser()
    PROMPT = PromptTemplate(template=prompt, input_variables=["diff"])
    chain = PROMPT | llm | output_parser

    print("Running diffs...")
    results = chain.invoke({"diff": diff_output})

    md = Markdown(results)
    console.print(md)


def entrypoint():
    app.run(main)


if __name__ == "__main__":
    entrypoint()
