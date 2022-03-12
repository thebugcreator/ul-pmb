# Analytic libs
import pandas as pd
# Scraping libs
from bs4 import BeautifulSoup
from requests import get
# Interpretation

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

    for i in range(idx_base, idx_last + 1):
        token = content_idm3.find("td", title="token {}".format(i)).text
        if len(token.split(" ")) > 1:
            token = "~".join(token.split(" "))
        semtag = content_idm3.find("td", id="semtag_i{}".format(i)).text[:3]
        tokens.append(token)
        semtags.append(semtag)
    return " ".join(tokens), " ".join(semtags)


def get_bilingual_data(in_df) -> pd.DataFrame:
    ids = in_df["ID"]
    fr_tokens = []
    fr_semtags = []
    it_tokens = []
    it_semtags = []
    _type = "der.xml"
    for item in ids:
        _id = item.split("/")
        try:
            fr_token, fr_semtag = get_sentence_data(*_id, _type, "fr")
            it_token, it_semtag = get_sentence_data(*_id, _type, "it")
        except:
            fr_token, fr_semtag, it_token, it_semtag = [], [], [], []
        fr_tokens.append(fr_token)
        fr_semtags.append(fr_semtag)
        it_tokens.append(it_token)
        it_semtags.append(it_semtag)
    out_df = pd.DataFrame()
    out_df["id"] = ids
    out_df["fr_token"] = fr_tokens
    out_df["fr_semtag"] = fr_semtags
    out_df["it_token"] = it_tokens
    out_df["it_semtag"] = it_semtags
    return out_df


def read_raw_data() -> pd.DataFrame:
    return pd.read_csv("raw.tsv", sep="\t", encoding="utf-8")


def save_raw_data(in_df: pd.DataFrame):
    in_df.to_csv("raw.tsv", index=False, encoding="utf-8", sep="\t")
    pass


def interpret(in_df):
    while True:
        chosen_id = input("> Input the sentence ID to interpret: ")
        if chosen_id.lower() == "exit" or chosen_id.lower() == "quit":
            break
        else:
            chosen_item = in_df[in_df["id"] == chosen_id]
            if len(chosen_item):
                print("----------FR-----------")
                for index, value in chosen_item[["fr_token", "fr_semtag"]].iterrows():
                    tokens = value["fr_token"].split(" ")
                    semtags = value["fr_semtag"].split(" ")
                    for i in range(len(tokens)):
                        print(tokens[i].ljust(20), semtags[i])
                print("----------IT-----------")
                for index, value in chosen_item[["it_token", "it_semtag"]].iterrows():
                    tokens = value["it_token"].split(" ")
                    semtags = value["it_semtag"].split(" ")
                    for i in range(len(tokens)):
                        print(tokens[i].ljust(20), semtags[i])
