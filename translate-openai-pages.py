# this file uses legacy chat completions api
# it is limited to 4,096 tokens which means longer files
# fail and throw an error, but it is cheaper to run

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Usage
# python translate-openai.py <language code> <input file or folder name>
# example: python translate-openai.py es pages
# example: python translate-openai.py ar home.html

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
    prompt = f"The following document is a page from a website written in the english language. It may be written in html or in markdown. Your job is to translate the page from english into the language with an ISO language code of {language}, while keeping all markup, html tags and attributes the same. Open Web Advocacy, hashtags and social media platform names should not be translated. The title and metaDesc properties in the front matter should be translated. The permalink should remain in English, but with the language code in front. For example ‘/‘ would become ‘/es/‘."

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return prompt + file_content

# This code is for testing without making actual API calls
# comment in and out as needed
# class ObjectView(object):
#     def __init__(self, d):
#         for k, v in d.items():
#             if isinstance(v, dict):
#                 d[k] = ObjectView(v)
#             elif isinstance(v, list):
#                 for i in range(len(v)):
#                     if isinstance(v[i], dict):
#                         v[i] = ObjectView(v[i])
#         self.__dict__ = d

# dummy = {
#   "choices": [
#     {
#       "finish_reason": "length",
#       "index": 0,
#       "logprobs": 'null',
#       "text": "\n\n\"Let Your Sweet Tooth Run Wild at Our Creamy Ice Cream Shack"
#     }
#   ],
#   "created": 1683130927,
#   "id": "cmpl-7C9Wxi9Du4j1lQjdjhxBlO22M61LD",
#   "model": "gpt-3.5-turbo-instruct",
#   "object": "text_completion",
#   "usage": {
#     "completion_tokens": 16,
#     "prompt_tokens": 10,
#     "total_tokens": 2600
#   }
# }
# dummyResponse = ObjectView(dummy)

def translate_text(text):
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
    prompt=text,
    max_tokens=2500,
    stop=None,
    temperature=0.1,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)
    return response

    # return dummyResponse

def write_output_to_file(translated_text, file_path):
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)
    print(f"Translated file output to {file_path}")


def getCostOfTranslation(response):
    cost_per_1k_tokens = 0.00150
    total_tokens_used = response.usage.total_tokens
    total_cost = (total_tokens_used / 1000) * cost_per_1k_tokens
    
    print(f"{response.usage.total_tokens} total tokens used at a cost of ${round(total_cost, 4)} USD")
    return total_cost

def process_file(input_path, output_dir):
    output_path = os.path.join(output_dir, os.path.basename(input_path))

    concatenated_content = concatenate_prompt_with_file_content(language, input_path)
    response = translate_text(concatenated_content)
    translated_text = response.choices[0].text.strip()

    print(f"#### concatenated_content: {concatenated_content}")

    print(f"##### response: {response}")
    print(f"#### Translated text: {translated_text}")

    write_output_to_file(translated_text, output_path)
    getCostOfTranslation(response)
    print(f"Translated file {input_path} and wrote output to {output_path}")


def process_files_in_directory(input_dir, output_dir):
    filenames = os.listdir(input_dir)
    successful_translations = 0
    error_count = 0
    total_cost = 0

    for filename in filenames:
        try:
            input_path = os.path.join(input_dir, filename)

            if os.path.isfile(input_path):
                output_path = os.path.join(output_dir, filename)

                concatenated_content = concatenate_prompt_with_file_content(language, input_path)
                response = translate_text(concatenated_content)
                translated_text = response.choices[0].text.strip()

                write_output_to_file(translated_text, output_path)                
                cost = getCostOfTranslation(response)
                total_cost += cost
                successful_translations += 1
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            error_count += 1

    print(f"Total number of files written: {successful_translations}")
    print(f"Total number of errors: {error_count}")
    print(f"Total cost of tokens in USD: ${round(total_cost, 4)}")

def process_input(input_path, output_dir):
    if os.path.isfile(input_path):
        process_file(input_path, output_dir)
    elif os.path.isdir(input_path):
        process_files_in_directory(input_path, output_dir)
    else:
        raise Exception(f'Invalid path: {input_path}')
    
process_input(input_path, language)