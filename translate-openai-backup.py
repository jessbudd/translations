import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#usage
# python translate-openai.py <language ISO code> <input file> 

if len(sys.argv) < 3:
    raise Exception('You must provide the language ISO code and input file as arguments')

language = sys.argv[1]
input_file = sys.argv[2]

output_file = f"{language}/{input_file}"

client = OpenAI(
  organization=os.getenv('OPEN_API_ORGANISATION_ID'),
  project= os.getenv('OPEN_API_PROJECT_ID'),
  api_key=os.getenv('OPEN_API_KEY')
)

def concatenate_prompt_with_file_content(language, file_path):
    prompt = f"The following document is a page from a website written in the english language. It may be written in html or in markdown. Your job is to translate the page from english into the language with an ISO language code of {language}, while keeping all markup, html tags and attributes the same. Open Web Advocacy, hashtags and social media platform names should not be translated. The text between the — characters is the front matter. The title and metaDesc properties should be translated. The permalink should remain in English, but with the language code in front. For example ‘/‘ would become ‘/es/‘."

    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return prompt + file_content

concatenated_content = concatenate_prompt_with_file_content(language, input_file)


class ObjectView(object):
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = ObjectView(v)
            elif isinstance(v, list):
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        v[i] = ObjectView(v[i])
        self.__dict__ = d

dummy = {
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "logprobs": 'null',
      "text": "\n\n\"Let Your Sweet Tooth Run Wild at Our Creamy Ice Cream Shack"
    }
  ],
  "created": 1683130927,
  "id": "cmpl-7C9Wxi9Du4j1lQjdjhxBlO22M61LD",
  "model": "gpt-3.5-turbo-instruct",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 16,
    "prompt_tokens": 10,
    "total_tokens": 26
  }
}
dummyResponse = ObjectView(dummy)

# Function to translate using OpenAI's API
def translate_text(text):
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
    prompt=text,
    max_tokens=1500,
    stop=None,
    temperature=0.1,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)
    return response

    return dummyResponse


# Translate the text
response = translate_text(concatenated_content)
translated_text = response.choices[0].text.strip().replace('\n', '')

print('########### response', response)
print('########### translated_text', translated_text)


def write_translated_text(translated_text, file_path):
    # Get the directory name from the file path
    directory = os.path.dirname(file_path)

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the translated text to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)

write_translated_text(translated_text, output_file)

# Calculate cost of translation in USD
cost_per_1k_tokens = 0.00150
total_tokens_used = response.usage.total_tokens
total_cost = total_tokens_used * cost_per_1k_tokens

# Print confirmation message
print(f"Translated file written to: {output_file}")
print(f"Total tokens used: {response.usage.total_tokens}")
print(f"Cost of translation in USD: {round(total_cost, 2)}")
