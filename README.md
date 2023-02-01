# unitoken

Working with large volumes of webtext can be a bit arduous, as the web contains many different languages. This package provides an automated way of tokenizing webtext in different languages by first detecting the language of a string, and then using an appropriate language specific tokenizer to tokenize it.

It exposes two functions:
* `tokenize(str)`: tokenizes your text into words.
* `sent_tokenize(str)`: tokenizes your text into sentences, which are again split into words.

The functions also take a dictionary mapping from languages to spacy models. This is handy if you'd like to use models you defined yourself.

The return of the models is a tuple: the first item is the tokens in the text, while the second item is a LanguageResult, indicating the language, the confidence, and whether the language was valid in the current context. If the language is invalid, i.e., `valid == False`, then the return list of tokens will be empty.

## Example

```python
from unitoken import tokenize

my_sentences = ["日本、朝鮮半島、中国東部まで広く分布し、その姿や鳴き声はよく知られている。",
"ประเทศโครเอเชียปรับมาใช้สกุลเงินยูโรและเข้าร่วมเขตเชงเกน", "The dog walked home and had a nice cookie."]

tokenized = []
for sentence in my_sentences:
    tokenized.append(tokenize(sentence))
```

Using a pre-defined model:

```python
import spacy
from unitoken import tokenize

# Assumes en_core_web_sm is installed.
predefined_models = {"en": spacy.load("en_core_web_sm")}

my_sentences = ["日本、朝鮮半島、中国東部まで広く分布し、その姿や鳴き声はよく知られている。",
"ประเทศโครเอเชียปรับมาใช้สกุลเงินยูโรและเข้าร่วมเขตเชงเกน", "The dog walked home and had a nice cookie."]

tokenized = []
for sentence in my_sentences:
    tokenized.append(tokenize(sentence, models=predefined_models))
```

## Installation

It can be installed by cloning through `setup.py`:

```
python3 setup.py install
```

 or by using `git`:

```
pip install git+https://github.com/stephantul/unitoken.git
```

## Credits

This package builds on top of [spacy](spacy.io) and [fasttext](https://fasttext.cc/docs/en/language-identification.html). I didn't really do a lot work.

## Improvements

* The current implementation assumes that a text consists of a single language. This is obviously false. We could try a window approach to find windows in which languages differ, but this requires some experimentation.

## Author

Stéphan Tulkens

## License

MIT

## Version

0.2.0
