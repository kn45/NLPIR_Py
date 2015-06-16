#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
# for cluster job
sys.path.append('./')
# for stand-alone job
# append the path of nlpir_py containing __init__.py
sys.path.append('/data0/result/chenting5/segmentation/NLPIR/')
import nlpir_py as nlpir

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

usr_dic_dir = '/data0/result/chenting5/segmentation/NLPIR/'

if __name__ == "__main__":
	if len(sys.argv) < 2 or sys.argv[1] not in ['s', 'c']:
		print "arg should be s(tandalone), or c(cluster)"
		sys.exit()
	seg_mod = sys.argv[1]
	if seg_mod == 's':
		load_usr_dic(usr_dic_dir + 'usr_dict')
	if seg_mod == 'c':
		load_usr_dic('usr_dict')
	#load_usr_dic('usr_dict_test')
	for line in sys.stdin:
		[label, content] = line.strip('\n').split('\t')
		uni = ' '.join([t[0] for t in nlpir.Seg(content) if valid_word(t) == True])
		print label + '\t' + uni
