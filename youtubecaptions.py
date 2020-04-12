# Irwin Qi Dec 2019, version 4
from pytube import YouTube
import nltk
import re, string
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt 
from matplotlib.colors import LinearSegmentedColormap

#import stop words from NLTK 
stop_words = set(stopwords.words('english'))

#video source
askforinput = input("Please provide a link of your YouTube video:  ")
source = YouTube(askforinput)


en_caption = source.captions.get_by_language_code('en')
srt =(en_caption.generate_srt_captions())

text = ''
removelist = ['-->', '</font>', '<font>', '<font color="#CCCCCC">', '<font color="#E5E5E5">', '<font color="#EEE">', ':','']
removecompile = re.compile(r"\b(" + "|".join(removelist) + ")\\W", re.I)

def Removesub(text):
    global removecompile
    return removecompile.sub(" ", text)

for line in srt:
    if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None and re.search('^-->', line) is None:
        text += '' + line.rstrip('\n')
        text = text.lstrip()
        #text = text.replace('-->','')
        #text = text.replace('</font>','')
        #text = text.replace('<font>','')
        #text = text.replace('<font color="#CCCCCC">','')
        #text = text.replace('<font color="#E5E5E5">','')
        #text = text.replace('<font color="#EEE">','')
        #text = text.replace(':','')
        text = Removesub(text)
for c in string.punctuation:
    text = text.replace(c,"")
    
#print(text)

tokens = [t for t in text.split()]
clean_tokens = tokens[:]
for token in tokens:
    if token in stop_words: 
        clean_tokens.remove(token)
freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items(): 
    print (str(key) + ':' + str(val))

colors = ["#f44336","#E91E63","#9C27B0","#673AB7","#3F51B5","#2196F3","#03A9F4","#00BCD4","#009688","#4CAF50","#8BC34A","#CDDC39","#FFEB3B","#FFC107","#FF9800","#FF5722","#795548","#FFB900","#E81123","#0063B1","#0099BC","#00CC6A","#107C10","#847545","#D13438","#00B7C3","#00CC6A","#ff5700","#b92b27","#1ab7ea","#55acee","#0084ff","#0077B5","#25D366","#ea4c89","#00c300","#FFFC00","#0084ff"]
cmap = LinearSegmentedColormap.from_list("mycmap", colors)
wordcloud = WordCloud(width=1600, height=1000, max_font_size=800, max_words=100, background_color="white", font_path='/Users/wqi3/Library/Fonts/Montserrat-Regular.otf', colormap=cmap).generate(text)
plt.figure( figsize=(20,10) )
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
