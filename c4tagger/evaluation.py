from analysis import get_tagging_rules
from analysis import get_data_from_tsv
from analysis import get_cooccurrences
from tagger import manual_tagging
from sklearn import metrics
import numpy as np

# %%
# Get the language bounded resources
language = "it"
rules = get_tagging_rules(language, sample_size=1000)
indf = get_data_from_tsv(language)
in_cooc_df = get_cooccurrences(language)

# Declare the tags belonging to the EVE (events, not midnights) family
#   Johan Bos et al. 2017
eves = ["EXS", "ENS", "EPS", "EXG", "EXT"]

# %%

# Get the input tokens, input POS tags, and input SEM tags
in_tok = indf["tok"].values  # Tokens
in_pos = [item.split(" ") for item in indf["pos"].values]  # POS tags
in_sem = [item.split(" ") for item in indf["sem"].values]  # SEM tags

# Process the sem tag for the input set
# Turn the tags in the family to its super-tag
in_sem_eve = []
for item in in_sem:
    mini_sem_list = []
    for tag in item:
        if tag in eves:  # If the tag is found to be favoured
            mini_sem_list.append("EVE")  # SUPER-TAG
        else:
            mini_sem_list.append(tag)  # Just pass it
    in_sem_eve.append(mini_sem_list)


# Do the tagging
out_sem = []
for item in in_pos:
    out_sem.append(manual_tagging(item, rules))

out_acc_scores = dict()
out_err_doc = 0
for i in range(len(in_sem_eve)):
    if len(in_sem_eve[i]) != len(out_sem[i]):
        out_err_doc += 1
        print(in_tok[i], in_pos[i], in_sem_eve[i], out_sem[i], sep="\n")
        print("-----------------------------")
        continue
    out_acc_scores[i] = metrics.accuracy_score(in_sem_eve[i], out_sem[i])

print("Mean accuracy:", np.mean([item for item in out_acc_scores.values()]))
print("Bad documents:", out_err_doc)
