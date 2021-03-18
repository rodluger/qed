import sys
import os
import subprocess
import shutil
import glob

try:
    from pdf2image import convert_from_path
except ModuleNotFoundError as e:

    def delayed_import_error(*args):
        raise e

    convert_from_path = delayed_import_error

INDEX_TEMPLATE = """
Examples
========

.. toctree::
   :titlesonly:
   :maxdepth: 1

   {index}
"""

IMAGE_TEMPLATE = """
.. image:: {png}
    :class: pdf-preview
"""

EXAMPLE_TEMPLATE = """
{title}
===============================================================================

Generated pdf
-------------

Click :download:`here <{pdf}>` to download the PDF.

{images}

LaTeX source
------------

Click :download:`here <{texfile}>` to download the TEX file.

.. literalinclude:: {texfile}
   :language: latex
   :lines: 2-
"""


def run_examples():

    # Current path
    HERE = os.path.dirname(os.path.abspath(__file__))

    # Copy the examples over here
    try:
        shutil.rmtree(os.path.join(HERE, "examples"))
    except OSError:
        pass
    shutil.copytree(
        os.path.join(HERE, "..", "examples"), os.path.join(HERE, "examples")
    )

    # Run the makefile for the examples
    subprocess.check_output(
        ["make", "clean"], cwd=os.path.join(HERE, "examples")
    )
    subprocess.check_output(["make"], cwd=os.path.join(HERE, "examples"))

    # Process each example
    index = []
    for file in glob.glob(os.path.join(HERE, "examples", "*.tex")):

        # File names
        texfile = os.path.basename(file)
        rstfile = os.path.join("examples", texfile.replace(".tex", ".rst"))
        pdffile = rstfile.replace(".rst", ".pdf")
        pngfile = rstfile.replace(".rst", "{}.png")

        # Get example title
        with open(file, "r") as f:
            title = f.readline()
            assert title.startswith("%"), "Example doesn't have a title!"
            title = title[1:-1].strip()

        # Append to the index of examples
        index.append(texfile.replace(".tex", ""))

        # Convert PDF to jpeg
        images = convert_from_path(pdffile)
        for i, image in enumerate(images):
            image.save(pngfile.format(i))
        images = "\n\n".join(
            [
                IMAGE_TEMPLATE.format(png=os.path.basename(pngfile.format(i)))
                for i in range(len(images))
            ]
        )

        # Create rst file
        with open(rstfile, "w") as f:
            print(
                EXAMPLE_TEMPLATE.format(
                    title=title,
                    texfile=texfile,
                    images=images,
                    pdf=os.path.basename(pdffile),
                ),
                file=f,
            )

    # Add index to `examples.rst`
    with open(os.path.join(HERE, "examples", "examples.rst"), "w") as f:
        print(INDEX_TEMPLATE.format(index=r"\n   ".join(index)), file=f)


if __name__ == "__main__":
    run_examples()
