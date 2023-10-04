# LoPPy

Logical Parsing with Python

### What Is It?

LoPPy (LOgical Parsing with PYthon) is a Prolog-inspired tool for writing facts that can then be used to build rules. 

The primary goal is to use this tool to build a syntactic parser for grammaticality judgments and part-of-speech tagging to be used in NLP tasks. 

### Files

* `loppy.py` - The core classes for defining facts
* `examples.py` - Some examples of useful methods
* `wh_grammar.py` - The current syntactic parser with a focus on wh-questions (still a long way to go with this!)
* `word_lists/` - Lists of words of various parts of speech for testing

### Running An Example

* From the command line, run `python wh_grammar.py`.
* This should bring up the prompt `Enter wh-question >>`.
* Enter a wh-question comprising only words from the `word_lists/` files, entirely in lower-case and without punctuation, e.g. `who finds the cat that eats the bird quickly`.
* This should return a tuple with a boolean indicating that this is a grammatical wh-question and a list of the parts-of-speech. Note that if the input is not grammatical, the parts-of-speech list will be empty.
* A prompt will ask if you would like to continue to test different input.

### Next Steps

* When, Where, Why, How questions
* Plurals and verb conjugations
* Recursive sentence structures ("The cat the dog chases chases mice.")
* Improved tokenization
* Punctuation handling
* Vocabulary data gathering
