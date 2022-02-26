#old functions
def tokenise(sentence: str, iob_option, by_contract = True, cut_mod = False):
    """
    Precondition: The sentence must be well-formed. There should be a space before the terminal symbol.
    :param iob_option: binary option for the IOB tag retrieval
    :param sentence: The sentence to tokenise
    :return: a 2-tuple. The first one is for the token array, the second one is for the IOB tags
    """

    # if len(sentence) == 0 : sentence = examples[0]
    # Take care of the terminal symbol
    if  ( sentence[-1] not in considered_letters ) and  by_contract :
        # If there's not a space before the terminal symbol, add one
        if sentence[-2] != " ":
            well_formed_sentence = sentence[0:-1] + " " + sentence[-1]
            sentence = well_formed_sentence
    ######
    # Semi- Cutter based approach. we consider a sentence as a character sequence, 
    # which will be splited in sebsequences and tokens. and so on. 
    CharSeq_list = [CharSeq(sentence)]  # list of Character_Sequeneces owhich could be CharSeq objects or SolidToken
    #

    # 
    if cut_mod is True :
        for phrs in especials :
            CharSeq_list_new = []
            for  charseq in CharSeq_list :
                if type(charseq) is CharSeq  : # and charseq.is_token == False
                    CharSeq_list_new.extend( apllyRule (charseq, phrs) )
                else :   # elif type(charseq) is SolidToken : 
                    CharSeq_list_new.append(charseq)
            CharSeq_list = CharSeq_list_new

        refined_quote_seg = []
        iob =[]
        iob_tokens = []
        for charseq in CharSeq_list :
            if type(charseq) is CharSeq :
                temp = tokenise(charseq.string, iob_option, cut_mod = False, by_contract = False)
                refined_quote_seg.extend( temp[0] )
                iob.extend(temp[1])
                iob_tokens.extend(temp[2])

            elif type(charseq) is PhraseToken :
                for item in charseq.items :
                    refined_quote_seg.append( Token(item) )
                    if iob_option :
                        iob_token = []
                        for i, j in enumerate(item) :
                            if i == 0: 
                                iob.append("B")
                                iob_token.append("B")
                            else :
                                iob.append("I")
                                iob_token.append("I")
                        iob_tokens.append(iob_token)
        return (refined_quote_seg, iob, iob_tokens)
    
    if cut_mod is False : 
        # Split the sentence using a space as separator
        if by_contract :
            space_seg = sentence.split(" ")
        # else :
        #     temp =  sentence.split(" ")
        #     if temp[0] == '' : first_sp = True
        #     if temp[-1] == '' : last_sp = True
        #     sent =sentence.strip()
        #     space_seg = sent.split(" ")



        # Take care of comma 
        sentence_seg = []
        for item in space_seg :
            if len (item) >1 and item[-1] == ',' :
                sentence_seg.append(item[:-1])
                sentence_seg.append(',')
            elif len(item) >0 :
                sentence_seg.append(item)
        space_seg = sentence_seg #just in case not to mess up the rest of the code

        #Take care of some especial cases
        for phrs in phrases :
            new_seg = []
            for seg in sentence_seg :
                if seg == phrs :
                    new_seg.extend( phrases[phrs] )
                else:
                    new_seg.append( seg )
            sentence_seg = new_seg
        space_seg = sentence_seg
    
        # Take care of dash between two words
        # temp_seg = []
        # for item in sentence_seg :
        #     if '-' in item and len(item)>1 :
        #         temp_seg.extend( item.split('-') )
        #     else :
        #         temp_seg.append(item)
        # space_seg = temp_seg # renaming because of not disturbing rest of the code

        ##
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

        # Take care of the named entities. # What if named entities come the second place?  
        # This grip is to skip the unnecessary loops
        grip = 0
        for i in range( len(quote_seg) ):
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
            iob_token = []
            iob_tokens = []
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
            return (refined_quote_seg, iob, iob_tokens)
        return (refined_quote_seg, [], [])