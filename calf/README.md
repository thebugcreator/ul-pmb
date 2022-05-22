#  Guideline to run CALF the mini Elephant tokeniser:
## 1. Tokenising a single sentence:
Arguments:
<ul>
<li>--sentence: The sentence to tokenise</li>
<li>--iob: True to retrieve the IOB tags, False otherwise</li>
</ul>
For example, to tokenise the sentence "Ne soyez pas paresseux !"

`python calf.py tokenise --sentence "Ne soyez pas paresseux !"`

Output: `([Ne, soyez, pas, paresseux, !], [])`

To tokenise that sentence and get the IOB tags as a byproduct:

`python calf.py tokenise --sentence "Ne soyez pas paresseux !" --iob True`

Output: 

`Ne soyez pas paresseux !`

`BIO BIIIIO BIIO BIIIIIIIIO B`
## 2. Tokenising a number of sentences in a tsv file:
Arguments:
<ul>
<li>First argument is the input file directory</li>
<li>--outdir: The output file directory</li>
<li>--iob: True to retrieve the IOB tags, False otherwise</li>
</ul>
For example, to tokenise the sentences in the file located at "../demos/input.tsv" and settle the result as "../demos/output.tsv":

`python calf.py extract "../demos/input.tsv" --outdir "../demos/output.tsv"`

Feel free to add your IOB option

`python calf.py extract "../demos/input.tsv" --outdir "../demos/output.tsv" --iob=True`

## 3. Evaluation over golden data:
Run the command `python evaluation.py` with optional argument:
<ul>
	<li> --file : should be followed by the name of the file containing extention (.tsv) located in the parent folder </li>li>
</ul>

the result will be stored in a text file named `evaluation.txt` in the current folder.

## 4. Agreement with spaCy :
Run the command `python agreement.py` with optional argument:
<ul>
	<li> --file : should be followed by the name of the file containing extention (.tsv) located in the parent folder </li>li>
</ul>

the result will be stored in a text file named `agreement.txt` in the current folder.
