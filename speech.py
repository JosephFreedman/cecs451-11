import os
import speech_recognition as sr
import distance
import string
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

class speech:
    
    def __init__(self):
        self.original = []
        self.recognized = []
        self.distances = []
    def read_original(self, file):
        path = os.getcwd() + file

        with open(path, 'r') as f:
            for line in f:
                line = str(line.encode('utf8'))
                self.original.append(line[2:len(line) - 1].replace(r'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', '-')
                .replace(r'\xc3\xa2\xe2\x82\xac\xe2\x84\xa2', "'").replace(r'\n', '').replace(',', '').replace('.', '').replace('-',' ').rstrip())

        

    def conv_audio(self, file):

        r = sr.Recognizer()

        root = os.getcwd() + '/audio'
        sub_roots = os.listdir(root)
        print(root)
        print(sub_roots)
        for i in range(len(sub_roots)):

            files = os.listdir(root + '/' + sub_roots[i])
            group = []
            to_txt = ''
            for j in range(len(files)):
                if not os.path.isfile(os.getcwd() +'/text/' + sub_roots[i] + '.txt'):
                    file = sr.AudioFile(root + '/' + sub_roots[i] + '/' + files[j])
                    
                    with file as source:
                        audio = r.record(source)
                        group.append(r.recognize_google(audio).replace('-', ' ') + '\n')
                        to_txt += r.recognize_google(audio).replace('-', ' ') + '\n'
            # If text conversion doesn't exist, generate one
            if not os.path.isfile(os.getcwd() +'/text/' + sub_roots[i] + '.txt'):
                with open(os.getcwd() + '/text/' + sub_roots[i] + '.txt', 'w+') as txt:
                    txt.write(to_txt)

            with open(os.getcwd() + '/text/' + sub_roots[i] + '.txt', 'r') as txt:
                self.recognized.append([])
                for line in txt:
                    self.recognized[i].append(line.replace('-', ' '))


    def get_original(self):
        return self.original

    def get_recognized(self, i = None):
        if i == None:
            return self.recognized
        else:
            for txt in self.recognized:
                return txt

    def comp_str(self):
        orignial_words = []
        recognized_words = []
        for str in self.original:
            orignial_words.append(str.lower().strip(string.punctuation).split())
        for i in range(len(self.recognized)):
            recognized_words.append([])
            for str in self.recognized[i]:
                recognized_words[i].append(str.lower().strip(string.punctuation).split())

        for sentence in range(len(orignial_words)): 
            dist = []
            for group in range(len(recognized_words)):
                dist.append(distance.levenshtein(orignial_words[sentence], recognized_words[group][sentence]) / max(len(orignial_words[sentence]), len(recognized_words[group][sentence])))
            self.distances.append(dist)


    def plot(self):
        plot_data = []
        data = {'sentences': [], 'nld': []}
        xlabel = []
        ylabel = []
        for x in range(len(self.distances)):
            sent = 'sent' + str(x + 1)
            for val in self.distances[x]:
                xlabel.append(sent)
                ylabel.append(val)
        data['sentences'] = xlabel
        data['nld'] = ylabel
        
        for i in self.distances:
            for j in i:
                print('%.2f' % j, end=' ')
            print()

        df = pd.DataFrame(data)
        ax = sns.boxplot(x="sentences", y="nld", data=df)
        plt.show()

if __name__ == '__main__':
    # Custom methods
    s = speech()
    s.read_original('/How Speech Recognition Works.txt')
    s.conv_audio('/How Speech Recognition Works.txt')
    s.comp_str()
    s.plot()