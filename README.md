# unitoken

Working with large volumes of webtext can be a bit arduous, as the web contains many different languages. This package provides an automated way of tokenizing webtext in different languages by first detecting the language of a string, and then using an appropriate language specific tokenizer to tokenize it.

It exposes two functions:
* `tokenize(str)`: tokenizes your text into words.
* `sent_tokenize(str)`: tokenizes your text into sentences, which are again split into words.

Both functions also take a `score_threshold` parameter. If the confidence of the language classifier is below this score, the functions throws a ValueError. This can be used to weed out noisy texts.

## Example

```python
from unitoken import tokenize

my_sentences = ["日本、朝鮮半島、中国東部まで広く分布し、その姿や鳴き声はよく知られている。",
"ประเทศโครเอเชียปรับมาใช้สกุลเงินยูโรและเข้าร่วมเขตเชงเกน", "The dog walked home and had a nice cookie."]

tokenized = []
for sentence in my_sentences:
    tokenized.append(tokenize(sentence))
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

0.1.0
