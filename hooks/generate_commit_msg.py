#!/sbin/python3
import os
import subprocess
import sys
from enum import Enum

from absl import app
from absl import flags
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


class LLMType(Enum):
    GEMINI = "gemini"
    OLLAMA = "ollama"


FLAGS = flags.FLAGS
flags.DEFINE_enum(
    "llm",
    LLMType.OLLAMA.value,
    [llm.value for llm in LLMType],
    f"The LLM to use: {', '.join(f'\'{llm.value}\'' for llm in LLMType)}",
)


def main(argv):

    commit_msg_filepath = argv[1]

    if not os.path.exists(commit_msg_filepath):
        print(
            f"Error: The specified commit message file '{commit_msg_filepath}' does not exist.",
        )
        sys.exit(1)

    git_diff_command = "git diff --cached"

    # Use the current working directory as the repository path
    cwd = os.getcwd()

    # Execute the git diff command and get the output
    diff_output = subprocess.check_output(git_diff_command, shell=True, cwd=cwd).decode(
        "utf-8",
    )

    prompt = """
    Generate a raw text commit message for the following git diff.
    Keep commit message concise and to the point. Use imperative form of verbs.
    Make the first line the title (100 characters max) and the rest the body:

    This is the git diff output between two commits: \n\n {diff}

    AI OUTPUT:

    """

    llm = None
    if FLAGS.llm == LLMType.GEMINI.value:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key=os.environ.get("GEMINI_API_KEY"),
        )
    elif FLAGS.llm == LLMType.OLLAMA.value:
        llm = ChatOllama(
            base_url="https://llm.dodges.it",
            model="mistral-small3.2:latest",
            reasoning=False,
        )
    if not llm:
        exit(2)

    output_parser = StrOutputParser()
    PROMPT = PromptTemplate(template=prompt, input_variables=["diff"])
    chain = PROMPT | llm | output_parser

    results = chain.invoke({"diff": diff_output})

    with open(commit_msg_filepath, "r+") as f:
        f.seek(0, 0)
        f.write(results)


def entrypoint():
    app.run(main)


if __name__ == "__main__":
    entrypoint()
