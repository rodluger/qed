.PHONY : clean, default

QED         = qed ms.tex
PDFLATEX    = pdflatex -interaction=nonstopmode -halt-on-error
TEX_FILES   = ms
QED_FILES   = .qed/*
TMP_SUFFS   = .pdf .aux .bbl .blg .log .dvi .ps .eps .out .ent Notes.bib
RM_TMP      = \
$(foreach d, ${TEX_FILES}, rm -rf $(foreach suff, ${TMP_SUFFS}, ${d}${suff})) \
msNotes.bib ${QED_FILES}
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
	@mkdir -p .qed
	@${BUILD_LATEX}
	@${QED}
	@${BUILD_LATEX}
	@rm .qed/*.icon

ms.pdf: ms.tex

clean:
	@$(RM_TMP)
