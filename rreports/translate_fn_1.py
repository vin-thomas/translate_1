import os
from . import apikey
os.environ['OPENAI_API_KEY'] = apikey.apikey
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ="./rreports/numeric.json"


import openai
import re

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

  ################################################

def llm_response(query):

  message = f'''Simplify the following text taken from a research report on 
  a listed company: {query} '''

  messages = [
      {"role": "system", "content": "You are an expert at simplifying english text."},
      {"role": "user", "content": message},
    ]

  response = client.chat.completions.create(
      model= GPT_MODEL,
      messages=messages,
      temperature=0
      )
  response = response.choices[0].message.content
  return response

  #################################################

from google.cloud import translate_v3 as translate


def translate_text_with_glossary(
    source,
    target,
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    project_id: str = "numeric-chassis-395210",
    glossary_id: str = "mal-eng-glossary",
  ) -> translate.TranslateTextResponse:
    """Translates a given text using a glossary.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project that owns the glossary.
        glossary_id: The ID of the glossary to use.

    Returns:
        The translated text."""
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    glossary = client.glossary_path(
        project=project_id, location="us-central1", glossary=glossary_id
        )


    glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)


    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        request={
            "contents": [text],
            "target_language_code": target,
            "source_language_code": source,
            "parent": parent,
            "glossary_config": glossary_config,
        }
    )

    return response.glossary_translations[0].translated_text # return response.glossary_translations

    #############################################

def clean_text(item):
  item = item.replace ('topline', 'revenue')
  item = item.replace ('top line', 'revenue')
  item = item.replace ('bottomline', 'net profit')
  item = item.replace ('bottom line', 'net profit')
  item = item.replace ('earning per share', 'EPS')
  item = item.replace ('earnings per share', 'EPS')
  item = item.replace ('earnings per share', 'EPS')
  item = item.replace ('Earning per share', 'EPS')
  item = item.replace ('flat', 'unchanged')
  item = item.replace ('capacity utilisation', 'കപ്പാസിറ്റി വിനിയോഗം')
  item = item.replace ('outlook', 'expectation')
  item = item.replace ('core', 'basic')
  item = item.replace ('YoY', ' over the previous year ')
  item = item.replace ('Order execution', 'ഓർഡർ എക്സിക്യൂഷൻ')
  item = item.replace ('execution', 'implementation')
  item = item.replace ('margins', 'margin')
  item = item.replace ('modest', 'small')
  item = item.replace (' per ', ' for a ')
  item = item.replace ('formulations', 'ഫോറമൂലേഷൻസ് ')
  item = item.replace ('Rs.', 'Rs')
  item = item.replace ('Valuations', 'വല്യൂയേഷൻ  ')
  item = item.replace ('valuation', 'വാല്യുയേഷൻ')
  item = item.replace ('mix', 'മിക്സ്')
  item = item.replace ('Order pipeline', 'ഓർഡർ പൈപ്പ് ലൈൻ')
  item = item.replace ('order pipeline', 'ഓർഡർ പൈപ്പ് ലൈൻ')
  item = item.replace ('supported by', 'on account of')
  item = item.replace ('muted', 'slow')
  item = item.replace ('Muted', 'slow')
  item = item.replace ('key monitorable', 'important aspects to watch')
  item = item.replace ('leisure', 'entertainment')
  item = item.replace ('fleet count', 'number of planes')
  item = item.replace ('risk', 'റിസ്ക്')
  item = item.replace ('realization', 'റിയലയിസെഷന്')
  item = item.replace ('CMP', 'Current Market Price')
  item = item.replace ('Buy ', 'ബൈ')
  item = item.replace ('Sell', 'സെല്ല്')
  item = item.replace ('Accumulate', 'ആക്കുമുലേറ്റ്')
  item = item.replace ('Hold', 'ഹോൾഡ്')
  item = item.replace ('volume', 'turn over')
  item = item.replace ('cash flows', 'inflow of cash')
  item = item.replace ('largely', 'to a great extent')
  item = item.replace ('accounting for', 'which account for')
  item = item.replace ('CAGR', 'yearly growth rate')
  item = item.replace ('fleet', 'collection')
  return item


  ###########################################


def translate_text (text):
  text_1 = repr(text)
  text_2 = text_1.replace('•', ' ')
  text_3 = re.sub(r'\\n\\n', '$$', text_2)
  text_3 = re.sub(r'\\r?\\n', '$$', text_3)
  
  text_4 = text_3.replace ('.$$', '**. ')
  text_5 = text_4.replace ('$$$$', '**. ')
  text_5 = text_5.replace ('$$', ' ')

  sentences = sent_tokenize(text_5)
  paragraphs = split_into_paragraphs(sentences)
  
  translation = ''
  simple_t = ''

  for para in paragraphs:
    clean = clean_text(para)
    if not '(' in clean:
      simple = llm_response (clean)
    else:
      simple = clean
    simple = clean_text(simple)
    tr_text = translate_text_with_glossary('en', 'ml', simple)
    translation += tr_text
    translation +="\n\n"
    simple_t +=simple
    simple_t += "\n\n"

  return simple_t + '\n\n' + translation
