#!/usr/bin/env python
"""Computes WER."""

import argparse
import logging
import re

from typing import Any, List

import numpy
import pandas  # type: ignore


Labels = List[Any]


def _edit_distance(x: Labels, y: Labels) -> int:
    """Computes edit distance."""
    # For a more expressive version of the same, see:
    #
    #     https://gist.github.com/kylebgorman/8034009
    idim = len(x) + 1
    jdim = len(y) + 1
    table = numpy.zeros([idim, jdim], dtype=numpy.uint8)
    table[1:, 0] = 1
    table[0, 1:] = 1
    for i in range(1, idim):
        for j in range(1, jdim):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                c1 = table[i - 1][j]
                c2 = table[i][j - 1]
                c3 = table[i - 1][j - 1]
                table[i][j] = min(c1, c2, c3) + 1
    return int(table[-1][-1])


def _normalize(trans: str) -> str:
    """Applies simple normalizations to the transcription."""
    return re.sub(r"[\.\?\!\,\-]", "", trans).casefold()


def main(args: argparse.Namespace) -> None:
    # TODO(kbg): This could probably be better; I'm not good at Pandas yet.
    gold = pandas.read_csv(args.gold_tsv, sep="\t", names=["flac", "gold"])
    gold.set_index("flac")
    hypo = pandas.read_csv(args.hypo_tsv, sep="\t", names=["flac", "hypo"])
    hypo.set_index("flac")
    merged = gold.merge(hypo)
    merged = merged.applymap(_normalize)
    merged["len"] = merged.gold.apply(lambda trans: len(trans.split()))
    merged["edit"] = merged.apply(
        lambda row: _edit_distance(row["gold"].split(), row["hypo"].split()),
        axis=1,
    )
    wer = 100 * merged["edit"].sum() / merged["len"].sum()
    logging.info("WER: %.2f", wer)


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gold_tsv", help="path to gold TSV file")
    parser.add_argument("hypo_tsv", help="path to hypothesis TSV file")
    main(parser.parse_args())
