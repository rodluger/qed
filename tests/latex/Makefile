.PHONY : clean, default

PDFLATEX    = pdflatex -interaction=nonstopmode -halt-on-error
TEX_FILES   = ms
TMP_SUFFS   = .pdf .aux .bbl .blg .log .dvi .ps .eps .out .ent Notes.bib
RM_TMP      = \
$(foreach d, ${TEX_FILES}, rm -rf $(foreach suff, ${TMP_SUFFS}, ${d}${suff})) \
msNotes.bib
CHECK_RERUN = grep Rerun ms.log
TECTONIC    = $(shell command -v tectonic >/dev/null && echo true || echo false )
BUILD_LATEX = \
if [ "${TECTONIC}" = "true" ]; then\
	tectonic ms.tex --keep-intermediates;\
else\
	${PDFLATEX} ms.tex;\
	( ${CHECK_RERUN} && ${PDFLATEX} ms.tex ) || echo "Done.";\
	( ${CHECK_RERUN} && ${PDFLATEX} ms.tex ) || echo "Done.";\
	( ${CHECK_RERUN} && ${PDFLATEX} ms.tex ) || echo "Done.";\
fi

default: ms.pdf clean
	@qed-setup
	@${BUILD_LATEX}
	@qed
	@${BUILD_LATEX}
	@qed-clean

ms.pdf: ms.tex

clean:
	@${RM_TMP}
	@qed-clean
