from functions_def import tokenise
from utils import get_cli_args
import pandas as pd


def extract(indir: str, outdir: str, iob_option: bool):
    """
    Tokenise sentences from a tsv file and output a new file with the original sentence as well as the tokenised version
    :param indir: Input directory
    :param outdir: Output directory
    :param iob_option: Binary option to retrieve the IOB tags
    :return: nothing
    """
    df = pd.read_csv(indir)
    outputs = []
    for index, value in df.iterrows():
        tokens = tokenise(value["French translation"], iob_option=iob_option)
        outputs.append(str(tokens).strip())
    outdf = pd.DataFrame()
    outdf["literals"] = df["French translation"]
    outdf["tokens"] = outputs
    outdf.to_csv(outdir, sep="\t", encoding="UTF-8", index=False)
    return outdf.size


if __name__ == "__main__":
    args = get_cli_args()
    if args.command == "tokenise":
        input_sentence = args.sentence
        input_iob_option = args.iob
        tokenisation_output = tokenise(input_sentence, input_iob_option)
        print(tokenisation_output.show())
    elif args.command == "extract":
        input_indir = args.indir
        input_outdir = args.outdir
        input_iob_option = args.iob
        extract(input_indir, input_outdir, input_iob_option)
        print(">> Extract successfully!")
    else:
        input_sentence = input(" :")
        tokenisation_output = tokenise(input_sentence)

        # raise RuntimeError(">> invalid command name!")
