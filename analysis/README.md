# Analysing the NLTK and Spacy French tokenisers using manually annotated data.
## I. Employment of methods and libraries
### 1. NLTK
- Methods: `word_tokenize as wt` and `WordPunctTokenizer as wp` 
- Result: From the 163 tokenised sentences provided by both wt and wp, they share 123 similar results.
- Differences: In the remained 40 sentences, the main differences are the criteria of different approaches.
All these sentences contain one or many symbols in the middle of the sentence such as the French clitics `'`, hyphens `-`, the dots `.` after titles or acronyms.
### 2. Spacy
- Pipelines: `fr_core_news_sm as sm` and `fr_core_news_md as md`
- Result: From the 163 tokenised sentences provided by both sm and md, they share 163 similar results.
- Difference: None
### 3. Calf
- Criteria:
- Result:
- Difference:
## II. Discussion
### Difficult cases
- Both NLTK and Spacy failed to recognise named entities
- Both NLTK and Spacy failed to recognise context-wise frozen tokens such as `il y a`
- NLTK failed to recognise clitics while Spacy seemed to be successful in handling this job
- There doesn't exist data for euphonic T's for verification. This will be examined later.