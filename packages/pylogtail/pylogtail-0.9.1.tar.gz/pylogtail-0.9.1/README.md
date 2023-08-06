# Python logtail

Python implementation of the logtail tool for use in python projects to process log file lines that have not been read.

## Usage

```
#!/usr/bin/env python3

from logtail import logtail

log = logtail("file.log")

for line in log.readline():
    if line:
        print(line.rstrip())
```
