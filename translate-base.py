import os
import sys
import logging
import time
from openai import OpenAI
from dotenv import load_dotenv

# Usage
# overwrites existing json file with translated content
#
# Command
# python translate-base.py <language code> <file_name>
# example: python translate-base.py es languages_base.json
# 
# Notes
# this gpt model has a limit of 4,096 output tokens
# files larger than this will fail and need to be translated 
# manually via the openAI playground

MODEL = 'gpt-4o-mini'
PROMPTS = {
    'languages_base.json': "The following JSON has a set of objects where the key is a language code. One of these keys is 'en' for English. The English object contains a number of properties with English text values. Please add a new {language} object where the properties are exactly the same as the English object, however the values of those properties are translated to the language with an ISO language code of {language}. For example `'asideHeading': 'Recent updates'` becomes `'asideHeading': 'Noticias recientes'` in Spanish. Open Web Advocacy, OWA, hashtags and platform names should not be translated. Please be mindful of using correct accents and consistent masculine gender if it applies to the language. Any languages that already exist should be retained.",
    
    
    'navigation.json': "The following JSON has a set of objects where the key is a language code. One of these keys is 'en' for English. The English object contains two objects; 'primary' and 'secondary'. These objects contain an array of navigation links with a 'text' property and a 'url' property. Please add a new {language} object which is a duplicate of the english object. Translate the 'text' properties only to the language of language code {language}. Open Web Advocacy, OWA, hashtags and platform names should not be translated. Please be mindful of using correct accents and consistent masculine gender if it applies to the language. Any languages that already exist should be retained.",
}

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()

if len(sys.argv) < 3:
    raise Exception('You must provide the language ISO code and input path as arguments')

language = sys.argv[1]
input_path = sys.argv[2]

client = OpenAI(
  organization=os.getenv('OPEN_API_ORGANISATION_ID'),
  project= os.getenv('OPEN_API_PROJECT_ID'),
  api_key=os.getenv('OPEN_API_KEY')
)

def concatenate_prompt_with_file_content(language, file_path):
    prompt = PROMPTS.get(file_path)
    formatted_prompt = prompt.format(language=language)

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        print(formatted_prompt)

    logging.info('CONCATENATED_PROMPT ' + formatted_prompt + file_content)
    return formatted_prompt + file_content

def translate_text(text):
    start_time = time.time()
    response = client.chat.completions.create(model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates English files into other languages for use on a static website."},
            {"role": "user", "content": text}
        ],
        max_tokens=4000,
        stop=None,
        temperature=0.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"The OpenAI translation request took {round(elapsed_time, 2)} seconds.") 
    logging.info('RESPONSE ' + str(response))
    logging.info('RESPONSE MESSAGE ' + response.choices[0].message.content.strip())
    return response

def write_output_to_file(text, file_path):
    with open(file_path, 'w') as file:
        file.write(text)

def getCostOfTranslation(response):
    cost_per_1k_tokens = 0.00150
    total_tokens_used = response.usage.total_tokens
    total_cost = (total_tokens_used / 1000) * cost_per_1k_tokens
    
    print(f"{response.usage.total_tokens} total tokens used at a cost of ${round(total_cost, 4)} USD")
    return total_cost

def process_file(language, input_path):
    output_path = input_path

    concatenated_content = concatenate_prompt_with_file_content(language, input_path)
    response = translate_text(concatenated_content)
    translated_text = response.choices[0].message.content.strip()

    write_output_to_file(translated_text, output_path)
    getCostOfTranslation(response)
    print(f"Translated file {input_path} and wrote output to {output_path}")

process_file(language, input_path)