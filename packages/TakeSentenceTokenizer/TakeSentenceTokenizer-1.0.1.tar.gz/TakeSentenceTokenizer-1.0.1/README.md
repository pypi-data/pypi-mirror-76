# TakeSentenceTokenizer

TakeSentenceTokenizer is a tool for pre processing and tokenizing sentences. 
The package is used to:
	- convert the first word of the sentence to lowercase
	- convert from uppercase to lowercase
	- convert word to lowercase after punctuation
	- replace words for placeholders: laugh, date, time, ddd, measures (10kg, 20m, 5gb, etc), code, phone number, cnpj, cpf, email, money, url, number (ordinal and cardinal)
	- replace abbreviations
	- replace common typos
	- split punctuations
	- remove emoji
	- remove characters that are not letters or punctuation
	- add missing accentuation
	- tokenize the sentence

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TakeSentenceTokenizer

```bash
pip install TakeSentenceTokenizer
```

## Usage

Example 1: full processing not keeping registry of removed punctuation

Code:
```python
from SentenceTokenizer import SentenceTokenizer
sentence = 'P/ saber disso eh c/ vc ou consigo ver pelo site www.dúvidas.com.br/minha-dúvida ??'
tokenizer = SentenceTokenizer()
processed_sentence = tokenizer.process_message(sentence)
print(processed_sentence)
```

Output:
```python
'para saber disso é com você ou consigo ver pelo site URL ? ?'
```


Example 2: full processing keeping registry of removed punctuation
```python
from SentenceTokenizer import SentenceTokenizer
sentence = 'como assim $@???'
tokenizer = SentenceTokenizer(keep_registry_punctuation = True)
processed_sentence = tokenizer.process_message(sentence)
print(processed_sentence)
print(tokenizer.removal_registry_lst)
```

Output:
```python
como assim ? ? ?
[['como assim $@ ? ? ?', {'punctuation': '$', 'position': 11}, {'punctuation': '@', 'position': 12}, {'punctuation': ' ', 'position': 13}]]
```

## Author
Take Data&Analytics Research

## License
[MIT](https://choosealicense.com/licenses/mit/)