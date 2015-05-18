import csv
from scipy.stats.stats import pearsonr

files = ['1820-44predictions.csv', '1845-69predictions.csv', '1870-94predictions.csv', '1895-19predictions.csv']

datelist = [(1810, 1844), (1845, 1869), (1870, 1894), (1895, 1925)]

def getfile(filename):
    vector = list()
    with open(filename, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vector.append(float(row['logistic']))
    return vector

def getfiledates(filename, dates):
    start, end = dates
    vector = list()
    with open(filename, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = int(row['pubdate'])
            if date >= start and date <= end:
                vector.append(float(row['logistic']))
    return vector

vectors = list()
for afile in files:
    vectors.append(getfile(afile))

distances = dict()
distances[1] = list()
distances[2] = list()
distances[3] = list()

for i in range(4):
    firstfile = files[i]
    for j in range(4):
        if i == j:
            continue
        else:
            dates = datelist[j]
            firstvec = getfiledates(firstfile, (1700, 1950))
            secondfile = files[j]
            secondvec = getfiledates(secondfile, (1700, 1950))
            r = pearsonr(firstvec, secondvec)[0]
            print(str(i) + " : " + str(j) + " : " + str(r))
            dist = abs(i-j)
            distances[dist].append(r)


for i in range(1,4):
    print(sum(distances[i]) / len(distances[i]))
