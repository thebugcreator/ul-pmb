from Token import Token
from utils import get_cli_args
from constants import considered_letters
import csv


def tokenise(sentence: str, iob_option):
    """
    Precondition: The sentence must be well-formed. There should be a space before the terminal symbol.
    :param iob_option: binary option for the IOB tag retrieval
    :param sentence: The sentence to tokenise
    :return: a 2-tuple. The first one is for the token array, the second one is for the IOB tags
    """

    if len(sentence) == 0 : sentence ="J'habite à Nancy, il y a une boulangerie, dites-moi où tu habites, qu'est-ce qu'il y a au cinéma?"

    # Take care of the terminal symbol
    #"J'habite à Nancy, il y a une boulangerie, que faites-vous chez vous, dites-moi où vous habitez ?" 
    if sentence[-1] not in considered_letters:
        # If there's not a space before the terminal symbol, add one
        if sentence[-2] != " ":
            well_formed_sentence = sentence[0:-1] + " " + sentence[-1]
            sentence = well_formed_sentence
    
    # Take care of some phrases
    phras = { "Qu'est-ce": "Qu_est_ce" , "qu'est-ce": "qu_est_ce",  'il y a':'il_y_a'} # 'il y a':'il_y_a', 'Il y a':'Il_y_a'
    new_sentence = sentence
    for pop, tech in phras.items() :   
        while True:
            ind = sentence.find(pop)
            if ind >= 0 : 
                new_sentence = sentence[:ind] + tech + sentence[ind+len(pop): ] 
                sentence = new_sentence
            else : break
        # sentence = new_sentence

    # Split the sentence using a space as separator
    space_seg = sentence.split(" ")

    # Take care of comma 
    sentence_seg = []
    for item in space_seg :
        if len (item) >1 and item[-1] == ',' :
            sentence_seg.append(item[:-1])
            sentence_seg.append(',')
        elif len(item) >0 :
            sentence_seg.append(item)
    
    # Take care of dash between two words
    temp_seg = []
    for item in sentence_seg :
        if '-' in item and len(item)>1 :
            temp_seg.extend( item.split('-') )
        else :
            temp_seg.append(item)

    space_seg = temp_seg # renaming because of not disturbing rest of the code
    quote_seg = []
    refined_quote_seg = []

    # Take care of the quotes
    for item in space_seg:
        # If a quote found, separate the combination into two elements
        if "'" in item:
            # The first element gets the quote as it's asset
            quote_seg.append(item.split("'")[0] + "'")
            quote_seg.append(item.split("'")[1])
        # If no quote found, just add it as it is
        else:
            quote_seg.append(item)

    # Take care of the named entities
    # This grip is to skip the unnecessary loops
    grip = 0
    for i in range(len(quote_seg)):
        # Skip the loop if already processed
        if i < grip:
            continue
        # If a uppercase letter found in a separation, search it's elements
        if quote_seg[i][0] in considered_letters.upper():
            for j in range(i + 1, len(quote_seg)):
                if not quote_seg[j][0] in considered_letters.upper():
                    refined_quote_seg.append(Token(*quote_seg[i:j]))
                    # Set the grip to avoid redundant loops
                    grip = j
                    break
        else:
            refined_quote_seg.append(Token(quote_seg[i]))
    if iob_option:
        iob =[]
        iob_tokens = []
        iob_token = []
        i = -1 # next loop counter
        # Take care of the IOB tags
        for token in refined_quote_seg:
            i += 1
            if i > 0 : iob_tokens.append(iob_token)
            iob_token =[]
            # Beginning of the token
            iob.append("B")
            iob_token.append("B")
            # Token's inners
            for smt in range(len(token.representation) - 1):
                iob.append("I")
                iob_token.append("I")
            # Do not add an token's outer if there exists a quote
            if "'" in token.representation:
                continue
            # Handle the end of the sentence
            elif token is refined_quote_seg[-1]:
                continue
            # Taking care of comma in IOB presentation. Do not add an token's outer if there exists a comma delimiter.
            elif i<len(refined_quote_seg)-1 and ( ',' in refined_quote_seg[i+1].representation   ) : 
                continue
            # Add a token outer
            else:
                iob.append("O")
                iob_token.append("O")
        iob_tokens.append(iob_token)

        return refined_quote_seg, iob_tokens
    return refined_quote_seg, []


def extract(indir: str, outdir: str, iob_option: bool):
    """
    Tokenise sentences from a tsv file and output a new file with the original sentence as well as the tokenised version
    :param indir: Input directory
    :param outdir: Output directory
    :param iob_option: Binary option to retrieve the IOB tags
    :return: nothing
    """
    sentences = []
    with open(indir, encoding="utf8") as f:
        for line in f:
            # Remove the carriage returns
            refined_line = line.strip()
            # A single line to write into the file
            # Add the original sentence as the first element
            tmp_line = [refined_line]
            # Tokenise the sentence
            tmp_output = tokenise(refined_line, iob_option)
            # Add the tokenised sentence into the line
            tmp_tokens = " ".join([str(token) for token in tmp_output[0]])
            tmp_line.append(tmp_tokens)
            if iob_option:
                # Add the IOB tags into the line
                tmp_line.append("".join(tmp_output[1]))
            # Add the line into the list to write
            sentences.append(tmp_line)

    with open(outdir, 'w', encoding="utf8", newline="") as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerows(sentences)
    pass


if __name__ == "__main__":
    args = get_cli_args()
    if args.command == "tokenise":
        input_sentence = args.sentence
        input_iob_option = args.iob
        tokenisation_output = tokenise(input_sentence,input_iob_option)
        
        print(*tokenisation_output[0])
        # print(tokenisation_output[1])
        [print(*x, sep='', end=' ') for x in tokenisation_output[1]]
        print()
        print('(',input_sentence,')')
    elif args.command == "extract":
        input_indir = args.indir
        input_outdir = args.outdir
        input_iob_option = args.iob
        extract(input_indir, input_outdir, input_iob_option)
        print(">> Extract successfully!")
    else:
        raise RuntimeError(">> invalid command name!")
