# GloVe Judicial Sentences
==========================

This project uses GloVe ( http://www-nlp.stanford.edu/projects/glove/ ) to generate word embeddings for brazilian portuguese judicial sentence based on Jusbrasil website ( https://www.jusbrasil.com.br ). I have used only sentences related to insurance, but you can easily change it by editing the `gjs/download_indexes.py` file.

## Warning

Since this project scraps Jusbrasil website, it can stop working if they change their html page.

## Executing

- `python gjs/download_indexes.py` -> Downloads all indexes from a jusbrasil specific search
- `python gjs/download_sentences.py` -> Downloads sentences from those indexes
- `python gjs/sentences_to_csv.py` -> Generates phrases csv file

Notebooks:

- `notebooks/glove.ipynb` -> Generates glove model
- `notebooks/tensorboard.ipynb` -> Generates tensorboard projection files

## Observations

- Transform article reference in "artn" word
- Transform document reference in "flsn" word

## Ideas to improve

- Transform any money reference in a word instead of removing it
- Generate using as each sample one entire object instead of a single phrase
- Compare quality with word2vect

