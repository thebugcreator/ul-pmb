#calf.py : main file to  execute.
from Token import *
from  utils import get_cli_args
from constants import considered_letters, patterns
from functions_def import tokenise
import csv



def extract(indir: str, outdir: str, iob_option: bool):
    """
    Tokenise sentences from a tsv file and output a new file with the original sentence as well as the tokenised version
    :param indir: Input directory
    :param outdir: Output directory
    :param iob_option: Binary option to retrieve the IOB tags
    :return: nothing
    """
    pass

if __name__ == "__main__":
    args = get_cli_args()
    if args.command == "tokenise":
        input_sentence = args.sentence
        input_iob_option = args.iob
        tokenisation_output = tokenise(input_sentence,input_iob_option)
        # print(*tokenisation_output[0])
        # print(tokenisation_output[1])
        # [print(*x, sep='', end=' ') for x in tokenisation_output[2]]
        # print('sentence: ("',input_sentence,'")', sep='')
        print(tokenisation_output.show())
    elif args.command == "extract":
        input_indir = args.indir
        input_outdir = args.outdir
        input_iob_option = args.iob
        extract(input_indir, input_outdir, input_iob_option)
        print(">> Extract successfully!")
    else:
        raise RuntimeError(">> invalid command name!")
