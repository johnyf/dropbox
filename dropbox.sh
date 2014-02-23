# clear junctions, then start dropbox
# 2012.05.08 -2013.08.29
# Ioannis Filippidis, jfilippidis@gmail.com

# clear shortcuts
cd /Users/ifilippi/Dropbox
junctions.py -d
find -f ./* -type l

# start dropbox
open -a Dropbox
