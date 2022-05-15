# C4 Tagger
> "A tagger that follows the footage of TNT Tagger for French semantic tagging"
## 1. Tokens to SEM tags and POS tags
- To run the POS tagger: <br/>
`python analysis.py extract --file <file_path> --pipeline <spacy pipeline>`<br>
  - `--file`: the conll file location <br/>
  - Make sure that you have downloaded the indicated pipeline. <br/>
  - For example, if you want to get SEM and POS tags of data for `it/dev` using `it_core_news_sm` pipeline:<br>
  `python analysis.py extract --file it/train --pipeline it_core_news_sm`
- To see the POS-SEM mutual occurences: <br/>
`python analysis.py inspect --file  <tsv file path> --extract_errors <boolean>`<br/>
  - `--file`: tsv file location
  - `--extract_error`: Choose to or not to extract the filtered sentences<br/>
  - For example, if you want to see the occurences of `it/train.tsv`:<br/>
  `python analysis.py inspect --file  it/train.tsv`

## Z. Interpreter for data exploration
- To run the interpreter: 
<br/>`python interpreter.py interpret`<br/>
The expected input for the programme is the standard PMB ID (XX/YYYY) with XX as the part ID and YYYY as the document ID.
- To update the data (if needed): `python interpreter.py update --l1 <first language> --l2 <second language>`<br/>
For example: `python interpreter.py update --l1 "fr" --l2 "it"` <br/>
Only perform data update when there are changes in the `pmb_french_163.tsv` file.

