# Analytic libs
import pandas as pd
# Scraping libs
from bs4 import BeautifulSoup
from requests import get
# Interpretation
import utils


df = pd.read_csv("../pmb_french_163.tsv", encoding="utf-8", sep="\t")


def get_sentence_data(part, docid, arg_type, language):
    url = "https://pmb.let.rug.nl/explorer/explore.php?part={0}&doc_id={1}&type={2}&alignment_language={3}".format(part,
                                                                                                                   docid,
                                                                                                                   arg_type,
                                                                                                                   language)
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    content_idm3 = soup.find("tr", id="content_idm3")
    idx_base = 1001
    tokens = []
    semtags = []
    try:
        terminal = content_idm3.contents[1]
        idx_last = int((terminal.find("table").attrs["id"])[1:])
    except IndexError:
        idx_last = 1000 + len(content_idm3.find_all("table", class_="lex"))
    except ValueError:
        return "", ""
    for i in range(idx_base, idx_last + 1):
        token = content_idm3.find("td", title="token {}".format(i)).text
        if len(token.split(" ")) > 1:
            token = "~".join(token.split(" "))
        semtag = content_idm3.find("td", id="semtag_i{}".format(i)).text[:3]
        tokens.append(token)
        semtags.append(semtag)
    return " ".join(tokens), " ".join(semtags)


def get_pos_tags(sentence, language):
    pos_tags = []
    if sentence:
        pipeline = utils.get_pipeline(language)
        document = pipeline(sentence)
        for token in document:
            pos_tags.append(token.pos_)
    return pos_tags


def get_bilingual_data(in_df, _l1, _l2) -> pd.DataFrame:
    ids = in_df["ID"]
    l1_tokens = []
    l1_semtags = []
    l1_postags = []
    l2_tokens = []
    l2_semtags = []
    l2_postags = []
    _type = "der.xml"
    for item in ids:
        _id = item.split("/")
        try:
            l1_token, l1_semtag = get_sentence_data(*_id, _type, _l1)
            l1_postag = " ".join(get_pos_tags(l1_token, _l1))
            l2_token, l2_semtag = get_sentence_data(*_id, _type, _l2)
            l2_postag = " ".join(get_pos_tags(l2_token, _l2))
        except:
            l1_token, l1_semtag, l2_token, l2_semtag = "", "", "", ""
            l1_postag, l2_postag = "", ""
        l1_tokens.append(l1_token)
        l1_semtags.append(l1_semtag)
        l1_postags.append(l1_postag)
        l2_tokens.append(l2_token)
        l2_semtags.append(l2_semtag)
        l2_postags.append(l2_postag)
    out_df = pd.DataFrame()
    out_df["id"] = ids
    out_df["l1_token"] = l1_tokens
    out_df["l1_semtag"] = l1_semtags
    out_df["l1_postag"] = l1_postags
    out_df["l2_token"] = l2_tokens
    out_df["l2_semtag"] = l2_semtags
    out_df["l2_postag"] = l2_postags
    return out_df


def read_raw_data() -> pd.DataFrame:
    return pd.read_csv("raw.tsv", sep="\t", encoding="utf-8")


def save_raw_data(in_df: pd.DataFrame):
    in_df.to_csv("raw.tsv", index=False, encoding="utf-8", sep="\t")
    pass


def interpret(in_df):
    while True:
        print("> To quit, input exit or quit.")
        chosen_id = input("> Input the sentence ID: ")
        if chosen_id.lower() == "exit" or chosen_id.lower() == "quit":
            break
        else:
            chosen_item = in_df[in_df["id"] == chosen_id]
            if len(chosen_item):
                print("----------L1-----------")
                tok1 = chosen_item["l1_token"].values[0].split(" ")
                sem1 = chosen_item["l1_semtag"].values[0].split(" ")
                pos1 = chosen_item["l1_postag"].values[0].split(" ")
                for i in range(len(tok1)):
                    print(tok1[i].ljust(20), sem1[i].ljust(10), pos1[i].rjust(10))
                print("----------L2-----------")
                tok2 = chosen_item["l2_token"].values[0].split(" ")
                sem2 = chosen_item["l2_semtag"].values[0].split(" ")
                pos2 = chosen_item["l2_postag"].values[0].split(" ")
                for i in range(len(tok2)):
                    print(tok2[i].ljust(20), sem2[i].ljust(10), pos2[i].rjust(10))


if __name__ == "__main__":
    args = utils.get_cli_args()
    if args.command == "interpret":
        interpret(read_raw_data())
    elif args.command == "update":
        l1 = args.l1
        l2 = args.l2
        save_raw_data(get_bilingual_data(df, l1, l2))
        print(">> Update successfully!")
    else:
        raise RuntimeError(">> Invalid command!")
