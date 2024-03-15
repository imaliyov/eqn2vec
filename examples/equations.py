#!/usr/bin/env python3

from eqn2vec import eqn2vec


def main():

    eq_list = [
        r'E = mc^2',
        r'S = \sum_{i=1}^n x_i',
        r'A = \int_0^1 f(x) dx',
    ]

    eqn2vec.eqn2vec(eq_list[:2],
                    style='inline',
                    format='pdf',
                    keep=False,
                    latex_compiler='latex')

    eqn2vec.eqn2vec(eq_list[2],
                    style='display',
                    format='pdf')


if __name__ == '__main__':
    main()