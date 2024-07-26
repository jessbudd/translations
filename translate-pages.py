import os
import sys
import logging
import time
from openai import OpenAI
from dotenv import load_dotenv

# Usage
# translates a single file or a directory of files
# and outputs them to a new language folder
#
# Command
# python translate-pages.py <language code> <input file or folder name>
# example: python translate-pages.py es pages
# example: python translate-pages.py ar home.html
# 
# this gpt model has a limit of 4,096 output tokens
# files larger than this will fail and need to be translated 
# manually via the Open AI playground

MODEL = 'gpt-4o-mini'

# Set up logging
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
    prompt = f"The following document is a page from a website written in the english language. It may be written in html or in markdown. Please translate the page from english into the language with an ISO language code of {language}, while keeping all markup, html tags and attributes the same. Open Web Advocacy, OWA, hashtags and platform names should not be translated. The permalinks should remain in English, but with the language code in front. For example ‘/‘ would become ‘/es/‘. The title and metaDesc properties in the front matter should be translated Please be mindful of using correct accents and consistent masculine gender if it applies to the given language."

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    logging.info('CONCATENATED_PROMPT ' + prompt + file_content)
    return prompt + file_content

def translate_text(text):
    start_time = time.time()
    response = client.chat.completions.create(model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates English files into other languages for use on a static website."},
            {"role": "user", "content": text}
        ],
        max_tokens=4000,
        stop=None,
        temperature=0.1,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"The OpenAI translation request took {round(elapsed_time, 2)} seconds.") 
    logging.info('RESPONSE ' + str(response))
    logging.info('RESPONSE MESSAGE ' + response.choices[0].message.content.strip())
    return response

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
    translated_text = response.choices[0].message.content.strip()

    write_output_to_file(translated_text, output_path)
    getCostOfTranslation(response)
    print(f"Translated file {input_path} and wrote output to {output_path}")


def process_files_in_directory(input_dir, output_dir):
    filenames = os.listdir(input_dir)
    successful_translations_count = 0
    error_count = 0
    error_file_names = [] 
    total_cost = 0

    for filename in filenames:
        if not filename.startswith('.'):  # Skip hidden files or files starting with .
            try:
                input_path = os.path.join(input_dir, filename)

                if os.path.isfile(input_path):
                    output_path = os.path.join(output_dir, filename)

                    concatenated_content = concatenate_prompt_with_file_content(language, input_path)
                    response = translate_text(concatenated_content)
                    translated_text = response.choices[0].message.content.strip()

                    write_output_to_file(translated_text, output_path)                
                    cost = getCostOfTranslation(response)
                    total_cost += cost
                    successful_translations_count += 1
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                error_file_names.append(filename)
                error_count += 1

    print(f"Total cost of translations in USD: ${round(total_cost, 4)}")
    print(f"Total number of files written: {successful_translations_count}")
    print(f"Total number of errors: {error_count}")
    print(f"Files with errors: {error_file_names}")

def process_input(input_path, output_dir):
    if os.path.isfile(input_path):
        process_file(input_path, output_dir)
    elif os.path.isdir(input_path):
        process_files_in_directory(input_path, output_dir)
    else:
        raise Exception(f'Invalid path: {input_path}')
    
process_input(input_path, language)