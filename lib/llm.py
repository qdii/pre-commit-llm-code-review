import os
from enum import Enum

from absl import flags
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama

FLAGS = flags.FLAGS


class LLMType(Enum):
    OLLAMA = "ollama"
    GEMINI = "gemini"
    MISTRAL = "mistral"


flags.DEFINE_enum(
    "llm",
    LLMType.OLLAMA.value,
    [llm.value for llm in LLMType],
    f"The LLM to use: {', '.join(f'\'{llm.value}\'' for llm in LLMType)}",
)


def new() -> ChatGoogleGenerativeAI | ChatOllama | ChatMistralAI:
    if FLAGS.llm == LLMType.GEMINI.value:
        return ChatGoogleGenerativeAI(
            model=FLAGS.model,
            temperature=FLAGS.temperature,
            max_tokens=None,
            timeout=FLAGS.timeout,
            max_retries=FLAGS.retries,
            google_api_key=get_api_key(),
        )
    elif FLAGS.llm == LLMType.OLLAMA.value:
        return ChatOllama(
            base_url=FLAGS.ollama_base_url,
            model=FLAGS.model,
            reasoning=False,
            timeout=FLAGS.timeout,
        )
    elif FLAGS.llm == LLMType.MISTRAL.value:
        return ChatMistralAI(
            model=FLAGS.model,
            timeout=FLAGS.timeout,
            temperature=FLAGS.temperature,
            max_tokens=None,
            mistral_api_key=get_api_key(),
            max_retries=FLAGS.retries,
        )
    raise ValueError(
        f'--llm should be one of {", ".join(f"\'{llm.value}\'" for llm in LLMType)}',
    )


def get_api_key() -> str:
    if FLAGS.llm not in ["gemini", "mistral"]:
        raise RuntimeError("Invalid LLM specified: " + FLAGS.llm)

    if FLAGS.api_key:
        return FLAGS.api_key

    env_name = ""
    if FLAGS.llm == "gemini":
        env_name = "GEMINI_API_KEY"
    elif FLAGS.llm == "mistral":
        env_name = "MISTRAL_API_KEY"

    api_key = os.getenv(env_name)
    if not api_key:
        raise ValueError(
            f"API key not found for {FLAGS.llm}: neither {env_name} nor --api_key is specified",
        )
    return api_key
