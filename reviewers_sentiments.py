import csv
import SonicScrewdriver as utils

predict = dict()
judge = dict()

with open('logisticpredictions.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['reviewed'] == 'not':
            continue
        else:
            predict[row['volid']] = row['logistic']

with open('masterpoemeta.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        htid = utils.clean_pairtree(row['docid'])
        if row['impaud'] == 'pop':
            row['judge'] = 'neg'
        judge[htid] = row['judge']

pos = list()
neg = list()
other = list()

for key, value in predict.items():
    if key not in judge:
        print(key)
        continue
    else:
        if judge[key] == 'pos':
            pos.append(float(value))
        elif judge[key] == 'neg':
            neg.append(float(value))
        else:
            other.append(float(value))






