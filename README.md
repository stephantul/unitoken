# unitoken

Working with large volumes of webtext can be a bit arduous, as the web contains many different languages. This package provides an automated way of tokenizing webtext in different languages by first detecting the language of a string, and then using an appropriate language specific tokenizer to tokenize it.

It exposes two functions:
* `tokenize(str)`: tokenizes your text into words.
* `sent_tokenize(str)`: tokenizes your text into sentences, which are again split into words.


