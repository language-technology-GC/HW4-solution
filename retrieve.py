#!/usr/bin/env python
"""Submits the files for recognition."""

import csv
import logging
import re
import sys

from rev_ai import apiclient  # type: ignore


def main() -> None:
    with open("APITOKEN", "r") as source:
        token = source.readline().rstrip()
    client = apiclient.RevAiAPIClient(token)
    transcribed = 0
    tsv_writer = csv.writer(sys.stdout, delimiter="\t")
    for job in client.get_list_of_jobs():
        assert job.status.name == "TRANSCRIBED", f"Unexpected status: {job.id}"
        flac_path = job.name
        logging.info("Getting transcript for %s...", flac_path)
        transcript = client.get_transcript_text(job.id)
        transcript = re.sub(
            r"^Speaker\s+(\d+)\s+(\d\d:\d\d:\d\d)\s+(.+)$",
            r"\g<3>",
            transcript,
        ).rstrip()
        tsv_writer.writerow([job.name, transcript])
        transcribed += 1
    logging.info("%d files transcribed", transcribed)


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    main()
