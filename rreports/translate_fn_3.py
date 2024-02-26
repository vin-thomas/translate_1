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
    Simplify the text to improve clarity and readability: {query}'''

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
        print (f'exception caught in the llm function: {e}')
        return query


  #################################################

from google.cloud import translate_v3 as translate
client_tr = translate.TranslationServiceClient()

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
    response = client_tr.translate_text(
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
    replacements = {
        'topline': 'revenue',
        'top line': 'revenue',
        'bottomline': 'net profit',
        'bottom line': 'net profit',
        'eps': 'earnings per share',
        'flat': 'unchanged',
        'outlook': 'expectation',
        'core': 'basic',
        'yoy': ' over the previous year ',
        'order execution': 'ഓർഡർ എക്സിക്യൂഷൻ',
        'execution': 'എക്സിക്യൂഷൻ',
        'executing': 'building',
        'margins': 'margin',
        'modest': 'small',
        ' per ': ' for a ',
        'formulations': 'ഫോറമൂലേഷൻസ് ',
        'rs.': 'rs ',
        'valuations': 'value determination',
        'valuation': 'value determination',
        'mix': 'മിക്സ്',
        'order pipeline': 'ഓർഡർ പൈപ്പ് ലൈൻ',
        'supported by': 'on account of',
        'muted': 'slow',
        'monitorable': 'aspects to monitor',
        'leisure': 'entertainment',
        'fleet count': 'number of planes',
        'risk': 'റിസ്ക്',
        'realization': 'റിയലയിസെഷന്',
        ' cmp': 'Current Market Price',
        ' buy ': 'ബൈ',
        ' sell': 'സെല്ല്',
        ' accumulate': 'ആക്കുമുലേറ്റ്',
        ' hold': 'ഹോൾഡ്',
        'volumes': 'turnover',
        'volume': 'turnover',
        'cash flows': 'inflow of cash',
        'largely': 'to a great extent',
        'accounting for': 'which account for',
        'cagr': 'yearly growth rate',
        'fleet': 'collection',
        '- ': '',
        'festive': 'festive season',
        'defying': 'against',
        'capacity additions': 'expansion',
        'capacity addition': 'expansion',
        'ramp up': 'improvement in activity',
        'support': 'help',
        'strategic': '',
        'trims': 'reduces',
        'trim': 'reduce'
    }

    for original, replacement in replacements.items():
        item = item.replace(original, replacement)

    return item


  ###########################################


def translate_text (text, target):
  import string
  text = clean_text(text)
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
