# My goal in this script is to package up the modeling and
# evaluation processes we actually ran to produce the article,
# so they can be replicated without a lot of fuss.

import parallel_crossvalidate as pc
import sys

allowable = {"full", "quarters", "nations", "genders", "canon", "halves"}

def instructions():
    print("Your options are: ")
    print()
    print("full -- model the full 700-volume dataset using default settings")
    print("quarters -- create four quarter-century models")
    print("nations -- distinguish American and British poets")
    print()

args = sys.argv
if len(args) > 1:
    command = args[1]
    if command not in allowable:
        instructions()
        sys.exit(0)

else:
    instructions()
    command = ""
    while command not in allowable:
        command = input('Which option do you want to run? ')

assert command in allowable

if command == 'full':

    ## PATHS.

    sourcefolder = 'poems/'
    extension = '.poe.tsv'
    classpath = 'poemeta.csv'
    outputpath = 'weirdpredictions.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950
    sizecap = 360

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1800

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

elif command == 'quarters':
    ## PATHS.

    sourcefolder = 'poems/'
    extension = '.poe.tsv'
    classpath = 'poemeta.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950

    sizecap = 360

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    quarteroptions = [('1820-44predictions.csv', 1800, 1844), ('1845-69predictions.csv', 1845, 1869), ('1870-94predictions.csv', 1870, 1894), ('1895-19predictions.csv', 1895, 1925)]

    quarterresults = list()

    for outputpath, pastthreshold, futurethreshold in quarteroptions:

        print(pastthreshold)
        paths = (sourcefolder, extension, classpath, outputpath)
        exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
        thresholds = (pastthreshold, futurethreshold)
        classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

        rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

        print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
        tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

        print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

        theseresults = dict()
        theseresults['allvolumes'] = allvolumes
        theseresults['rawaccuracy'] = rawaccuracy
        theseresults['tiltaccuracy'] = tiltaccuracy
        theseresults['coefficientuples'] = coefficientuples
        theseresults['startdate'] = pastthreshold

        quarterresults.append(theseresults)

elif command == 'nations':

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
    extension = '.poe.tsv'
    classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/finalpoemeta.csv'
    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/nationalpredictions.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950
    sizecap = 360

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1700

    # CLASSIFY CONDITIONS

    positive_class = 'uk'
    category2sorton = 'nation'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

elif command == 'genders':

    ## PATHS.

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/texts/'
    extension = '.poe.tsv'
    classpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/finalpoemeta.csv'
    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/poetry/nationalpredictions.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950
    sizecap = 360

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1700

    # CLASSIFY CONDITIONS

    positive_class = 'f'
    category2sorton = 'gender'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

if command == 'canon':

    ## PATHS.

    sourcefolder = 'poems/'
    extension = '.poe.tsv'
    classpath = 'poemeta.csv'
    outputpath = 'canonpredictions.csv'
    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    # excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1700
    excludeabove['firstpub'] = 1950
    sizecap = 450

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1800

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

if command == 'halves':

    ## PATHS.

    sourcefolder = 'poems/'
    extension = '.poe.tsv'
    classpath = 'poemeta.csv'
    outputpath = 'firsthalfpredictions.csv'

    ## EXCLUSIONS.

    excludeif = dict()
    excludeif['pubname'] = 'TEM'
    # We're not using reviews from Tait's.

    excludeif['recept'] = 'addcanon'
    # We don't ordinarily include canonical volumes that were not in either sample.
    # These are included only if we're testing the canon specifically.

    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    excludebelow['firstpub'] = 1800
    excludeabove['firstpub'] = 1875
    sizecap = 300

    # For more historically-interesting kinds of questions, we can limit the part
    # of the dataset that gets TRAINED on, while permitting the whole dataset to
    # be PREDICTED. (Note that we always exclude authors from their own training
    # set; this is in addition to that.) The variables futurethreshold and
    # pastthreshold set the chronological limits of the training set, inclusive
    # of the threshold itself.

    ## THRESHOLDS

    futurethreshold = 1925
    pastthreshold = 1800

    # CLASSIFY CONDITIONS

    positive_class = 'rev'
    category2sorton = 'reviewed'
    datetype = 'firstpub'
    numfeatures = 3200
    regularization = .00007

    paths = (sourcefolder, extension, classpath, outputpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    thresholds = (pastthreshold, futurethreshold)
    classifyconditions = (category2sorton, positive_class, datetype, numfeatures, regularization)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

    # NOW DO THE SECOND HALF.

    excludebelow['firstpub'] = 1876
    excludeabove['firstpub'] = 1925
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    outputpath = 'secondhalfpredictions.csv'
    paths = (sourcefolder, extension, classpath, outputpath)

    rawaccuracy, allvolumes, coefficientuples = pc.create_model(paths, exclusions, thresholds, classifyconditions)

    tiltaccuracy = pc.diachronic_tilt(allvolumes, 'linear', [])

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))










