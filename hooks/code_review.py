#!/usr/bin/env python3
import os
import subprocess

from absl import app
from absl import flags
from absl import logging
from httpx import ConnectError
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from rich.console import Console
from rich.markdown import Markdown

from lib import llm


FLAGS = flags.FLAGS
flags.DEFINE_string(
    "stage",
    "pre-commit",
    "Either 'pre-commit' or 'pre-merge-commit'. Modifies the git diff command to send the right diff to the LLM.",
)

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


def set_logging_verbosity():
    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
    else:
        logging.set_verbosity(logging.ERROR)


def git_diff_merge_command() -> str:
    try:
        # The commit hash of the branch being merged is in .git/MERGE_HEAD
        with open(".git/MERGE_HEAD") as f:
            next_commit = f.read()
    except FileNotFoundError:
        raise RuntimeError(".git/MERGE_HEAD not found. Is this a merg commit?")

    # The commit hash of the branch being merged into is in HEAD
    prev_commit = subprocess.check_output(
        "git rev-parse HEAD",
        shell=True,
        cwd=os.getcwd(),
    ).decode("utf-8")
    return f"git diff {prev_commit} {next_commit}"


def git_diff() -> str:
    if FLAGS.stage == "pre-commit":
        git_diff_command = "git diff --cached"
    elif FLAGS.stage == "pre-merge-commit":
        git_diff_command = git_diff_merge_command()
    else:
        raise ValueError(
            f"Invalid stage value '{FLAGS.stage}'. Must be either 'pre-commit' or 'pre-merge-commit'",
        )

    raw_output = subprocess.check_output(git_diff_command, shell=True, cwd=os.getcwd())
    return raw_output.decode("utf-8")


def main(argv):
    del argv
    set_logging_verbosity()

    console = Console()
    try:
        diff_output = git_diff()
    except subprocess.CalledProcessError as e:
        logging.error("Calling 'git diff' failed with error: %s", e.output)
        exit(1)

    try:
        llm_engine = llm.new()
    except ValueError as e:
        logging.error("Cannot instantiate LLM: %s", e)
        exit(1)

    output_parser = StrOutputParser()
    PROMPT = PromptTemplate(template=prompt, input_variables=["diff"])
    chain = PROMPT | llm_engine | output_parser

    print("Running diffs...")
    try:
        results = chain.invoke({"diff": diff_output})
    except ConnectError as e:
        logging.error("Cannot send request to LLM: %s", e)
        exit(1)

    md = Markdown(results)
    console.print(md)


def entrypoint():
    app.run(main)


if __name__ == "__main__":
    entrypoint()
