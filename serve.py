#!/usr/bin/env python

import os 

from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../IHAI-lessons/000_lesson_data/044_llm/.env'))

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser

# 5. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 6. Adding chain route
if not any(route.path == "/chain" for route in app.routes):
    add_routes(app,
               chain, 
               path="/chain")

@app.get("/")
async def root():
    return {"message": "Welcome to the Translation API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
