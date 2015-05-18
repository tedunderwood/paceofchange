paceofchange
============

Code, data, and metadata to support replication of the results in "How quickly do literary standards change?"

If you have Python 3 with numpy, pandas and scikit-learn, you should be able to clone this repo and then run replicate.py. Different forms of analysis can be provided to replicate.py as command-line arguments. For instance,

> python3 replicate.py full

Replicates the main model represented in Figure 1 of the article. Other options include *quarters*, *halves*, *canon,* *genders*, and *nations.*

The standards we are trying to meet are pithily summarized by Jason Baldridge in ["It's okay for academic software to suck."](https://bcomposes.wordpress.com/2015/05/07/its-okay-for-academic-software-to-suck/) We want our results to be reliable, so we've worked hard to ensure that the models produced by this code are cross-validated appropriately. We want the enclosed data and metadata to be reliable -- which means, on this scale, a low level of evenly-distributed error. So we've documented our procedures and shared metadata in ["Understanding Genre in a Collection of a Million Volumes."](http://figshare.com/articles/Understanding_Genre_in_a_Collection_of_a_Million_Volumes_Interim_Report/1281251)

But this is not a project that promised to build portable tools, and you won't find any in this repo. Our view is that the really portable tools are already encapsulated in scikit-learn.

code
----

The important modules are

**replicate.py**
**parallel_crossvalidate.py**
**metafilter.py**
**modelingprocess.py**

**Replicate.py** translates a command-line option (like *halves*) into a set of parameters which it passes to **parallel_crossvalidate.py.** This module loads data, calls **metafilter** to load metadata, and figures out which volumes have to be excluded from each crossvalidation pass. Then it starts a multiprocessing pool, which calls **modelingprocess* to create each model in a leave-one-out crossvalidation scheme.

The most fragile part of this is probably the multiprocessing. The code could be rewritten to be single-threaded.

