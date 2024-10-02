# Benchmarking Semantic Sensitive Information in LLMs Outputs

This is the project repository of our anonymous submission.

## Abstract
Large language models (LLMs) can output sensitive information, which has emerged as a novel safety concern. Previous works focus on structured sensitive information (e.g. personal identifiable information). However, we notice that sensitive information in LLMs’ outputs can also be at the semantic level, i.e. semantic sensitive information (SemSI). Particularly, simple natural questions can let state-of-the-art (SOTA) LLMs output SemSI. Compared to previous work of structured sensitive information in LLM’s outputs, SemSI are hard to define and are rarely studied. Therefore, we propose a novel and large-scale investigation on SemSI for SOTA LLMs. First, we construct a comprehensive and labeled dataset of semantic sensitive information, SemSI-Set, by including three typical categories of SemSI. Then, we propose a large-scale benchmark, SemSI-Bench, to systematically evaluate semantic sensitive information in 25 SOTA LLMs. Our
finding reveals that SemSI widely exists in SOTA LLMs’ outputs by querying with simple natural questions.


<img src="image.png" alt="" width="600">


## Semantic sensitive information (SemSI)

### Definition 
***It consists of at least a subject and a predicate and expresses a viewpoint or a statement that has a risk of harm towards the subject.***

### Taxonomy
* Sensitive identity attributes (S)
* Reputation-harmful contents (R)
* Incorrect hazardous information (I)

## The first dataset for SemSI, SemSI-Set
We construct a dataset, SemSI-Set, with 10,830 prompts (in ```./dataset/final_processed_dataset.json```) about hot news collected from three fact-checking websites (politifact, snopes, factcheck), to systematically evaluate the occurrence of SemSI. GPT-4o is used to label 9 fields on each answer of LLMs (in ```./code/metric_merge.py```) and the validity is verified by experts.

We have evaluated 25 popular LLMs. We currently release the dataset for GPT-4o and GPT-3.5-turbo (in ```./dataset```). We will release the remaining 23 LLMs dataset once our paper is accepted.  

## Benchmark for SemSI, SemSI-Bench
To evaluate SemSI behavior of an LLM, we first prompt it with prompts in SemSI-Set (in ```./code/genLLManswer.py```), and label each answer with the nine fields related to SemSI. With these nine fields, we can compute metrics to compare LLMs and construct a leaderboard of SemSI safety, SemSI-Board (in ```./code/leaderboard.ipynb```).

### Metrics
* Occurrence rate (OR)
* Toxicity score (TS)
* Coverage (CR)

### Leaderboard, SemSI-Board
| Model                  | o-OR(%) | o-TS | o-CR(%) | p-OR(%) | r-OR(%) | m-OR(%) | p-TS | r-TS | m-TS | p-CR(%) | r-CR(%) | m-CR(%) |
|------------------------|---------|------|---------|---------|---------|---------|------|------|------|---------|---------|---------|
| GPT-4o                 | 42.09   | 1.30 | 15.23   | 30.92   | 28.60   | 6.14    | 0.59 | 0.57 | 0.13 | 17.87   | 6.51    | 1.26    |
| GPT-4                  | 46.18   | 1.43 | 20.66   | 31.49   | 29.68   | 11.97   | 0.60 | 0.57 | 0.26 | 22.41   | 8.60    | 3.09    |
| GPT-3.5-Turbo          | 45.30   | 1.50 | 24.26   | 27.10   | 27.10   | 17.90   | 0.53 | 0.56 | 0.42 | 20.93   | 9.60    | 5.26    |
| GPT-3.5-Turbo-Instruct | 62.78   | 2.37 | 29.85   | 42.19   | 37.63   | 32.35   | 0.82 | 0.78 | 0.76 | 28.10   | 12.03   | 8.24    |
| Claude3 Opus           | 43.16   | 1.33 | 16.65   | 30.38   | 30.38   | 7.14    | 0.58 | 0.59 | 0.15 | 18.25   | 8.91    | 1.81    |
| Claude3 Sonnet         | 30.45   | 0.82 | 10.83   | 18.49   | 19.90   | 3.82    | 0.34 | 0.39 | 0.08 | 11.50   | 5.32    | 0.59    |
| Claude3 Haiku          | 25.08   | 0.69 | 9.52    | 13.84   | 17.85   | 3.51    | 0.26 | 0.35 | 0.08 | 8.31    | 5.11    | 0.65    |
| Gemini 1.5 Pro         | 37.94   | 1.06 | 9.75    | 23.92   | 27.84   | 4.23    | 0.45 | 0.53 | 0.09 | 13.92   | 6.66    | 0.70    |
| Gemini 1.5 Flash       | 42.01   | 1.27 | 10.93   | 25.93   | 27.80   | 11.83   | 0.50 | 0.52 | 0.25 | 15.30   | 6.82    | 2.74    |
| Gemini 1.0 Pro         | 39.30   | 1.11 | 23.71   | 12.82   | 17.27   | 24.79   | 0.25 | 0.34 | 0.52 | 8.93    | 7.43    | 14.82   |
| Llama3-8B-Instruct     | 52.09   | 1.68 | 16.98   | 30.42   | 26.55   | 25.64   | 0.57 | 0.53 | 0.57 | 18.67   | 7.37    | 6.13    |
| Llama3-8B              | 72.40   | 3.81 | 42.00   | 47.32   | 52.17   | 62.49   | 1.07 | 1.19 | 1.56 | 45.89   | 43.93   | 50.09   |
| Llama2-7B-Chat         | 59.06   | 1.92 | 15.95   | 32.24   | 27.43   | 33.37   | 0.61 | 0.54 | 0.77 | 18.58   | 7.60    | 6.06    |
| Llama2-7B              | 83.90   | 4.18 | 17.44   | 51.39   | 55.42   | 69.20   | 1.18 | 1.27 | 1.72 | 41.75   | 22.37   | 19.94   |
| GLM4-9B-CHAT           | 66.67   | 2.51 | 17.70   | 40.27   | 36.59   | 41.22   | 0.78 | 0.76 | 0.98 | 20.63   | 6.99    | 7.67    |
| GLM4-9B                | 68.44   | 3.07 | 18.86   | 35.71   | 39.55   | 57.14   | 0.77 | 0.88 | 1.42 | 24.65   | 18.78   | 20.89   |
| GPT-J-6B               | 35.11   | 0.99 | 5.00    | 9.21    | 5.94    | 30.19   | 0.16 | 0.13 | 0.70 | 5.99    | 1.82    | 4.50    |
| Gemma-7B-Instruct      | 26.81   | 0.66 | 17.64   | 2.12    | 8.87    | 21.57   | 0.04 | 0.17 | 0.45 | 2.00    | 5.16    | 16.59   |
| MiniCPM-Llama3-V       | 63.39   | 2.44 | 32.04   | 33.03   | 33.54   | 45.60   | 0.67 | 0.69 | 1.08 | 26.00   | 11.58   | 15.40   |
| Phi-3-Mini-4K-Instruct | 39.59   | 1.22 | 10.03   | 21.02   | 14.90   | 24.08   | 0.38 | 0.29 | 0.55 | 12.11   | 3.89    | 4.93    |
| Qwen2-7B-Instruct      | 46.76   | 1.64 | 13.91   | 27.60   | 23.38   | 28.22   | 0.52 | 0.46 | 0.65 | 17.07   | 5.13    | 5.64    |
| Mistral-7B-Instruct-v0.3 | 56.21 | 1.91 | 21.35   | 34.93   | 30.35   | 27.60   | 0.68 | 0.60 | 0.63 | 21.10   | 8.15    | 6.29    |

