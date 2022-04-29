#eval.py
# Evaluating the tokeniser results over gold data.
from functions_def import tokenise
# import spacy

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
#############################
# nlp = spacy.load("fr_dep_news_trf")

f = open("../pmb_french_163.tsv", "r" , encoding = 'utf-8')
fw = open("evaluation.txt", "w", encoding = 'utf-8')
head_line = f.readline().split('\t')
for i, item in enumerate(head_line):
    if item == "French translation": ind_FrSen = i
    if  "French tokenisation" in item: ind_FrTok = i
# print(ind_FrSen)
# print(ind_FrTok)
correct = 0
provided = 0
expected = 0
for i in range(163):
    line = f.readline().split('\t')
    sentence = line[ind_FrSen]
    tokens = line[ind_FrTok].split(' ')
    print(sentence, file=fw)
    print('golden -->' , tokens, end='  ,' ,  file=fw)
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

    if token[-1] == '\n':
        if token[0] == ' ':
            l = len(token)-2
            if l>0 :
                iob = "O" + "B" + (l-1)* "I"
                IOBs.append (iob)
        elif len(token) > 1 :
            l = len(token) - 1
            iob = "B" + (l-1)* "I"
            IOBs.append (iob)



    print(IOBs, file= fw) # include the punctuation, but not the newline character

    output = tokenise(sentence, True)
    outTokens = output[0]
    outIOBs = output[1]

    IOBs_str = "".join(IOBs)
    outIOBs_str = "".join(outIOBs) # "".join(outIOBs[:-1])
    # outIOBs_str = outIOBs_str[:-1] # we ommit the last space befor the punctuation as well.
    print('output -->' , outTokens , end='  ,' , file=fw)
    print(outIOBs , file=fw)

    print(IOBs_str, '<-- string of golden IOBs', file=fw)
    print(outIOBs_str, '<-- string of output IOBs', file=fw)
    print(file=fw)
    c = calc(IOBs_str, outIOBs_str)
    expected += c[0]
    correct += c[1]
    provided += c[2]
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