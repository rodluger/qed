import os

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

QEDSEPARATORS = ["|", ",", ";"]

QEDWEBSITE = "https://luger.dev/qed"

QEDPASS = 0
QEDFAIL = 1
QEDERROR = 2
QEDINDET = 3
QEDNA = 4
