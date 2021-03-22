.PHONY : clean

TEX_FILES  := $(shell find . -maxdepth 1 -iname '*.tex' | xargs -L1 -I{} basename "{}" .tex)
PDFLATEX    = pdflatex -interaction=nonstopmode -halt-on-error
PDF_FILES   = $(foreach d, ${TEX_FILES}, ${d}.pdf)
TMP_SUFFS   = .aux .bbl .blg .log .dvi .ps .eps .out .ent Notes.bib
RM_TMP      = \
$(foreach d, ${TEX_FILES}, rm -rf $(foreach suff, ${TMP_SUFFS}, ${d}${suff})) msNotes.bib
CHECK_RERUN = grep Rerun ms.log
TECTONIC    = $(shell command -v tectonic >/dev/null && echo true || echo false )
BUILD_LATEX = \
if [ "${TECTONIC}" = "true" ]; then\
	tectonic $^ --keep-intermediates --keep-logs;\
else\
	${PDFLATEX} $^;\
	( ${CHECK_RERUN} && ${PDFLATEX} $^ ) || echo "Done.";\
	( ${CHECK_RERUN} && ${PDFLATEX} $^ ) || echo "Done.";\
	( ${CHECK_RERUN} && ${PDFLATEX} $^ ) || echo "Done.";\
fi

default: ${PDF_FILES}

%.pdf: %.tex
	@qed-setup
	@${BUILD_LATEX}
	@qed
	@${BUILD_LATEX}
	@${RM_TMP}
	@qed-clean
	@touch $^

clean:
	@rm -f ${PDF_FILES}
	@${RM_TMP}
	@qed-clean
