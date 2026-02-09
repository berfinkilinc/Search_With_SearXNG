import random
import time
import os
import gradio as gr
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from langchain_rag import *



load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")


force_dark_mode = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

client = OpenAI(api_key=openai_api_key)

system_message = "You are a helpful assistant that responds in markdown"

def stream_gpt(prompt):

   answer = creating_answer(model, tools, system_prompt=prompt)
   
   '''
   messages = [
      {"role": "system", "content": system_message},
      {"role": "user", "content": prompt}
   ]
   stream = client.chat.completions.create(
      model = "gpt-4o-mini",
      messages=messages,
      stream=True
   )
   result = ""
   for chunk in stream:
      result += chunk.choices[0].delta.content or ""
      yield result

   '''
   yield answer

view = gr.Interface(
   fn=stream_gpt, 
   inputs=[gr.Textbox(label="Your message:", lines=6)], 
   outputs= [gr.Textbox(label="Response:", lines=8)],
   flagging_mode = "never",
   js=force_dark_mode
)

view.launch(inbrowser=True, share=True)






