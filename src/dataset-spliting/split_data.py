import random as rd

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gera arquivo de anotacoes para YOLOv3 do dataset dividido')
    parser.add_argument('--dataset', type=str, dest='dataset', default='full_base.txt', help='Path para arquivo de anotacoes')
    parser.add_argument('--train', type=int, dest='perc_train', default=60, help='Percentual de treinamento')
    parser.add_argument('--val', type=int, dest='perc_val', default=20, help='Percentual de validacao')
    parser.add_argument('--test', type=int, dest='perc_test', default=20, help='Percentual de teste')
    
    args = parser.parse_args()

	
	read_f = open(args.dataset, "r").read()
	list_data = read_f.split('\n')
	size = len(list_data)

	rd.shuffle(list_data)

	percent_train = args.perc_train
	trainobjs = ""

	percent_val = args.perc_val
	valobjs = ""

	percent_test = args.perc_test
	testobjs = ""

	assert (percent_train + percent_val + percent_test) == 100

	idx = 0
	for item in list_data:
		#print(item)
		per = float((idx * 100) / size)
		print(("%0.2f%%") % (per))
		idx += 1
		
		if per < percent_train:
			trainobjs = trainobjs + item + '\n'
		elif per >= percent_train and per < (percent_train + percent_val):
			valobjs = valobjs + item + '\n'
		elif per >= (percent_train + percent_val):
			testobjs = testobjs + item + '\n'
		
		
	with open("train.txt", "w") as text_file:
		text_file.write(trainobjs)

	with open("val.txt", "w") as text_file:
		text_file.write(valobjs)
		
	with open("test.txt", "w") as text_file:
		text_file.write(testobjs)
