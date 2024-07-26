# Basic

This script uses a combination of OpenAI and Google Translate to translate html and markdown files into a specified language. It is developed for a specific website, but could be tailored to work for others.

Open AI excels with specific data structure transformation, while Google Translate is superior in translating natural sounding language.

It requires a paid OpenAI key and Google Cloud account.

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
GOOGLE_CLOUD_PROJECT_ID="your-project-id"

```

### Pages

You can use this script to translate a single file or a directory of files. 

```
python translate-pages.py <language code> <input file or folder name>
```

For example, to translate a directory named "pages" into Spanish, you would run:

```
python translate-pages.py es pages
```

To translate a single file named "home.html" into Arabic, you would run:
```
python translate-pages.py ar home.html
```


### Global JSON content

To translate the languages_base file for global content into Spanish, you would run:
```
python translate-base.py es languages_base.json
```

To translate the navigation file into Arabic, you would run:
```
python translate-base.py ar navigation.json
```

## Notes
The Open AI model has an output token limit. Files larger than this will fail and need to be translated manually via the OpenAI playground.

The script logs its activity to a file named "app.log" for help debugging.

### License
[GNU AFFERO GENERAL PUBLIC LICENSE](license.txt)