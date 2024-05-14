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
        'advances': 'loans',
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
        ' hold ': ' hold (that is, a rating of "Hold")',
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
        'bps':'basis points ',
        'P/E': 'P/E multiple',
        'EV/EBITDA': 'EV/EBITDA multiple',
        '\n':' ',
        '\r':' ',
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


def llm_response(query, summary_text, model=GPT_MODEL, temperature=0):
    
    system_message = "You are an expert at simplifying complex text for lay persons, by eliminating jargon. "
    user_message = f'''Please simplify the following text excerpted 
    from a larger piece titled {summary_text},
    sentence by sentence: {query}'''

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

def summary(query, model=GPT_MODEL, temperature=0):
    
    system_message = "You are an expert headline editor."
    user_message = f'''Provide a headline of 30 words
    to the following text: {query}'''

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
    summary_text = summary(text)
    abbns = extract_uppercase_words(text)
    paragraphs = split_to_para(text)
    para_wise_text=''
    for i, item in enumerate(paragraphs):
        if len(item)>100 or '.' in item[-4:]:
            item = replace_upper(item.lower(), abbns)
            item = clean_text(item)
            item = llm_response(item, summary_text)
        else:
            item = replace_upper(item.lower(), abbns)
            item = clean_text(item)
            item = '<b>'+item+'</b>'
 
            
        item = translate.translate_text_with_glossary(item, target)
        if i+1 == len(paragraphs):
            para_wise_text += item
            yield para_wise_text
        else:    
            para_wise_text += item + '<br><br>'
            yield para_wise_text
    # return para_wise_text
