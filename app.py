import logging
from typing import Optional, Tuple

import gradio as gr
import pandas as pd
from buster.completers import Completion
from buster.utils import extract_zip

import cfg
from cfg import setup_buster

# Create a handler to control where log messages go (e.g., console, file)
handler = (
    logging.StreamHandler()
)  # Console output, you can change it to a file handler if needed

# Set the handler's level to INFO
handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

# Typehint for chatbot history
ChatHistory = list[list[Optional[str], Optional[str]]]

buster = setup_buster(cfg.buster_cfg)


def add_user_question(
    user_question: str, chat_history: Optional[ChatHistory] = None
) -> ChatHistory:
    """Adds a user's question to the chat history.

    If no history is provided, the first element of the history will be the user conversation.
    """
    if chat_history is None:
        chat_history = []
    chat_history.append([user_question, None])
    return chat_history


def format_sources(matched_documents: pd.DataFrame) -> str:
    if len(matched_documents) == 0:
        return ""

    matched_documents.similarity_to_answer = (
        matched_documents.similarity_to_answer * 100
    )

    # drop duplicate pages (by title), keep highest ranking ones
    matched_documents = matched_documents.sort_values(
        "similarity_to_answer", ascending=False
    ).drop_duplicates("title", keep="first")

    documents_answer_template: str = "📝 Here are the sources I used to answer your question:\n\n{documents}\n\n{footnote}"
    document_template: str = "[🔗 {document.title}]({document.url}), relevance: {document.similarity_to_answer:2.1f} %"

    documents = "\n".join(
        [
            document_template.format(document=document)
            for _, document in matched_documents.iterrows()
        ]
    )
    footnote: str = "I'm a bot 🤖 and not always perfect."

    return documents_answer_template.format(documents=documents, footnote=footnote)


def add_sources(history, completion):
    if completion.answer_relevant:
        formatted_sources = format_sources(completion.matched_documents)
        history.append([None, formatted_sources])

    return history


def chat(chat_history: ChatHistory) -> Tuple[ChatHistory, Completion]:
    """Answer a user's question using retrieval augmented generation."""

    # We assume that the question is the user's last interaction
    user_input = chat_history[-1][0]

    # Do retrieval + augmented generation with buster
    completion = buster.process_input(user_input)

    # Stream tokens one at a time to the user
    chat_history[-1][1] = ""
    for token in completion.answer_generator:
        chat_history[-1][1] += token

        yield chat_history, completion


demo = gr.Blocks()
with demo:
    with gr.Row():
        gr.Markdown("<h3><center>RAGTheDocs</center></h3>")

    chatbot = gr.Chatbot()

    with gr.Row():
        question = gr.Textbox(
            label="What's your question?",
            placeholder="Type your question here...",
            lines=1,
        )
        submit = gr.Button(value="Send", variant="secondary")

    examples = gr.Examples(
        examples=[
            "How can I install the library?",
            "What dependencies are required?",
        ],
        inputs=question,
    )

    gr.Markdown(
        "This app uses [Buster 🤖](github.com/jerpint/buster) and ChatGPT to search the docs for relevant info and answer questions."
    )

    response = gr.State()

    # fmt: off
    gr.on(
        triggers=[submit.click, question.submit],
        fn=add_user_question,
        inputs=[question],
        outputs=[chatbot]
    ).then(
        chat,
        inputs=[chatbot],
        outputs=[chatbot, response]
    ).then(
        add_sources,
        inputs=[chatbot, response],
        outputs=[chatbot]
    )


demo.queue(concurrency_count=16)
demo.launch(share=False)
