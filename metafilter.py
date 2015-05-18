# metafilter.py

# Functions that process metadata for parallel_crossvalidate.py

import csv, random

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    dirtyname = prefix + "." + postfix
    return dirtyname

def forceint(astring):
    try:
        intval = int(astring)
    except:
        intval = 0

    return intval

def get_metadata(classpath, volumeIDs, excludeif, excludeifnot, excludebelow, excludeabove):
    '''
    As the name would imply, this gets metadata matching a given set of volume
    IDs. It returns a dictionary containing only those volumes that were present
    both in metadata and in the data folder.

    It also accepts four dictionaries containing criteria that will exclude volumes
    from the modeling process.
    '''
    print(classpath)
    metadict = dict()

    with open(classpath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)

        anonctr = 0

        for row in reader:
            volid = dirty_pairtree(row['docid'])
            theclass = row['recept'].strip()

            # I've put 'remove' in the reception column for certain
            # things that are anomalous.
            if theclass == 'remove':
                continue

            bail = False
            for key, value in excludeif.items():
                if row[key] == value:
                    bail = True
            for key, value in excludeifnot.items():
                if row[key] != value:
                    bail = True
            for key, value in excludebelow.items():
                if forceint(row[key]) < value:
                    bail = True
            for key, value in excludeabove.items():
                if forceint(row[key]) > value:
                    bail = True

            if bail:
                continue

            birthdate = forceint(row['birth'])

            pubdate = forceint(row['inferreddate'])

            gender = row['gender'].rstrip()
            nation = row['nationality'].rstrip()

            #if pubdate >= 1880:
                #continue

            if nation == 'ca':
                nation = 'us'
            elif nation == 'ir':
                nation = 'uk'
            # I hope none of my Canadian or Irish friends notice this.

            notes = row['notes'].lower()
            author = row['author']
            if len(author) < 1 or author == '<blank>':
                author = "anonymous" + str(anonctr)
                anonctr += 1

            title = row['title']
            canon = row['canon']

            # I'm creating two distinct columns to indicate kinds of
            # literary distinction. The reviewed column is based purely
            # on the question of whether this work was in fact in our
            # sample of contemporaneous reviews. The obscure column incorporates
            # information from post-hoc biographies, which trumps
            # the question of reviewing when they conflict.

            if theclass == 'random':
                obscure = 'obscure'
                reviewed = 'not'
            elif theclass == 'reviewed':
                obscure = 'known'
                reviewed = 'rev'
            elif theclass == 'addcanon':
                obscure = 'known'
                reviewed = 'addedbecausecanon'
            else:
                print("Missing class" + theclass)

            if notes == 'well-known':
                obscure = 'known'
            if notes == 'obscure':
                obscure = 'obscure'

            if canon == 'y':
                if theclass == 'addcanon':
                    actually = 'Norton, added'
                else:
                    actually = 'Norton, in-set'
            elif reviewed == 'rev':
                actually = 'reviewed'
            else:
                actually = 'random'

            metadict[volid] = dict()
            metadict[volid]['reviewed'] = reviewed
            metadict[volid]['obscure'] = obscure
            metadict[volid]['pubdate'] = pubdate
            metadict[volid]['birthdate'] = birthdate
            metadict[volid]['gender'] = gender
            metadict[volid]['nation'] = nation
            metadict[volid]['author'] = author
            metadict[volid]['title'] = title
            metadict[volid]['canonicity'] = actually
            metadict[volid]['pubname'] = row['pubname']
            metadict[volid]['firstpub'] = forceint(row['firstpub'])

    # These come in as dirty pairtree; we need to make them clean.

    cleanmetadict = dict()
    allidsinmeta = set([x for x in metadict.keys()])
    allidsindir = set([dirty_pairtree(x) for x in volumeIDs])
    missinginmeta = len(allidsindir - allidsinmeta)
    missingindir = len(allidsinmeta - allidsindir)
    print("We have " + str(missinginmeta) + " volumes in missing in metadata, and")
    print(str(missingindir) + " volumes missing in the directory.")
    print(allidsinmeta - allidsindir)

    for anid in volumeIDs:
        dirtyid = dirty_pairtree(anid)
        if dirtyid in metadict:
            cleanmetadict[anid] = metadict[dirtyid]

    return cleanmetadict

def sort_by_proximity(idlist, dictionary, target):
    proximities = list()
    random.shuffle(idlist)

    for anid in idlist:
        date = dictionary[anid]['pubdate']
        proximities.append(abs(target - date))

    decorated = list(zip(proximities, idlist))
    decorated.sort()

    sortedlist = [x[1] for x in decorated]
    return sortedlist

def label_classes(metadict, category2sorton, positive_class, sizecap):
    ''' This takes as input the metadata dictionary generated
    by get_metadata. It subsets that dictionary into a
    positive class and a negative class. Instances that belong
    to neither class get ignored.
    '''

    all_instances = set([x for x in metadict.keys()])

    # The first stage is to find positive instances.

    all_positives = set()

    for key, value in metadict.items():
        if value[category2sorton] == positive_class:
            all_positives.add(key)

    all_negatives = all_instances - all_positives
    iterator = list(all_negatives)
    for item in iterator:
        if metadict[item]['reviewed'] == 'addedbecausecanon':
            all_negatives.remove(item)

    if sizecap > 0 and len(all_positives) > sizecap:
        positives = random.sample(all_positives, sizecap)
    else:
        positives = list(all_positives)
        print(len(all_positives))

    # If there's a sizecap we also want to ensure classes have
    # matching sizes and roughly equal distributions over time.

    numpositives = len(all_positives)

    if sizecap > 0 and len(all_negatives) > numpositives:
        if not 'date' in category2sorton:
            available_negatives = list(all_negatives)
            negatives = list()

            for anid in positives:
                date = metadict[anid]['pubdate']

                available_negatives = sort_by_proximity(available_negatives, metadict, date)
                selected_id = available_negatives.pop(0)
                negatives.append(selected_id)

        else:
            # if we're dividing classes by date, we obvs don't want to
            # ensure equal distributions over time.

            negatives = random.sample(all_negatives, sizecap)

    else:
        negatives = list(all_negatives)

    # Now we have two lists of ids.

    IDsToUse = set()
    classdictionary = dict()

    print()
    print("We have " + str(len(positives)) + " positive, and")
    print(str(len(negatives)) + " negative instances.")

    for anid in positives:
        IDsToUse.add(anid)
        classdictionary[anid] = 1

    for anid in negatives:
        IDsToUse.add(anid)
        classdictionary[anid] = 0

    for key, value in metadict.items():
        if value['reviewed'] == 'addedbecausecanon':
            IDsToUse.add(key)
            classdictionary[key] = 0
    # We add the canon supplement, but don't train on it.

    return IDsToUse, classdictionary














