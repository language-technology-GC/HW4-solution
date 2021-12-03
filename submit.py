#!/usr/bin/env python
"""Submits the files for recognition."""

import glob
import logging


from rev_ai import apiclient  # type: ignore


LANGUAGE = "en"


def main() -> None:
    with open("APITOKEN", "r") as source:
        token = source.readline().rstrip()
    client = apiclient.RevAiAPIClient(token)
    for flac_path in glob.iglob("flac/*.flac"):
        logging.info("Submitting %s...", flac_path)
        client.submit_job_local_file(
            flac_path,
            skip_diarization=True,
            skip_punctuation=True,
            language=LANGUAGE,
        )


if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="%(levelname)s: %(message)s")
    main()
