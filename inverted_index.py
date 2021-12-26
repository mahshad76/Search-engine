import re
import pandas as pd
import hazm as hz
import random
import math
from matplotlib import pyplot as plt
import numpy as np
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
def Reverse(lst):
    lst.reverse()
    return lst
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
def make_index(list):
    inverted_index={}
    result=[]
    count=0
    vocab_list={}
    term_id=0
    for i in range(0,len(list)):
        for j in range(0,len(list[i])):
            tokens=(list[i][j][0]).split()
            for k in range(0,len(tokens)):
                    if(tokens[k] not in vocab_list.keys()):
                        doc_list=[]
                        doc_list.append([i,j])
                        vocab_list.update({tokens[k]:1})
                        term_id=[*vocab_list].index(tokens[k])
                        inverted_index.update({term_id:doc_list})
                    else:
                        if([i,j] not in inverted_index.get([*vocab_list].index(tokens[k]))):
                                term_id = [*vocab_list].index(tokens[k])
                                vocab_list.update({tokens[k]:vocab_list.get(tokens[k])+1})
                                inverted_index.get(term_id).append([i,j])
                        else:
                            vocab_list.update({tokens[k]: vocab_list.get(tokens[k]) + 1})
            print(count)
            count+=1
    result.append(vocab_list)
    result.append(inverted_index)
    return result
def Rand(start, end, num):
    res = []
    j=0
    while j<num:
        rand=random.randint(start, end)
        if(rand not in res):
            res.append(rand)
            j+=1
    return res
def zipf(vocab1,str):
    vocab1= {k: v for k, v in sorted(vocab1.items(), key=lambda item: item[1])}
    keys=[*vocab1]
    k = vocab1.get(keys[len(keys)-1])
    print("zipf:")
    print(k)
    x=[]
    y1=[]
    for i in range(1, len([*vocab1])+1):
        x.append(math.log(i,10))
        y1.append(math.log(k,10)-math.log(i,10))
    plot1 = plt.figure(str)
    values = Reverse([*vocab1.values()])
    plt.plot(x,[math.log(v) for v in values],'o', color='black')
    plt.plot(x,y1)
    plt.show()
    return 0
def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b
def heap(list,str):
    total= 0
    differ= 0
    x1=[]
    y1=[]
    vocab= []
    sample_doc = []
    for i in range(0, 4):
        j_range = []
        j_range = Rand(0, len(list[i]) - 1, 4000)
        for j in j_range:
            sample_doc.append([i, j])
    for i in range(4,6):
        j_range = []
        j_range = Rand(0, len(list[i]) - 1, 2000)
        for j in j_range:
            sample_doc.append([i, j])
    for k in range(0, len(sample_doc)):
        [i, j] = sample_doc[k]
        for x in list[i][j][0].split():
            if x not in vocab:
                vocab.append(x)
        differ = len(vocab)
        total = total + len(list[i][j][0].split())
        x1.append(math.log(total,10))
        y1.append(math.log(differ,10))
    a, b = best_fit(x1, y1)
    plot1 = plt.figure(str)
    plt.plot(x1, y1, 'o', color='black')
    yfit = [a + b * xi for xi in x1]
    plt.plot(x1, yfit)
    plt.show()
    return 0
list=[]
for i in range(0,6):
            list.append((pd.read_csv(r'C:\Users\Mohammadreza Rahmani\Desktop\IR-S19-project-data\-'+str(i)+'.csv', usecols=['content']))
            .values.tolist())
stop_words= pd.read_excel (r'C:\Users\Mohammadreza Rahmani\Desktop\stop.xlsx').values.tolist()
stop_words=[inner for outer in stop_words for inner in outer]
c=0
for i in range(0,len(list)):
    for j in range(0,len(list[i])):
        ((list[i])[j])[0] = remove_tags(((list[i])[j])[0])
        for ch in ['\\', ':', '/', '*', '_', '{', '}', '[', ']', '(', ')', '>', '<', '#', '+', '-', '.', '!', '\'',
                   ';', '"', '?', '@', '$', '%', '^', '&', '~', "'", '|', '،', '=', '؛',',']:
            if (ch in ((list[i])[j])[0]):
                ((list[i])[j])[0] = ((list[i])[j])[0].replace(ch, ' ')
        ((list[i])[j])[0] = re.sub(r"[0-9]", " ", ((list[i])[j])[0])
        for word in ['raquo', 'laquo', 'lt', 'gt', 'bull', 'hearts', 'diams', 'clubs', 'spades', 'mdash', 'nbsp']:
            if (word in ((list[i])[j])[0]):
                ((list[i])[j])[0] = ((list[i])[j])[0].replace(word, ' ')
        for ch in ['۰', '٠', '۱', '١', '۲', '٢', '۳', '٣', '۴', '٤', '۵', '٥', '۶', '٦', '۷', '٧', '۸', '٨', '۹', '٩']:
            if ch in ((list[i])[j])[0]:
                ((list[i])[j])[0] = ((list[i])[j])[0].replace(ch, ' ')
        li = ((list[i])[j])[0].split()
        li = [word for word in li if word not in stop_words]
        ((list[i])[j])[0] = ' '.join(li)
        print(c)
        c+=1
heap(list,"heap1")
result=make_index(list)
vocab1=result[0]
print('vocab1:')
print(vocab1)
invindex1=result[1]
print('inv1:')
print(invindex1)
zipf(vocab1,"zipf1")
signs=['Ø', '±', 'Ù', '†', '§', '…', '‡', '¬', 'Û', 'Œ', 'Ú', '©', '´', '¾', '„', 'ª', '\xad', 'µ', '¯', 'Ø³', 'Ø¹', 'ˆ', '®', 'Ø²', 'Ø°', 'º', 'â', '€', 'Ž']
c=0
for i in range(0,len(list)):
    for j in range(0,len(list[i])):
        list[i][j][0]=normalizeArabic(deNoise(list[i][j][0]))
        list[i][j][0]=add_space_between_emojies(list[i][j][0])
        for ch in signs:
            if (ch in list[i][j][0]):
                list[i][j][0]=list[i][j][0].replace(ch,' '+ch+' ')
        list[i][j][0]=tokenize(list[i][j][0])
        res=[]
        stemmer = hz.Stemmer()
        lemmatizer = hz.Lemmatizer()
        for word in list[i][j][0].split():
            limit = lemmatizer.lemmatize(stemmer.stem(word))
            if ('#' in limit):
                limit = limit.split('#')
                res.append(limit[0])
            else:
                res.append(limit)
        list[i][j][0] = ' '.join(res)
    print(c)
    c+=1
heap(list,"heap2")
result=make_index(list)
vocab2=result[0]
print('vovab2')
print(vocab2)
invindex2=result[1]
print('inv2')
print(invindex2)
zipf(vocab2,"zipf2")
