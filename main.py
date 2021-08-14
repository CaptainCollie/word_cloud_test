import datetime as dt
import requests
import json
from apikey import apikey
from collections import Counter
import nltk
import enchant
import matplotlib.pyplot as plt
from wordcloud import WordCloud

date = dt.datetime.today()
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
text = ''
for i in range(31):
    day = (date - dt.timedelta(days=i)).strftime("%Y-%m-%d")
    print(day)
    response = requests.get(
        f'https://newsapi.org/v2/everything?q=russia&pageSize=100&page=1&from={day}&to='
        f'{day}&apiKey={apikey}').text
    json_text = json.loads(response)
    articles = json_text.get('articles')
    if articles:
        for j in articles:
            article_text = j.get('content')
            if article_text not in text:
                text += ' ' + article_text


useless = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", 'chars', 'del', 'con', 'today',
           'week', 'year', 'month', 'day']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
useless += months
useless = [i.lower() for i in useless]

d = enchant.Dict('en_US')

text = text.lower()
tokens = nltk.word_tokenize(text)
tags = nltk.pos_tag(tokens)
themes = [word for word, pos in tags if
          (pos == 'NN' or pos == 'NNP' or pos == 'NNPS') and word.isalpha() and word not in useless and d.check(
              word) and len(word) > 2]

di = Counter(themes).most_common(50)
word_dic = {}
for i in di:
    word_dic.setdefault(i[0], i[1])

wc = WordCloud(background_color='white', width=1920, height=1080).generate_from_frequencies(word_dic)
plt.figure(figsize=(16, 9))
plt.imshow(wc)
plt.axis('off')
plt.show()
