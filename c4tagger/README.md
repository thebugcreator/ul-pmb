# C4 Tagger
> "A tagger that follows the footage of TNT Tagger for French semantic tagging"

## Z. Interpreter for data exploration
- To run the interpreter: 
<br/>`python interpreter.py interpret`<br/>
The expected input for the programme is the standard PMB ID (XX/YYYY) with XX as the part ID and YYYY as the document ID.
- To update the data (if needed): `python interpreter.py update --l1 <first language> --l2 <second language>`<br/>
For example: `python interpreter.py update --l1 "fr" --l2 "it"` <br/>
Only perform data update when there are changes in the `pmb_french_163.tsv` file.
