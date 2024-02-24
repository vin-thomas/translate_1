import os
import openai
import re
import requests

openai.api_key = os.environ['OPENAI_API_KEY']
GPT_MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"

from openai import OpenAI
client = OpenAI()

import nltk
nltk.download('punkt')  # Download the Punkt tokenizer models
from nltk.tokenize import sent_tokenize
import re

#################################################

import openai

def llm_response(query, model="gpt-3.5-turbo", temperature=0.5):
    
    system_message = "You are an expert at simplifying English text."
    user_message = f'''The following text taken from a research report on a listed company. 
    Simplify the text for clarity and readability: {query}'''

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
client = translate.TranslationServiceClient()

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
  item = item.replace ('valuations', 'value determination')
  item = item.replace ('valuation', 'value determination')
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
  item = item.replace ('volumes', 'turnover')
  item = item.replace ('volume', 'turnover')
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
  item = item.replace ('trims', 'reduces')
  item = item.replace ('trim', 'reduce')

  return item


  ###########################################


def translate_text (text, target):
  import string
  text = clean_text(text.lower())
  text = text.replace ('.\r\n\r\n', '**. ')
  text = text.replace('\r\n\r\n', '**. ')
  text = text.replace ('\n\r', '**.')
  text = text.replace('•', '**.')
  
  paragraphs = text.split('**')
  
  translation = ''

  for para in paragraphs:
    simple = ''
    tr_text = ''

    if len(para)>100:
        simple = llm_response(para.lstrip(string.punctuation).lstrip())

    else:
        simple = para.lstrip(string.punctuation).lstrip()
    
    simple = clean_text(simple)

    if len(simple)>3:
      tr_text = translate_text_with_glossary('en', target, simple)

       
    if tr_text:
      if len(tr_text)<100:
        tr_text = f"<b>{tr_text}</b>"
      translation += tr_text + "<br><br>"

  return translation
