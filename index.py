import streamlit as st
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import time
from visualize import validate_seq, get_complement, findMotif
# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="BioSequence Visualizer",
    page_icon="🧬",
    layout="wide"
)

# ─────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    body { background-color: #0f172a; }
    .main { background-color: #0f172a; }

    .center-header { text-align: center; padding-bottom: 6px; }
    .center-sub { text-align: center; color: #94a3b8; font-size: 15px; margin-bottom: 24px; }

    /* Center analyze button */
    div[data-testid="stButton"] { display: flex; justify-content: center; }
    div[data-testid="stButton"] > button {
        background-color: #4ade80;
        color: #0f172a;
        font-weight: bold;
        font-size: 15px;
        padding: 10px 48px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }

    .section-gap { margin-top: 40px; margin-bottom: 8px; }

    .card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        text-align: center;
    }
    .card-label { color: #94a3b8; font-size: 13px; margin-bottom: 6px; }
    .card-value { color: #4ade80; font-size: 2rem; font-weight: bold; }

    .seq-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .seq-label { color: #94a3b8; font-size: 14px; font-weight: bold; }
    .copy-btn {
        background: #1e293b;
        border: 1px solid #334155;
        color: #94a3b8;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        cursor: pointer;
    }
    .copy-btn:hover { background: #334155; color: #e2e8f0; }

    .seq-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        font-family: monospace;
        font-size: 13px;
        color: #4ade80;
        word-break: break-all;
        line-height: 1.8;
        margin-bottom: 20px;
    }
    .bio-note {
        background-color: #172033;
        border-left: 4px solid #60a5fa;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 12px;
    }
    .dl-center { display: flex; justify-content: center; margin-top: 20px; }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 13px;
        padding: 20px 0 8px 0;
    }

    .gc-low  { color: #f87171 !important; }
    .gc-mid  { color: #4ade80 !important; }
    .gc-high { color: #60a5fa !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# Helper: copy button using JS
# ─────────────────────────────────────────
def seq_block_with_copy(label, seq_text):
    safe = seq_text.replace("`", "")
    components.html(f"""
    <div style="margin-bottom:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <span style="color:#94a3b8; font-size:14px; font-weight:bold;">{label}</span>
        <button onclick="navigator.clipboard.writeText(`{safe}`).then(()=>{{this.innerText='Copied ✔'; setTimeout(()=>this.innerText='Copy',1500)}})"
          style="background:#1e293b; border:1px solid #334155; color:#94a3b8;
                 padding:4px 14px; border-radius:6px; font-size:12px; cursor:pointer;">
          Copy
        </button>
      </div>
      <div style="background:#1e293b; border:1px solid #334155; border-radius:10px;
                  padding:16px; font-family:monospace; font-size:13px; color:#4ade80;
                  word-break:break-all; line-height:1.8;">
        {seq_text}
      </div>
    </div>
    """, height=max(100, 60 + len(seq_text) // 6))


# ─────────────────────────────────────────
# Functions
# ─────────────────────────────────────────


def get_reverse_complement(seq):
    return get_complement(seq)[::-1]

def get_nucleotide_freq(seq):
    return {"A": seq.count("A"), "T": seq.count("T"), "G": seq.count("G"), "C": seq.count("C")}

def get_gc_content(freq, length):
    return round((freq["G"] + freq["C"]) / length * 100, 2)

def get_at_gc_ratio(freq):
    gc = freq["G"] + freq["C"]
    return "N/A" if gc == 0 else round((freq["A"] + freq["T"]) / gc, 2)

def get_melting_temp(freq):
    return 2 * (freq["A"] + freq["T"]) + 4 * (freq["G"] + freq["C"])

def get_purine_pyrimidine(freq):
    return freq["A"] + freq["G"], freq["T"] + freq["C"]

def format_sequence_chunks(seq, chunk=10):
    return "  ".join([seq[i:i+chunk] for i in range(0, len(seq), chunk)])


# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.markdown("<h1 class='center-header'>🧬 DNA Sequence Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='center-sub'>Upload a FASTA file to get a full bioinformatics analysis</p>", unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────
# Input
# ─────────────────────────────────────────
sequence = ""

uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta", "fa", "txt"])
if uploaded_file:
    content = uploaded_file.getvalue().decode("utf-8").splitlines()
    for line in content:
        line = line.strip()
        if not line.startswith(">"):
            sequence += line

st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
_, center_col, _ = st.columns([2, 1, 2])
with center_col:
    analyze = st.button("🔬 Analyze", use_container_width=True)


# ─────────────────────────────────────────
# Analysis
# ─────────────────────────────────────────
if analyze:
    if not sequence:
        st.error("No sequence provided. Please upload a FASTA file.")
        st.stop()

    if not validate_seq(sequence):
        st.error("Invalid sequence! Only A, T, G, C characters are allowed.")
        st.stop()

    # ── Auto scroll (works via components.html) ──
    components.html("""
    <script>
        window.parent.document.querySelector('section.main').scrollBy({ top: 500, behavior: 'smooth' });
    </script>
    """, height=0)

    # ── Dynamic Loading Bar ──
    progress_bar = st.progress(0, text="Initializing analysis...")
    steps = [
        (15,  "Validating sequence..."),
        (35,  "Counting nucleotides..."),
        (55,  "Calculating GC content & melting temperature..."),
        (75,  "Generating complement strands..."),
        (90,  "Building frequency chart..."),
        (100, "Analysis complete ✔"),
    ]
    for pct, msg in steps:
        time.sleep(0.3)
        progress_bar.progress(pct, text=msg)

    seq            = sequence.upper()
    freq           = get_nucleotide_freq(seq)
    length         = len(seq)
    gc             = get_gc_content(freq, length)
    at_gc          = get_at_gc_ratio(freq)
    tm             = get_melting_temp(freq)
    purine, pyrimidine = get_purine_pyrimidine(freq)
    complement     = get_complement(seq)
    rev_complement = get_reverse_complement(seq)

    st.success("Valid DNA sequence loaded ✔")

    # ─────────────────────────────────────
    # Section 1 — Stats Cards
    # ─────────────────────────────────────
    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.subheader("📊 Sequence Statistics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><div class='card-label'>Sequence Length</div><div class='card-value'>{length} bp</div></div>", unsafe_allow_html=True)
    with c2:
        gc_class = "gc-low" if gc < 40 else "gc-high" if gc > 60 else "gc-mid"
        st.markdown(f"<div class='card'><div class='card-label'>GC Content</div><div class='card-value {gc_class}'>{gc}%</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><div class='card-label'>Melting Temp (Tm)</div><div class='card-value'>{tm}°C</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><div class='card-label'>AT/GC Ratio</div><div class='card-value'>{at_gc}</div></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # Section 2 — GC Meter
    # ─────────────────────────────────────
    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.subheader("🧪 GC Content Meter")
    gc_color = "#f87171" if gc < 40 else "#60a5fa" if gc > 60 else "#4ade80"
    st.markdown(f"""
    <div style="background:#1e293b; border-radius:99px; height:22px; border:1px solid #334155; overflow:hidden;">
        <div style="width:{gc}%; background:{gc_color}; height:100%; border-radius:99px;"></div>
    </div>
    <div style="display:flex; justify-content:space-between; color:#64748b; font-size:12px; margin-top:4px;">
        <span>0%</span><span>50%</span><span>100%</span>
    </div>
    <div class='bio-note'>
        💡 GC content between 40–60% is typical for most organisms.
        High GC content indicates more thermally stable DNA.
        Melting temperature (Tm) uses the Wallace Rule: Tm = 2(A+T) + 4(G+C).
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────
    # Section 3 — Nucleotide Counts
    # ─────────────────────────────────────
    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.subheader("🔢 Nucleotide Counts")
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        st.markdown(f"<div class='card'><div class='card-label'>Adenine (A)</div><div class='card-value' style='color:#4ade80'>{freq['A']}</div></div>", unsafe_allow_html=True)
    with n2:
        st.markdown(f"<div class='card'><div class='card-label'>Thymine (T)</div><div class='card-value' style='color:#f87171'>{freq['T']}</div></div>", unsafe_allow_html=True)
    with n3:
        st.markdown(f"<div class='card'><div class='card-label'>Guanine (G)</div><div class='card-value' style='color:#60a5fa'>{freq['G']}</div></div>", unsafe_allow_html=True)
    with n4:
        st.markdown(f"<div class='card'><div class='card-label'>Cytosine (C)</div><div class='card-value' style='color:#facc15'>{freq['C']}</div></div>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#94a3b8; margin-top:4px;'><b>Purines (A+G):</b> {purine} &nbsp;&nbsp; <b>Pyrimidines (T+C):</b> {pyrimidine}</p>", unsafe_allow_html=True)

    # ─────────────────────────────────────
    # Section 4 — Chart (centered, compact)
    # ─────────────────────────────────────
    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.subheader("📈 Nucleotide Frequency Chart")

    _, col_chart, _ = st.columns([1, 2, 1])
    with col_chart:
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.patch.set_facecolor('#1e293b')
        ax.set_facecolor('#1e293b')
        bars = ax.bar(
            list(freq.keys()),
            list(freq.values()),
            color=['#4ade80', '#f87171', '#60a5fa', '#facc15'],
            edgecolor='#334155',
            linewidth=0.8,
            width=0.5
        )
        ax.set_title("Nucleotide Frequency", color='#e2e8f0', fontsize=11, pad=8)
        ax.set_xlabel("Nucleotide", color='#94a3b8', fontsize=9)
        ax.set_ylabel("Count", color='#94a3b8', fontsize=9)
        ax.tick_params(colors='#94a3b8', labelsize=9)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_ylim(0, max(freq.values()) + 12)
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 3,
                str(int(bar.get_height())),
                ha='center', va='bottom',
                color='#e2e8f0', fontsize=9
            )
        plt.tight_layout()
        st.pyplot(fig)

    # ─────────────────────────────────────
    # Section 5 — Strand Information
    # ─────────────────────────────────────
    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.subheader("🔗 Strand Information")

    seq_block_with_copy("Original Sequence (grouped by 10)", format_sequence_chunks(seq))
    seq_block_with_copy("Complement Strand", format_sequence_chunks(complement))
    seq_block_with_copy("Reverse Complement", format_sequence_chunks(rev_complement))

    # ── Centered Download Button ──
    all_seqs = (
        f">Original\n{seq}\n\n"
        f">Complement\n{complement}\n\n"
        f">Reverse_Complement\n{rev_complement}\n"
    )
    _, dl_col, _ = st.columns([1, 1, 1])
    with dl_col:
        st.download_button(
            label="⬇️ Download All Sequences (.txt)",
            data=all_seqs,
            file_name="sequences.txt",
            mime="text/plain",
            use_container_width=True
        )
    st.subheader("Motif Detection")

    motif_pattern = st.text_input("Enter motif pattern (regex allowed)")

    if st.button("Search Motif"):

        if motif_pattern.strip() == "":
            st.warning("Please enter a motif pattern.")
        else:
            positions = findMotif(seq, motif_pattern)

    if positions:
        st.success(f"{len(positions)} match(es) found!")
        st.write("Positions:", positions)
    else:
        st.warning("No matches found.")


    # ─────────────────────────────────────
    # Footer
    # ─────────────────────────────────────
    st.markdown("<div style='margin-top:48px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p class='footer'>Built by Joyeeta Sarkar Puja | Bioinformatics Engineering, BAU</p>", unsafe_allow_html=True)