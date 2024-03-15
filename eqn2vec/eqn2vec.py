#!/usr/bin/env python3
import os
import subprocess


def check_environment():
    """
    The following packages are required:
    - pdflatex
    - pdfseparate
    - pdf2svg
    """

    # Check for pdflatex
    try:
        subprocess.run(["pdflatex", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("pdflatex not found. Please install TeX Live or MiKTeX.")
        return False

    # Check for pdfseparate
    try:
        subprocess.run(["pdfseparate", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("pdfseparate not found. Please install poppler-utils.")
        return False

    # Check for pdf2svg
    try:
        subprocess.run(["pdf2svg", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("pdf2svg not found. Please install pdf2svg.")
        return False

    return True


def create_latex_file(equations, filename="equations.tex"):
    """
    Creates a LaTeX file with each equation on a separate page.
    """

    # equation must be a list
    if not isinstance(equations, list):
        equations = list(equations)

    with open(filename, "w") as file:
        # Write the LaTeX document header
        file.write("\\documentclass[multi=page, border=1pt]{standalone}\n")
        file.write("\\usepackage{amsmath}\n")
        file.write("\\begin{document}\n")

        # Add each equation in a separate 'page' environment
        for i, eq in enumerate(equations):

            print(f'Equation {i}: {eq}')

            file.write("\\begin{page}\n")
            file.write(f"${eq}$\n")
            file.write("\\end{page}\n")

        # Close the document
        file.write("\\end{document}\n")

    return filename


def compile_latex_to_pdf(latex_file, output_pdf="equations.pdf"):
    """
    Compiles a LaTeX file into a PDF.
    """

    cmd = ["pdflatex", "-interaction=nonstopmode", latex_file]

    print(f"Compiling {latex_file} to {output_pdf}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return output_pdf


def split_pdf_to_svgs(pdf_file, equations, output_prefix="eqn"):
    """
    Splits a PDF into separate PDFs for each page and converts them to SVG files.
    """
    # Split the PDF into separate pages
    print(f"Splitting {pdf_file} into separate pages")
    subprocess.run(["pdfseparate", pdf_file, f"{output_prefix}%d.pdf"], check=True)

    pdf_file_list = [f"{output_prefix}{i}.pdf" for i in range(1, 1 + len(equations))]

    # Convert each split PDF to SVG
    for i, pdf in enumerate(pdf_file_list):
        svg_file = pdf.replace(".pdf", ".svg")

        print(f"Creating {svg_file}")

        subprocess.run(["pdf2svg", pdf, svg_file], check=True)


def main():
    eq_list = []
    eq_list.append("U(\\mathbf{X} ; \\boldsymbol{\\Theta})")

    # Add more equations as needed
    # eq_list.append("E = mc^2")

    latex_file = create_latex_file(eq_list)
    compiled_pdf = compile_latex_to_pdf(latex_file)
    split_pdf_to_svgs(compiled_pdf, eq_list)


if __name__ == "__main__":
    main()