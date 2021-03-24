import os

# Temporary files
QEDFUNCTIONFILE = os.path.join(".qed", "functions.qed")
QEDSYMBOLFILE = os.path.join(".qed", "symbols.qed")
QEDQEDICONFILES = os.path.join(".qed", "qed", "{qedCounter}.icon")
QEDQEDTEXFILES = os.path.join(".qed", "qed", "{qedCounter}.tex")
QEDQEDOPTFILES = os.path.join(".qed", "qed", "{qedCounter}.json")
QEDFILES = [
    QEDFUNCTIONFILE,
    QEDSYMBOLFILE,
    QEDQEDICONFILES,
    QEDQEDTEXFILES,
    QEDQEDOPTFILES,
]
QEDDIRS = [".qed", os.path.join(".qed", "qed")]

# Function argument separators
QEDSEPARATORS = ["|", ",", ";"]

# Built-in defs
QEDBUILTINS = {r"\dd": "d", r"\equiv*": "="}

# Console web address
QEDWEBSITE = "https://luger.dev/qed"

# TODO: Remove in production
if bool(int(os.getenv("QEDDEBUG", 0))):
    QEDWEBSITE = "file:///Users/rluger/src/qed/index.html"

# Status badge codes
QEDPASS = 0
QEDFAIL = 1
QEDERROR = 2
QEDINDET = 3
QEDNA = 4

# Logging messages
QEDMSGANATRUE = 0
QEDMSGANAFALSE = 1
QEDMSGINDET = 2
QEDMSGNUMFALSE = 3
QEDMSGNUMTRUE = 4
QEDMSGNOTIMP = 5
QEDMSGDEF = 6
QEDMSGNUMDIS = 7
QEDMSGANADIS = 8
QEDMSGNONEED = 9
