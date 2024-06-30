# OpenAI Translation Script

This script uses OpenAI's GPT-3.5-turbo model to translate html and markdown files or directories of html and markdown files into a specified language. It is developed for a specific website, but could be tailored to work for others.

It requires an OpenAI key and a paid account.

## Installation 

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/jessbudd/translations.git
cd <your-repo-directory>
pip install -r requirements.txt
```

## Usage

Create a `.env` file based on `.env.sample` and add your own OpenAI credentials.

```
OPEN_API_KEY="your-key-id"
OPEN_API_ORGANISATION_ID="your-org-id"
OPEN_API_PROJECT_ID="your-proj-id"

```
You can use this script to translate a single file or a directory of files. 

```
python translate-pages.py <language code> <input file or folder name>
```

For example, to translate a directory named "pages" into Spanish, you would run:

```
python translate-openai.py es pages
```

To translate a single file named "home.html" into Arabic, you would run:
```
python translate-openai.py ar home.html
```

## Notes
The GPT-3.5-turbo model at the time of writing has a limit of 4,096 output tokens. Files larger than this will fail and need to be translated manually via the OpenAI playground.

The script logs its activity to a file named "app.log" for help debugging.

### License
[GNU AFFERO GENERAL PUBLIC LICENSE](license.txt)