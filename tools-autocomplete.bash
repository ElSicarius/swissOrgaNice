complete  -W "`tools | awk '{print $1}' | cut -d '|' -f 1 | tr '\n' ' '`" swissOrgaNice.py
