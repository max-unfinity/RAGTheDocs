---
title: RAGTheDocs
emoji: 👀
colorFrom: gray
colorTo: yellow
sdk: gradio
sdk_version: 3.50.2
app_file: app.py
pinned: false
license: mit
---

# RAGtheDocs

## Introduction 📚

RAGTheDocs is an open-source library that allows you to deploy retrieval augmented generation (RAG) on any readthedocs documentation with a one-click deploy on huggingface spaces!

## Usage

1) Go to the [example space](https://huggingface.co/spaces/jerpint/RAGTheDocs)
2) Duplicate the space:

![image](https://github.com/jerpint/buster/assets/18450628/0c89038c-c3af-4c1f-9d3b-9b4d83db4910)

3) Set your environment variables:
* `OPENAI_API_KEY`: Needed for the app to work, e.g. `sk-...`
* `READTHEDOCS_URL`: The url of the website you are interested in scraping
* `READTHEDOCS_VERSION`: This is important only if there exist multiple versions of the docs (e.g. "en/v0.2.7" or "en/latest"). If left empty, it will scrape all available versions.

**WARNING** This library is experimental and automatically calls OpenAI APIs for you. Use at your own risk! ⚠️


## Features 🚀

- **Web Scraping and embeddings:** RAGtheDocs automatically scrapes and embeds documentation from any website generated by ReadTheDocs/Sphinx using OpenAI embeddings

- **RAG Interface:** It comes built-in with a gradio UI for users to interact with [Buster 🤖](https://github.com/jerpint/buste) our RAG agent.

- **Customization Options:** Tailor RAGtheDocs to your needs with customizable settings and options.
