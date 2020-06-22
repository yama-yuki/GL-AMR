#from GL_load import slotM, slotP
import re

ASP=['begin','began','begun','beginning','start','started','starting',
     'finish','finished','finishing','end','ended','ending']
BAKE=['bake','baked','baking','cook','cooked','cooking','fry','fried','frying']

import csv
clusters = 'clusters2_both.csv'

def make_sent_list(text):
    with open(text, mode='r') as f:
        new_lines = []
        lines = f.readlines()
        for line in lines:
            l = line.rstrip('\r\n')
            new_lines.append(l)
        return new_lines

with open(clusters, mode='r') as f:
    cluster = []
    reader = csv.reader(f)
    for row in reader:
        cluster.append(row)

    print('**********DONE LOADING CLUSTERS**********')
    slotM = cluster[1]
    slotP = cluster[0]

def make_list(lines,n):
    sents = []
    sent = []
    for line in lines:
        if line.strip():
            line = line.rstrip('\n')
            line = line[:-1]
            new_line = re.split('\(|,\s', line)
            if n>0:
                word_tag = new_line[n]
                word = word_tag.split('-')[0]
            else:
                word = new_line[n]
            sent.append(word)
        else:
            sents.append(sent)
            sent = []
    if sent:
        sents.append(sent)
    return sents

def detection(depfile):
    with open(depfile, 'r') as f:
        lines = f.readlines()
        GO = []
        objects = []
        GL_obj = []

        label = make_list(lines,0)
        gov = make_list(lines,1)
        sents = make_list(lines,2)

        s=0
        for sent in sents:
            #type coercion
            gov_index=[]
            asp_verb = 'None'
            det = 'None'
            obj = 'None'
            for word in enumerate(sent):
                if word[1].lower() in ASP:
                    asp_verb = word[1]
            if asp_verb != 'None':
                for word in enumerate(gov[s]):
                    if word[1].lower() == asp_verb:
                        gov_index.append(word[0])
                if gov_index:
                    for i in gov_index:
                        if label[s][i] == 'dobj':
                            obj = sents[s][i]
                            det = 'TC'

            ###########
            #co-composition
            gov_index=[]
            bake_verb = 'None'
            if det == 'None':
                for word in enumerate(sent):
                    if word[1].lower() in BAKE:
                        bake_verb = word[1]
                if bake_verb != 'None':
                    for word in enumerate(gov[s]):
                        if word[1].lower() == bake_verb:
                            gov_index.append(word[0])
                    if gov_index:
                        for i in gov_index:
                            if label[s][i] == 'dobj':
                                obj = sents[s][i]
                                if obj in slotP:
                                    det = 'CC'
                                else: obj = 'None'

            objects.append(obj)
            GO.append(det)
            pair = []
            pair.append(det)
            pair.append(obj)
            GL_obj.append(pair)
            s+=1

    return GL_obj

'''
if __name__ == '__main__':
    depfile = 'dep'
    print(detection(depfile))
'''
