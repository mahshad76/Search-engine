import pickle
import re
import pandas as pd
import hazm as hz
import math
import numpy as np
import pickle
import math
import heapq

stop_words= pd.read_excel (r'C:\Users\Mohammadreza Rahmani\Desktop\stop.xlsx').values.tolist()
stop_words=[inner for outer in stop_words for inner in outer]
signs=['Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', '\xad', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž']
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub(' ', text)
def normalizeArabic(text):
        text = re.sub("[إأٱآا]", "ا", text)
        text = re.sub("ي", "ی", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("[ةـة]", "ت", text)
        text = re.sub("ك", "ک", text)
        text = re.sub("ۀ", "ء", text)
        return (text)
def deNoise(text):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return text
def add_space_between_emojies(text):
  EMOJI_PATTERN = re.compile(
    "(["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "])"
  )
  text = re.sub(EMOJI_PATTERN, r' \1 ', text)
  return text
def tokenize(string):
    prefix_v_n=['می','فرو','فرا','نمی']
    for prefix in prefix_v_n:
        if prefix in string:
            string=string.replace(prefix+" ",prefix+"\u200c")
    post_n_v = ['ها', 'تر', 'ترین', 'مان', 'هایمان', 'هایشان', 'هایتان', 'هایم', 'هایت', 'هایش',
                 'ام', 'اش', 'امان', 'اتان', 'هاتان', 'هاشان', 'یم', 'یت', 'یمان', 'یتان', 'یشان', 'گری', 'تری', 'گر',
                 'یش', 'هامان', 'اشان', 'های', 'ی', 'ای','ام','ایم','اید','اند' ,'ات']
    for post in post_n_v:
        if post in string:
            string=string.replace(" "+post,"\u200c"+post)
    combinations = {'علی ای حال': 'علی\u200cای\u200cحال',
                    'بنا بر این': 'بنا\u200cبر\u200cاین',
                    'چنان چه': 'چنان\u200cچه',
                    'فی کل حال': 'فی\u200cکل\u200cحال',
                    'فی ما بین': 'فی\u200cما\u200cبین',
                    'در واقع': 'در\u200cواقع',
                    'کلهم اجمعین': 'کلهم\u200cاجمعین',
                    'فی المثل': 'فی\u200cالمثل',
                    'اگر چه': 'اگر\u200cچه',
                    'من حیث المجموع': 'من\u200cحیث\u200cالمجموع',
                    'فی مدت المعلوم': 'فی\u200cمدت\u200cالمعلوم',
                    'فی البداهه': 'فی\u200cالبداهه',
                    'فی مابین': 'فی\u200cمابین',
                    'جا به جا':'جا\u200cبه\u200cجا',
                    'علی ای حال':'علی\u200cای\u200cحال',
                    'گرچه':'گر\u200cچه',
                    'مع ذالک': 'مع\u200cذالک'
                    }
    keys=combinations.keys()
    for k in keys:
        if k in string:
            string=string.replace(k,combinations.get(k))
    return string

query=input("enter your query:"+'\n')
query = remove_tags(query)
for ch in ['\\', ':', '/', '*', '_', '{', '}', '[', ']', '(', ')', '>', '<', '#', '+', '-', '.', '!', '\'',
                   ';', '"', '?','؟', '@', '$', '%', '^', '&', '~', "'", '|', '،', '=', '؛', ',']:
            if (ch in query):
                query = query.replace(ch, ' ')
query = re.sub(r"[0-9]", " ", query)
for word in ['raquo', 'laquo', 'lt', 'gt', 'bull', 'hearts', 'diams', 'clubs', 'spades', 'mdash', 'nbsp']:
            if (word in query):
                query = query.replace(word, ' ')
for ch in ['۰', '٠', '۱', '١', '۲', '٢', '۳', '٣', '۴', '٤', '۵', '٥', '۶', '٦', '۷', '٧', '۸', '٨', '۹', '٩']:
            if ch in query:
                query = query.replace(ch, ' ')
li = query.split()
li = [word for word in li if word not in stop_words]
query = ' '.join(li)
query=normalizeArabic(deNoise(query))
query=add_space_between_emojies(query)
for ch in signs:
            if (ch in query):
                query=query.replace(ch,' '+ch+' ')
query=tokenize(query)
res=[]
stemmer = hz.Stemmer()
lemmatizer = hz.Lemmatizer()
for word in query.split():
            limit = lemmatizer.lemmatize(stemmer.stem(word))
            if ('#' in limit):
                limit = limit.split('#')
                res.append(limit[0])
            else:
                res.append(limit)
query = ' '.join(res)
tokens=query.split()

frequency=[]
term=[]
vocabulary = []
key=[]
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\invindex.txt', 'rb') as handle:
  inverted_index = pickle.loads(handle.read())
with open(r"C:\Users\Mohammadreza Rahmani\Desktop\vocabu.txt", encoding="utf-8") as file_in:
    for line in file_in:
        vocabulary.append(line)
for i in range(1,len(vocabulary)):
    ss = vocabulary[i].encode('utf-8')
    ss=ss.decode('utf-8')
    if ss.endswith('\n'):
        vocabulary[i]=ss[:-(len('\n'))]
for i in range(0,len(tokens)):
    if(tokens[i]!=' '):
        if(tokens[i] in vocabulary):
            frequency.append(tokens.count(tokens[i]))
            item=tokens[i]
            term.append(item)
            for j in range(i,len(tokens)):
                if tokens[j]==item:
                    tokens[j]=' '
for i in range(0,len(term)):
    if(term[i] in vocabulary):
        key.append(vocabulary.index(term[i]))
idf=[]
for i in range(0,len(vocabulary)):
    idf.append(math.log((55109/len(inverted_index.get(i))),10))
size={}
with open(r'C:\Users\Mohammadreza Rahmani\Desktop\doc_sizes.txt', 'rb') as handle:
  size = pickle.loads(handle.read())
q_length=0.0
for i in range(0,len(key)):
    q_length=q_length+math.pow((math.log((1+frequency[i]),10)*idf[key[i]]),2)
q_length=math.sqrt(q_length)

score={}
for i in range(0,len(key)):
    docs=inverted_index.get(key[i])
    for j in range(0,len(docs)):
        ff=(math.log((docs[j][2]+1),10)*idf[key[i]])*(math.log((frequency[i]+1),10)*idf[key[i]])
        if((score.get((docs[j][0],docs[j][1])))!=None):
            score.update({(docs[j][0],docs[j][1]):score.get((docs[j][0],docs[j][1]))+ff})
        else:
            score.update({(docs[j][0], docs[j][1]): ff})
k_list=list(score.keys())
for i in range(0,len(k_list)):
    d_length=math.sqrt(size.get(k_list[i]))
    score.update({k_list[i]:(score.get(k_list[i]))/(d_length*q_length)})
heap=list(score.values())
heapq.heapify(heap)
max_scores=heapq.nlargest(10, heap)
selected=[]
for i in range(0,len(max_scores)):
    selected.append(list(score.keys())[list(score.values()).index(max_scores[i])])
list1=[]
for i in range(0,6):
            list1.append((pd.read_csv(r'C:\Users\Mohammadreza Rahmani\Desktop\IR-S19-project-data\-'+str(i)+'.csv', usecols=['content']))
            .values.tolist())
list2=[]
for i in range(0,6):
            list2.append((pd.read_csv(r'C:\Users\Mohammadreza Rahmani\Desktop\IR-S19-project-data\-'+str(i)+'.csv', usecols=['title']))
            .values.tolist())
for i in range(0,len(selected)):
    print(list1[selected[i][0]][selected[i][1]][0])
    print(list2[selected[i][0]][selected[i][1]][0])
    print("/////////////////")


