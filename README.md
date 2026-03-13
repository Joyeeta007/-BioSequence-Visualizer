# 🧬 BioSequence Visualizer

A web-based DNA sequence analysis tool built with Python and Streamlit. Upload a FASTA file and get an instant, comprehensive bioinformatics report — no installation required.

**🔗 Live Demo:** [biovisualizer.streamlit.app](https://biovisualizer.streamlit.app)

---

## Features

| Section | What it does |
|---|---|
| 📊 Sequence Statistics | Sequence length, GC content, melting temperature (Tm), AT/GC ratio |
| 🧪 GC Content Meter | Color-coded visual bar — red (low), green (normal), blue (high) |
| 🔢 Nucleotide Counts | Individual A, T, G, C counts with purine/pyrimidine totals |
| 📈 Frequency Chart | Bar chart of nucleotide distribution |
| 📉 GC Along Sequence | Sliding window line graph showing GC% across the sequence |
| 🔍 Motif Detection | Search for any pattern (supports regex) and get all match positions |
| 🧫 Annotated Features | Auto-detects start codons (ATG) and stop codons (TAA, TAG, TGA) |
| 🔗 Strand Information | Original, complement, and reverse complement with one-click copy |
| ⬇️ Download | Export all three strands as a `.txt` file |


## How to Use

1. Go to [biovisualizer.streamlit.app](https://biovisualizer.streamlit.app)
2. Upload a `.fasta`, `.fa`, or `.txt` file containing a valid DNA sequence
3. Click **Analyze**
4. View your full analysis report

### Sample FASTA format
```
>gene_name
ATGCGATCGATCGTAGCTAGCATGCATGCATGCGCTAGCTAGC
```


## Run Locally

**Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/biosequence-visualizer.git
cd biosequence-visualizer
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Run the app**
```bash
streamlit run app.py
```


## Project Structure

```
biosequence-visualizer/
├── app.py            # Streamlit UI and layout
├── visualize.py      # All bioinformatics logic and functions
├── requirements.txt  # Python dependencies
└── README.md
```

### Logic separation
- `visualize.py` handles all biological computation — validation, nucleotide counting, GC content, melting temperature, complement generation, motif detection, sliding window analysis, and codon annotation
- `app.py` handles only the UI — importing functions from `visualize.py` and rendering results


## Science Behind the Features

**GC Content** — percentage of guanine and cytosine bases. Values between 40–60% are typical for most organisms. Higher GC content means more thermally stable DNA.

**Melting Temperature (Tm)** — calculated using the Wallace Rule: `Tm = 2(A+T) + 4(G+C)`. Commonly used in primer design and PCR experiments.

**Sliding Window GC** — GC% calculated in overlapping windows of 10 bases across the sequence. Used to identify GC-rich or AT-rich regions in a genome.

**Motif Detection** — uses Python's `re.finditer()` to find all occurrences of a pattern including overlapping matches. Supports full regex syntax (e.g. `AT[GC]`).

**Codon Annotation** — detects start codon `ATG` and stop codons `TAA`, `TAG`, `TGA` and displays their positions in a sortable table.


## Tech Stack

- **Python 3**
- **Streamlit** — web interface
- **Matplotlib** — bar chart and sliding window line chart
- **Pandas** — annotation features table
- **re** — regex-based motif detection


## Built By

**Joyeeta Sarkar Puja**
[LinkedIn](https://www.linkedin.com/in/joyeeta--sarkar) · [GitHub](https://github.com/Joyeeta007)
