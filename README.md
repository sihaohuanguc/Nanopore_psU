# Description
This protocol is used for pseudouridine (psU, Ψ) prediction of nanopore RNA direct sequencing data. There is no minimum input reads requirement but a raw dataset of >1M reads is recommended for the following processing for human transcriptome. For a larger transcriptome, more reads are recommended.

This protocol is tested on a cluster of linux system ("midway2", Scientific Linux 7.2).
# Package versions
The version of softwares and packages for testing codes:

Python3: 3.6.6

guppy_basecaller: 3.2.2+9fe0a78 ((C) Oxford Nanopore Technologies, Limited) (So far this software is only available when you are a customer of Oxford Nanopore Technologies)

minimap2: 2.18-r1015

samtools: 1.11 (Copyright (C) 2020 Genome Research Ltd.)

Python packages:

pickle: 4.0 (python3)

numpy: 1.16.4

sklearn: 0.20.4

re: 2.2.1

pandas: 0.24.2

# Download
You could download the package to your cluster by the following command.
```bash
git clone https://github.com/sihaohuanguc/Nanopore_psU.git
```
Then go to the folder with the `setup.py` file. And run
```bash
pip3 install .
```
Now you've installed the package. You could use it at any place of your account.
**Make sure that your default python is python3 but not python2.**

# Reference and citation
If you would like to use this package in your work, please cite the following paper:

(Placeholder)

# Protocol
## 1. Base call
You could base call the reads during sequencing. If so, this step is not necessary. If the data is not base called, use the following command to do the base call.
```bash
guppy_basecaller --input_path fast5 \
                 --recursive \
                 --save_path fastq \
                 --records_per_fastq 0 \
                 --flowcell FLO-MIN106 \
                 --kit SQK-RNA002 \
                 --qscore_filtering \
                 --min_qscore 7 \
                 --cpu_threads_per_caller 3 \
                 --num_callers 5
```
"Input_path" is the path of your raw data. "Save_path" is your output folder. "Flowcell" is the type of nanopore flowcell you use. "Kit" is the version of nanopore direct RNA sequencing kit you use. Customize "cpu_threads_per_caller" and "num_caller" according to the state of your own cluster. This step is computation intensive.

## 2. Alignment and pile up
```bash
python alignment.py fastq/pass/ GRCh38.p13.genome.fa
```
The first argument is the input fastq path. The fastq files must be directly in this folder. The second argument is the genome reference file.
The output is a folder "alignment" with two subfolders. The two subfolders contains data of reads aligned to forward and reverse strands respectively. This step is computation intensive.

If you would like to test the package on your device. Please copy the `example` folder, which contains 200 reads of human 18S rRNA and its reference sequence, to a place you like and go to that place. Then run the following command.
```bash
nanopsu alignment -i example/fastq -r example/reference.fa
```
If everything is correct, you'll get a folder named `alignment` in you current folder and there is a `plus_strand` folder in the `a;ignment` folder. Check the folder and you'll see the following files.
```bash
$ ls alignment/plus_strand/
collect.bam    collect_pile.txt  collect.sorted.bam  reference.fa.fai
collect.fastq  collect.sam       reference.fa
```
Of course, you could use the `.bam` file or the `_pile.txt` file for analysis by other softwares if you want. Here in this example there is no `minus_strand` folder as all the RNA reads are aligned to the forward strand of the reference. If you align your transcriptome sample to the genome reference, then you'll likely to have both `plus_strand` and `minus_strand` folder.

## 3. Feature extraction
Due to the design of samtools. In the mpileup files, the split reads will be filled a ">" or "<" in the jumped regions and the coverage and the quality score are affected. Run the following script to remove the intron gap sections in the mpileup file. This step is computation intensive.
```bash
python remove_intron.py
```
For the testing example, you'll find a file called `collect_pile_no_intron.txt` in the `plus_strand` folder.

Then extract 12 features of all U sites. This step is computation intensive.
```bash
python extract_features.py
```
The output file is `features.csv` in the `alignment` folder. This file contains information from reads aligned to both forward and reverse strands.

## 4. psU prediction
Make sure that the "model_3_0.pkl" file is in your current folder which contains the "alignment" folder. Then run the following script.
```bash
python3 prediction.py
```
The output file is the "prediction.csv" in the "alignment" folder. Each row contains the reference strand, position, base type, coverage, U probability and psU probability.




