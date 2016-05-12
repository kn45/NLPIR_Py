#!/usr/bin/env python2.6
# -*- coding=utf-8 -*-

import sys
# for cluster job
sys.path.append('./')
# for stand-alone job
sys.path.append('/data0/result/chenting5/segmentation/NLPIR/')
import nlpirpy as nlpir

def valid_word(atom):
    pos = atom[1]
    if pos[0] == 'u':  # url because of expired link
        return False
    if pos[0] == 'm':  # number
        return False
    if pos[0] == 'w':  # punctuation
        return False
    if pos[0] == 't':  # time date
        return False
    try:
        if len(atom[0].decode('utf-8')) <= 1:
            return False
    except:
            return False
    return True

def load_usr_dic(dic_dir):
    for line in open(dic_dir, 'r'):
        nlpir.AddUserWord(line.strip())

seg_dir = './'

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ['s', 'c']:
        print "arg should be s(tandalone), or c(luster)"
        sys.exit()
    seg_mod = sys.argv[1]
    if seg_mod == 's':
        load_usr_dic(seg_dir + 'usr_dict')
    if seg_mod == 'c':
        load_usr_dic('usr_dict')

    if sys.stdin.isatty():
        content = '大哥请你从stdin输入一句话啊!'
        uni = ' '.join([t[0] for t in nlpir.Seg(content) if valid_word(t) == True])
        print uni
    else:
        for line in sys.stdin:
            content = line.strip('\n')
            if content == '':
                content = '大哥请你从stdin输入一句话啊!'
            uni = ' '.join([t[0] for t in nlpir.Seg(content) if valid_word(t) == True])
            print uni
