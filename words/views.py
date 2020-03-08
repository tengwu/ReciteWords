from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import time
import _thread
from words.models import WordJson

# Create your views here.
from django.http import HttpResponse

def getWord(_word, fdlog):
    cnt = 0
    _word = _word.replace(' ', '%20').strip('\n')
    url = 'http://www.iciba.com/'
    while True: #获取失败后等待10s再次获取
        html = urlopen(url+_word)
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        # bsObj = BeautifulSoup(open('files/tmp.txt', 'r').read(), 'html.parser')
        word_dict = {}
        word_dict['spell'] = _word.replace('%20', ' ')
        baseSpeak = bsObj.select_one('div.base-speak')
        if baseSpeak is None:
            if cnt == 1: #一个单词重试1次
                break
            fdlog.write("ERROR Failed to get %s, Wait for 10s and retry...\n" % _word)
            fdlog.flush()
            time.sleep(10)
            cnt = cnt+1
            continue
        speak_span = baseSpeak.find_all('span')
        try:
            word_dict['speak_england'] = speak_span[1].text #word.speak_england
        except:
            word_dict['speak_england'] = ''
        try:
            word_dict['speak_america'] = speak_span[3].text #word.speak_america
        except:
            word_dict['speak_america'] = ''

        collins_sec = bsObj.select_one('div.collins-section')
        meaning_all = collins_sec.find_all(class_='prep-order')
        word_dict['meaning'] = []
        try:
            for meaning in meaning_all: #对每一个解释，抽取词性、中文解释、英文解释、例句
                tmp = meaning.find_all(class_='family-english') #词性和英文解释
                tmp_meaning = {}
                tmp_meaning['property'] = tmp[0].text
                tmp_meaning['english'] = tmp[1].text
                tmp_meaning['chinese'] = meaning.select_one('span.family-chinese').text
                tmp_meaning['example'] = []
                tmp_example = {}
                example_all = meaning.find_all(class_="text-sentence")
                for example in example_all:
                    tmp_example['english'] = example.select_one('p.family-english').text.lstrip().rstrip()
                    tmp_example['chinese'] = example.select_one('p.family-chinese').text.lstrip().rstrip()
                    tmp_meaning['example'].append(tmp_example)
                word_dict['meaning'].append(tmp_meaning)
        except Exception as e:
            if cnt == 1: #一个单词重试1次
                break
            fdlog.write("ERROR Failed to get %s when get meaning, exception info: %s, Wait for 10s and retry...\n" % (_word, repr(e)))
            fdlog.flush()
            time.sleep(10)
            cnt = cnt+1
            continue

        wordJson = WordJson()
        wordJson.spell = _word
        wordJson.json = json.dumps(word_dict)
        wordJson.save()

        fdlog.write('INFO Successful to get %s.\n' % _word)
        fdlog.flush()
        break

def index(request):
    return HttpResponse("hello, you're at the words index.")

def threadGetWords():
    fdlog = open('files/log.txt', 'w')
    for word in open('files/wordlist.txt', 'r'):
        getWord(word, fdlog)
    fdlog.close()

def getWords(request):
    _thread.start_new_thread(threadGetWords, ())
    return HttpResponse("Create a thread to get words, please go to files/log.txt for more information.")