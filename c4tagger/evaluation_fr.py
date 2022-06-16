from analysis import get_tagging_rules
from analysis import get_data_from_tsv
from analysis import get_cooccurrences
from tagger import manual_tagging
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

# %%

# Get the language bounded resources

it_rules = get_tagging_rules("it", sample_size=1000)
it_in_cooc_df = get_cooccurrences("it")

en_rules = get_tagging_rules("en", sample_size=1000)
en_in_cooc_df = get_cooccurrences("en")

indf = get_data_from_tsv("fr")

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
it_based_out_sem = []
en_based_out_sem = []
for item in in_pos:
    it_based_out_sem.append(manual_tagging(item, it_rules))
    en_based_out_sem.append(manual_tagging(item, en_rules))

it_out_acc_scores = dict()
en_out_acc_scores = dict()
err_docs = []
for i in range(len(in_sem_eve)):
    if len(in_sem_eve[i]) != len(it_based_out_sem[i]) or len(in_sem_eve[i]) != len(en_based_out_sem[i]):
        # print(in_tok[i], in_pos[i], in_sem_eve[i], out_sem[i], sep="\n")
        # print("-----------------------------")
        err_docs.append(i)
        continue
    it_out_acc_scores[i] = metrics.accuracy_score(in_sem_eve[i], it_based_out_sem[i])
    en_out_acc_scores[i] = metrics.accuracy_score(in_sem_eve[i], en_based_out_sem[i])

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Accuracy scores for IT-FR and EN-FR tag projection')
ax1.boxplot(it_out_acc_scores.values())
ax2.boxplot(en_out_acc_scores.values())
ax1.set_title("IT-FR")
ax2.set_title("EN-FR")
plt.show()

print("Mean accuracy IT:", np.mean([item for item in it_out_acc_scores.values()]))
print("Median accuracy IT:", np.median([item for item in it_out_acc_scores.values()]))

print("Mean accuracy EN:", np.mean([item for item in en_out_acc_scores.values()]))
print("Median accuracy EN:", np.median([item for item in en_out_acc_scores.values()]))
print("Bad documents: {0}/{1}".format(len(err_docs), len(in_pos)))

for k, v in it_out_acc_scores.items():
    if v < 0.3:
        print(in_tok[k], in_pos[k], in_sem_eve[k], it_based_out_sem[k], sep="\n")