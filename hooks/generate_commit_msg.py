#!/usr/bin/env python3
import os
import subprocess
import sys

from absl import app
from absl import flags
from absl import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from lib import llm

FLAGS = flags.FLAGS


def set_logging_verbosity():
    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
    else:
        logging.set_verbosity(logging.ERROR)


def main(argv):
    set_logging_verbosity()
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

    try:
        llm_engine = llm.new()
    except ValueError as e:
        logging.error("Cannot instantiate LLM: %s", e)
        exit(1)

    output_parser = StrOutputParser()
    PROMPT = PromptTemplate(template=prompt, input_variables=["diff"])
    chain = PROMPT | llm_engine | output_parser

    results = chain.invoke({"diff": diff_output})

    with open(commit_msg_filepath, "r+") as f:
        f.seek(0, 0)
        f.write(results)


def entrypoint():
    app.run(main)


if __name__ == "__main__":
    entrypoint()
