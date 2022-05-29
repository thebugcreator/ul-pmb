# C4 Tagger
> "A tagger that follows the footage of TNT Tagger for French semantic tagging"
## 1. Tokens to SEM tags and POS tags
- To run the POS tagger: <br/>
`python analysis.py extract --file <file_path> --pipeline <spacy pipeline>`<br>
  - `--file`: CONLL file location <br/>
  - Make sure that you have downloaded the indicated pipeline. <br/>
  - For example, if you want to get SEM and POS tags of data for `it/dev` using `it_core_news_sm` pipeline:<br>
  `python analysis.py extract --file it/train --pipeline it_core_news_sm`
  
## 2. POS-SEM tag relation
- To see the POS-SEM projection in format POS - (List of SEM): <br/>
`python analysis.py inspect --file  <tsv file path> --extract_errors <boolean>`<br/>
  - `--lang`: chosen language, for example one of these: \[it, de, en, nl]
  - `--extract_err`: Choose to or not to extract the filtered sentences<br/>
  - For example, if you want to see the occurences of `it/train.tsv`:<br/>
  `python analysis.py inspect --lang  it`

## 3. POS-SEM tag co-occurrences preview
- To get the structure, co-occurrences, and number of occurences of the POS-SEM:<br/>
  `python analysis.py get_cooc --lang <tsv file path> --visualise <Visualisation choice>`
  - `--lang`: chosen language, for example one of these: \[it, de, en, nl]
  - `--stacked`: choose to include different languages, default: `False`
  - `--sample_size`: Choose the number of samples for each language if `stacked`, default `500`
  - `--visualise`: Choose to or not to render a heatmap of co-occurrences. Default: `True`
  - `--savefig`: Choose to or not to save the rendered heatmap of co-occurrences. Default: `True`
  - For example, if you want to see the co-occurrences of POS-SEM for `it/train.tsv`:<br/>
  `python analysis.py get_cooc --lang it --visualise True --savefig True`
  - Or, POS-SEM co-occurrences in different languages (for instance EN and DE):<br/>
  `python analysis.py get_cooc --lang en,de --stacked True --visualise True --savefig True`
## Z. Interpreter for data exploration
- To run the interpreter: 
<br/>`python interpreter.py interpret`<br/>
The expected input for the programme is the standard PMB ID (XX/YYYY) with XX as the part ID and YYYY as the document ID.
- To update the data (if needed): `python interpreter.py update --l1 <first language> --l2 <second language>`<br/>
For example: `python interpreter.py update --l1 "fr" --l2 "it"` <br/>
Only perform data update when there are changes in the `pmb_french_163.tsv` file.

