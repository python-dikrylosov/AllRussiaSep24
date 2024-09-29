import pandas as pd
from sentence_transformers import SentenceTransformer
import json
from tqdm.autonotebook import tqdm
import numpy as np
import faiss

data = pd.read_csv("test.csv")[['video_id', 'title']]
taxonomy = pd.read_csv("IAB_tags.csv")

print(data.columns)
print(data.head(5))

print(taxonomy.head(5))
print(taxonomy.columns)
model = SentenceTransformer('hunkim/sentence-transformer-klue',)#('DeepPavlov/rubert-base-cased-sentence', )
dim = 768 # размер вектора эмбеддинга
data['title_vector'] = data['title'].apply(lambda l: model.encode(l, convert_to_tensor=True).cpu().numpy())
def get_tags():
    tags = {}
    for i, row in tqdm(taxonomy.iterrows()):
        if isinstance(row['Уровень 1 (iab)'], str):
            tags[row['Уровень 1 (iab)']] = model.encode(row['Уровень 1 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
        if isinstance(row['Уровень 2 (iab)'], str):
            tags[row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)']] = model.encode(row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
        if isinstance(row['Уровень 3 (iab)'], str):
            tags[row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)']+": "+row['Уровень 3 (iab)']] = model.encode(row['Уровень 1 (iab)']+ ": "+row['Уровень 2 (iab)']+": "+row['Уровень 3 (iab)'], convert_to_tensor=True).cpu().numpy()#.tolist()
    return tags


tags = get_tags()
tags_list = list(tags.keys())
vectors = np.array(list(tags.values()))
index = faiss.index_factory(dim, "Flat", faiss.METRIC_INNER_PRODUCT)
print(index.ntotal)
index.add(vectors)
print(index.ntotal)
topn = 3
scores, predictions = index.search(np.array(data['title_vector'].to_list()[:10]), topn)
for j, i in enumerate(predictions):
    print("SCORES", scores[j])
    print("PREDICTION_by_title", np.array(tags_list)[predictions[j]])
    print("SAMPLE", data['title'].to_list()[:10][j])
    print("\n")

topn=1
sample_submission = pd.DataFrame(data=data['video_id'].to_list(), columns=['video_id'])
sample_submission['predicted_tags']=np.nan
sample_submission['predicted_tags'] = sample_submission['predicted_tags'].astype('object')

for i, row in data.iterrows():
    scores, predictions = index.search(np.array([row['title_vector']]), topn)
    index_i = sample_submission[sample_submission.video_id == row.video_id].index
    sample_submission.at[index_i[0], 'predicted_tags'] = [tags_list[predictions[0][0]]] # вытаскиваем предсказание из
    print(sample_submission.head(5))

sample_submission.to_csv("sample_submissionEND.csv", index_label=0)