import os
from . import apikey
os.environ['OPENAI_API_KEY'] = apikey.apikey
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="./rreports/numeric.json"


import openai
import re
import requests

GPT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"

from openai import OpenAI
client = OpenAI()

import nltk
nltk.download('punkt')  # Download the Punkt tokenizer models
from nltk.tokenize import sent_tokenize
import re



##################################################

def split_into_paragraphs(sentences):
  
  paragraphs = []
  current_paragraph = ""

  for sentence in sentences:
    
    current_paragraph += sentence + " "    
    if sentence[-2] == '*':
      sentence = sentence.replace('**', '')

      paragraphs.append(current_paragraph.strip())
      current_paragraph = ""

    # Add the last paragraph if any text remains
  if current_paragraph:
    paragraphs.append(current_paragraph.strip())

  return paragraphs

#################################################

import openai

def llm_response(query, model="gpt-3.5-turbo", temperature=0.5):
    
    """
    Simplify English text using OpenAI's ChatGPT.

    Parameters:
    - query (str): Text to be simplified.
    - model (str): OpenAI GPT model to use (default: "gpt-3.5-turbo").
    - temperature (float): Controls randomness in the response (default: 0.5).

    Returns:
    - str: Simplified text.
    """
    system_message = "You are an expert at simplifying English text."
    user_message = f"Simplify the following text taken from a research report on a listed company. Retain text within parentheses unchanged: {query}"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout= 10
        )
        response = response.choices[0].message.content
        return response

    except Exception as e:
        print (f'exception caught: {e}')
        return query


  #################################################

from google.cloud import translate_v3 as translate


def translate_text_with_glossary(
    source,
    target,
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    project_id: str = "numeric-chassis-395210",
  ) -> translate.TranslateTextResponse:
    """

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project that owns the glossary.
       

    Returns:
        The translated text."""
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    
    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        request={
            "contents": [text],
            "target_language_code": target,
            "source_language_code": source,
            "parent": parent,
        
        }
    )

    return response.translations[0].translated_text # return response.glossary_translations

    #############################################

def clean_text(item):
  item = item.replace ('topline', 'revenue')
  item = item.replace ('top line', 'revenue')
  item = item.replace ('bottomline', 'net profit')
  item = item.replace ('bottom line', 'net profit')
  item = item.replace ('eps', 'earnings per share')
  item = item.replace ('flat', 'unchanged')
  item = item.replace ('capacity utilisation', 'കപ്പാസിറ്റി വിനിയോഗം')
  item = item.replace ('outlook', 'expectation')
  item = item.replace ('core', 'basic')
  item = item.replace ('yoy', ' over the previous year ')
  item = item.replace ('order execution', 'ഓർഡർ എക്സിക്യൂഷൻ')
  item = item.replace ('execution', 'എക്സിക്യൂഷൻ')
  item = item.replace ('executing', 'building')
  item = item.replace ('margins', 'margin')
  item = item.replace ('modest', 'small')
  item = item.replace (' per ', ' for a ')
  item = item.replace ('formulations', 'ഫോറമൂലേഷൻസ് ')
  item = item.replace ('rs.', 'rs ')
  item = item.replace ('valuation', 'വാല്യുയേഷൻ')
  item = item.replace ('mix', 'മിക്സ്')
  item = item.replace ('order pipeline', 'ഓർഡർ പൈപ്പ് ലൈൻ')
  item = item.replace ('supported by', 'on account of')
  item = item.replace ('muted', 'slow')
  item = item.replace ('monitorable', 'aspects to monitor')
  item = item.replace ('leisure', 'entertainment')
  item = item.replace ('fleet count', 'number of planes')
  item = item.replace ('risk', 'റിസ്ക്')
  item = item.replace ('realization', 'റിയലയിസെഷന്')
  item = item.replace (' cmp', 'Current Market Price')
  item = item.replace (' buy ', 'ബൈ')
  item = item.replace (' sell', 'സെല്ല്')
  item = item.replace (' accumulate', 'ആക്കുമുലേറ്റ്')
  item = item.replace (' hold', 'ഹോൾഡ്')
  item = item.replace ('volumes', 'turn over')
  item = item.replace ('volume', 'turn over')
  item = item.replace ('cash flows', 'inflow of cash')
  item = item.replace ('largely', 'to a great extent')
  item = item.replace ('accounting for', 'which account for')
  item = item.replace ('cagr', 'yearly growth rate')
  item = item.replace ('fleet', 'collection')
  item = item.replace ('- ', '')
  item = item.replace ('festive', 'festive season')
  item = item.replace ('defying', 'against')
  item = item.replace ('capacity additions', 'expansion')
  item = item.replace ('capacity addition', 'expansion')
  item = item.replace ('ramp up', 'improvement in activity')
  item = item.replace ('support', 'help')
  item = item.replace ('strategic', '')

  return item


  ###########################################


def translate_text (text, target):
  
  text_1 = repr(clean_text(text.lower()))
  text_2 = text_1.replace('•', '$$')
  text_3 = re.sub(r'\\n\\n', '$$', text_2)
  text_3 = re.sub(r'\\r?\\n', '$$', text_3)
  
  text_4 = text_3.replace ('.$$', '**. ')
  text_5 = text_4.replace ('$$$$', '**. ')
  text_5 = text_5.replace ('$$', ' ')

  sentences = sent_tokenize(text_5)
  paragraphs = split_into_paragraphs(sentences)
  
  translation = ''

  for para in paragraphs:
    if len(para)>100:
        simple = llm_response(para)
        
    else:
        simple = para.replace('**', '')
    
    simple = clean_text(simple)
    if simple:
      tr_text = translate_text_with_glossary('en', target, simple)
    
    if len(tr_text)<0:
      tr_text = f"<b>{tr_text}</b>"

    translation += tr_text
    translation +="<br><br>"
  return translation
