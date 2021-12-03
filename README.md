To replicate:

1.  Create a file `APIKEY` containing your Rev.ai API key.

2.  Run [`./submit.py`](submit.py).

3.  Wait for recognition to complete.

4.  Use [`./retrieve.py`](retrieve.py) to retrieve the hypothesis
    transcriptions:

        ./retrieve.py > hypo.tsv

5.  Use [`wer.py`](wer.py) to compute the WER:

        ./wer.py gold.tsv hypo.tsv

I obtain a WER of 19.30.