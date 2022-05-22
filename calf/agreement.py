#agree.py
# Agreement between the spacy and the tokeniser results
from functions_def import tokenise
import spacy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Corpus Extractor")
    parser.add_argument("--file", type=str, default="pmb_french_163.tsv",  help="name of the file including french sentences.")
    # parser.add_argument('--verbose', help='print out the logs (default: False)', action='store_true')
    args = parser.parse_args()


def calc(s1, s2):
    """
    calculates the expected, correct, and provided "B" tag for eaach sentence. inputs are IOB strings, golden and estimated, respectfully.
    """
    an = 0
    ag = 0
    for i, ch in enumerate(s1):
        if ( ch in "BO" ) : # if ( ch in "BO" ) or (s2[i] in "BO") :
            an += 1
            if i < len(s2):
                if s2[i] == ch : ag += 1
        # if i < len(s2):
        #     if s2[i] == "B" : p += 1
    return an, ag
#############################
nlp = spacy.load("fr_dep_news_trf")
print('loaded spacy...')

# f = open("../pmb_french_163.tsv", "r" , encoding = 'utf-8')
f = open("../" + args.file, "r" , encoding = 'utf-8')
fw = open("agreement.txt", "w", encoding = 'utf-8')


head_line = f.readline().split('\t')
for i, item in enumerate(head_line):
    if item == "French translation": ind_FrSen = i
    if ("French tokenisation" in item) or ("French tokenization" in item) : ind_FrTok = i

annotation = 0
agreement = 0

line_mix = f.readline()
# for i in range(163):
while line_mix :

    line = line_mix.split('\t')
    sentence = line[ind_FrSen]
    # tokens = line[ind_FrTok].split(' ')
    tokens = nlp(sentence)
    print(sentence, file=fw)
    print('[spacy -->'  , *tokens , sep="] [" , end="]   ,"  , file=fw)
    # print(file=fw)
    # forming the IOB tags for tokens
    acc = 0 # accumulator for counting the characters
    IOBs = []

    for token in tokens[:-1] : # we ommit the punctuation, because of different syntax. it is always well tokenised.
        l = len(token)
        acc += l
        iob = "B" + (l-1)* "I"
        if sentence[acc] == " ": 
            IOBs.append (iob + "O")
            acc +=1
        else :
            IOBs.append(iob)
    # IOBs[-1] = IOBs[-1] + "O"

    token = tokens[-1]
    l = len(token)
    iob = "B" + (l-1)* "I"
    IOBs.append (iob)


    print(IOBs, file= fw) # include the punctuation, but not the newline character

    output = tokenise(sentence, True)
    outTokens = output[0]
    outIOBs = output[1]

    IOBs_str = "".join(IOBs)
    outIOBs_str = "".join(outIOBs) # "".join(outIOBs[:-1])
    # outIOBs_str = outIOBs_str[:-1] # we ommit the last space befor the punctuation as well.
    print('[output-->' , *outTokens , sep="] [" , end="]   ," , file=fw)
    print(outIOBs , file=fw)

    print(IOBs_str, '<-- string of spacy IOBs', file=fw)
    print(outIOBs_str, '<-- string of output IOBs', file=fw)
    print(file=fw)

    c = calc(IOBs_str, outIOBs_str)
    annotation += c[0]
    agreement += c[1]

    print(file=fw)
    line_mix = f.readline()


print('\n\n',annotation,'<-- annotation\n', agreement, '<-- agreement\n',  '##########################\n', file=fw)
print('...........Agreement Results ............', file=fw)
print('A0: ', agreement/annotation, file= fw)


fw.close()
f.close()