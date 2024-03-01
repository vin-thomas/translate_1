import re
from . import translate

def extract_uppercase_words(text):
    uppercase_words = re.findall(r'\b[A-Z][A-Z0-9]+\b', text)
    return set(uppercase_words)

def replace_upper(text, upper):
    for item in upper:
        text = text.replace(item.lower(), item)
    return text
    

def split_to_para(text):
    # text = re.sub(r'(?<!\.)\n(?=[A-Z])', '**', text)
    text = text.replace ('.\r\n\r\n', '.** ')
    text = text.replace('\r\n\r\n', '** ')
    text = text.replace ('\n\r', '**')
    text = text.replace('•', '** ')
    
    paragraphs = text.split('**')
       
    return(paragraphs)


def clean_text(item):
    replacements = {
        'on FY': 'FY',
        'dumping': '"dumping"',
        'topline': 'revenue',
        'top line': 'revenue',
        'bottomline': 'net profit',
        'bottom line': 'net profit',
        ' eps ': ' earnings per share ',
        ' flat ': ' unchanged ',
        'outlook': 'expectation',
        ' core ': ' basic ',
        'yoy ': ' compared to the previous year ',
        ' year over year ': ' compared to the previous year ',
        'order execution': '"order execution"',
        'execution': '"execution"',
        'executing': 'building',
        'margins': 'margin',
        'modest': 'small',
        ' per ': ' for a ',
        'formulations': 'formulations (that is, pharmaceutical preparation)',
        ' rs. ': ' rs ',
        ' Rs. ': ' Rs ',
        'valuations': '"valuations"',
        'valuation': '"valuation"',
        ' mix ': ' mix (that is, a combination of various items) ',
        'order pipeline': '"order pipeline" ',
        'supported by': 'on account of',
        'muted': 'slow',
        'monitorable': 'aspects to monitor',
        'leisure': 'entertainment',
        'fleet count': 'number of planes',
        ' risk ': ' risk (that is, business risk) ',
        'realization': 'realization (that is, the amount collected)',
        'realisation': 'realisation (that is, the amount collected)',
        ' cmp': 'Current Market Price',
        ' buy ': ' buy (that is, a rating of "Buy")',
        ' sell ': ' sell (that is, a rating of "Sell")',
        ' accumulate ': ' accumulate (that is, a rating of "Accumulate") ',
        ' hold': ' hold (that is, a rating of "Hold")',
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
        'trim': 'reduce',
        'volatility': 'fluctuation',
        'bps':'basis points (that is one hundredth of a percentage) ',
        'P/E': 'P/E multiple',
        'EV/EBITDA': 'EV/EBITDA multiple',
    }

    for original, replacement in replacements.items():
        item = item.replace(original, replacement)

    return item

import os
import openai
openai.api_key = os.environ['OPENAI_API_KEY']
GPT_MODEL = "gpt-3.5-turbo"
# GPT_MODEL = "gpt-4"
from openai import OpenAI
client = OpenAI()


def llm_response(query, model=GPT_MODEL, temperature=0):
    
    system_message = "You are an expert at simplifying English text."
    user_message = f'''The following text taken from a research report on a listed company. 
    Simplify the text to improve clarity and readability.
    Use short sentences.: {query}'''

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



def preprocess(text, target):
    abbns = extract_uppercase_words(text)
    paragraphs = split_to_para(text)
    para_wise_text=''
    for item in paragraphs:
        if len(item)>100:
            item = replace_upper(item.lower(), abbns)
            item = clean_text(item)
            item = llm_response(item)
            item = clean_text(item)
        else:
            item = replace_upper(item.lower(), abbns)
            item = '<b>'+clean_text(item)+'</b>'
        
        print (item)
            
        item = translate.translate_text_with_glossary(item, target)
        para_wise_text +=item + '<br><br>'
    return para_wise_text
