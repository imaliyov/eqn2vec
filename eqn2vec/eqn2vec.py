#!/usr/bin/env python3
import os
import subprocess
from latex import build_pdf
import argparse
import time


def check_environment(latex_compiler="pdflatex"):
    """
    The following packages are required:
    - pdflatex
    - pdfseparate
    - pdf2svg
    """

    # Check for pdflatex
    if latex_compiler == 'pdflatex':
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


def create_latex_file(equations, style='display', filename="equations.tex"):
    """
    Creates a LaTeX file with each equation on a separate page.
    """

    with open(filename, "w") as file:
        # Write the LaTeX document header
        file.write("\\documentclass[multi=page, border=1pt]{standalone}\n")
        file.write("\\usepackage{amsmath}\n")
        file.write("\\begin{document}\n\n")

        # Add each equation in a separate 'page' environment
        for i, eq in enumerate(equations):

            print(f'Equation {i+1}: {eq}')

            file.write("\\begin{page}\n")

            if style == 'display':
                #file.write("\\begin{equation*}\n")
                #file.write(f"{eq}\n")
                #file.write("\\end{equation*}\n")

                #file.write(f"\\[\n{eq}\n\\]\n")

                file.write(f"$ \displaystyle {eq}$\n")
            elif style == 'inline':
                file.write(f"${eq}$\n")
            else:
                raise ValueError("Invalid style. Must be 'display' or 'inline'.")

            file.write("\\end{page}\n\n")

        print()
        # Close the document
        file.write("\\end{document}\n")

    return filename


def compile_latex_to_pdf_external(latex_file, output_pdf="equations.pdf"):
    """
    Compiles a LaTeX file into a PDF.
    """

    cmd = ["pdflatex", "-interaction=nonstopmode", latex_file]

    print(f"Compiling {latex_file} to {output_pdf}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return output_pdf


def compile_latex_to_pdf(latex_code, output_pdf="equations.pdf"):
    """
    Compiles LaTeX code into a PDF using the `latex` library.
    """
    pdf = build_pdf(latex_code)
    pdf.save_to(output_pdf)
    return output_pdf


def compile_latex_wrapper(latex_file, latex_compiler='latex', output_pdf="equations.pdf"):

    if latex_compiler == 'pdflatex':
        print('Compiling with pdflatex')
        compiled_pdf = compile_latex_wrapper(latex_file)
    elif latex_compiler == 'latex':

        with open(latex_file, "r") as file:
            latex_code = file.read()

        print('Compiling with Python latex')
        compiled_pdf = compile_latex_to_pdf(latex_code)

    return compiled_pdf


def split_pdf(pdf_file, equations, format='svg', output_prefix="eqn"):
    """
    Splits a PDF into separate PDFs for each page and converts them to SVG files.
    """

    if format not in ['svg', 'pdf']:
        raise ValueError("Invalid format. Must be 'svg' or 'pdf'.")

    # Split the PDF into separate pages
    print(f'Target format: {format}')
    print(f"Splitting {pdf_file} into separate pages")
    subprocess.run(["pdfseparate", pdf_file, f"{output_prefix}%d.pdf"], check=True)

    pdf_file_list = [f"{output_prefix}{i}.pdf" for i in range(1, 1 + len(equations))]

    if format == 'svg':
        # Convert each split PDF to SVG
        for i, pdf in enumerate(pdf_file_list):
            svg_file = pdf.replace(".pdf", ".svg")

            subprocess.run(["pdf2svg", pdf, svg_file], check=True)

        output_file_list = [pdf.replace(".pdf", ".svg") for pdf in pdf_file_list]

    elif format == 'pdf':
        output_file_list = pdf_file_list

    print()
    for i, file in enumerate(output_file_list):
        print(f'Output file {i+1}: {file}')

    return output_file_list


def cleanup_files(latex_file="equations.tex", pdf_file="equations.pdf", format='svg'):

    print(f'\nCleaning up intermediate files.')
    # Remove the LaTeX file
    if os.path.exists(latex_file):
        os.remove(latex_file)

    # Remove the .aux file
    if os.path.exists(latex_file.replace(".tex", ".aux")):
        os.remove(latex_file.replace(".tex", ".aux"))

    # Remove the .log file
    if os.path.exists(latex_file.replace(".tex", ".log")):
        os.remove(latex_file.replace(".tex", ".log"))

    # Remove the PDF file
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

    # Remove the split PDF files
    if format == 'svg':
        for i in range(1, 100):
            pdf_file = f"eqn{i}.pdf"
            if os.path.exists(pdf_file):
                os.remove(pdf_file)


def print_header():
    print("="*20+"eqn2vec"+"="*20)


def eqn2vec(equations, style='display', format='svg', keep=False, latex_compiler='latex'):

    trun = time.perf_counter()

    print_header()

    # Check equations type
    if not isinstance(equations, list):
        equations = [equations]

    check_environment(latex_compiler=latex_compiler)

    latex_file = create_latex_file(equations, style=style)

    #latex_compiler = "latex"
    #latex_compiler = "pdflatex"

    compiled_pdf = compile_latex_wrapper(latex_file, latex_compiler=latex_compiler)

    split_pdf(compiled_pdf, equations, format=format)

    if not keep:
        cleanup_files(latex_file, compiled_pdf, format=format)

    print("="*13+f"Done in {time.perf_counter()-trun:.2f} seconds"+"="*14+"\n")

def main():
    #eq_list = []
    #eq_list.append("U(\\mathbf{X} ; \\boldsymbol{\\Theta})")
    #eq_list.append("x=y\\tilde{u}")

    # Parse command line arguments
    parser = argparse.ArgumentParser(
                description="Convert LaTeX equations to vector image files.")

    parser.add_argument('-eq', '--equations', required=True, nargs="*", help="The LaTeX equations to convert to vector images.")
    parser.add_argument('-f', '--format', default="svg", help="The format of the vector image files. Must be 'svg' or 'pdf'.")
    parser.add_argument('-c', '--compiler', default="latex", help="The LaTeX compiler to use. Must be 'latex' or 'pdflatex'.")
    parser.add_argument('-k', '--keep', action="store_true", help="Keep the intermediate LaTeX and PDF files.")
    parser.add_argument('-s', '--style', default="display", help="The style of the LaTeX equations. Must be 'display' or 'inline'.")

    args = parser.parse_args()

    eqn2vec(args.equations, style=args.style, format=args.format.lower(), keep=args.keep, latex_compiler=args.compiler)


if __name__ == "__main__":
    main()