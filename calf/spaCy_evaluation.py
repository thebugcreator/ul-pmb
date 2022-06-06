# spaCy evaluation
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
    e = 0
    c = 0
    p = 0
    for i, ch in enumerate(s1):
        if ch == "B" :
            e += 1
            if i < len(s2):
                if s2[i] == "B" : c += 1
        if i < len(s2):
            if s2[i] == "B" : p += 1
    return e, c, p
#################################### main 
nlp = spacy.load("fr_dep_news_trf")
print('loaded spacy...')

f = open("../" + args.file, "r" , encoding = 'utf-8')
fw = open("spaCy_evaluation.txt", "w", encoding = 'utf-8')

head_line = f.readline().split('\t')
for i, item in enumerate(head_line):
    if "French translation" in item : ind_FrSen = i
    if  ("French tokenisation" in item) or ("French tokenization" in item) : ind_FrTok = i
# print(ind_FrSen)
correct = 0
provided = 0
expected = 0

line_mix = f.readline()
while line_mix :
    
    line = line_mix.split('\t')
    sentence = line[ind_FrSen]
    # temp = line[ind_FrTok].strip()
    tokens = line[ind_FrTok].strip().split(' ')
    spaCtokens = nlp(sentence)

    print(sentence, file=fw)
    print('golden -->' , tokens, end='  ,' ,  file=fw)
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
    token = tokens[-1]

    if True : # token[-1] == '\n':
        '''
        if token[0] == ' ':
            l = len(token)-2
            if l>0 :
                iob = "O" + "B" + (l-1)* "I"
                IOBs.append (iob)
                '''
        if len(token) >= 1 :
            l = len(token) - 1
            iob = "B" + (l-1)* "I"
            IOBs.append (iob)
        
    print(IOBs, file= fw) # include the punctuation, but not the newline character
    IOBs_str = "".join(IOBs)

    ###################
    print('[spacy -->'  , *spaCtokens , sep="] [" , end="]   ,"  , file=fw)
    acc = 0 # accumulator for counting the characters
    IOBs = []

    for token in spaCtokens[:-1] : # we ommit the punctuation, because of different syntax. it is always well tokenised.
        l = len(token)
        acc += l
        iob = "B" + (l-1)* "I"
        if sentence[acc] == " ": 
            IOBs.append (iob + "O")
            acc +=1
        else :
            IOBs.append(iob)
    token = spaCtokens[-1]
    l = len(token)
    iob = "B" + (l-1)* "I"
    IOBs.append (iob)

    print(IOBs, file= fw) # include the punctuation, but not the newline character
    spaCyIOBs_str = "".join(IOBs)

    print(IOBs_str, '<-- string of golden IOBs', file=fw)
    print(spaCyIOBs_str, '<-- string of spaCy IOBs', file=fw)
    print(file=fw)
    c = calc(IOBs_str, spaCyIOBs_str)
    expected += c[0]
    correct += c[1]
    provided += c[2]

    line_mix = f.readline()
print(expected,'<-- expected\n', correct, '<-- correct\n', provided, '<-- provided\n', '##########################\n', file=fw)
Precision = correct / provided
Recall = correct / expected
F1 = 2/(1/(Precision) + 1/(Recall))

print('...........Evaluation Results ............', file=fw)
print('Precision: ', Precision, file= fw)
print('Recall: ', Recall, file=  fw)
print('F1-measure: ', F1, file= fw)

######################################

fw.close()
f.close()
    



