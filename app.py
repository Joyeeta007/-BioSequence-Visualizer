import streamlit as st

st.title("🧬 DNA Sequence Analyzer (FASTA Input)")

uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta", "fa", "txt"])

def validate_seq(sequence):
    validSeq = "ATGC"
    for base in sequence:
        if base.upper() not in validSeq:
            return False
    return True

def replaceStrain(seq):
    length=len(seq)
    complementedStrain=""

    for i in range(0,length):
        if seq[i] == "A":
            complementedStrain+="T"
        elif seq[i] == "T":
            complementedStrain+="A"
        elif seq[i] == "C":
            complementedStrain+="G"
        elif seq[i] == "G":
            complementedStrain+="C"
    return complementedStrain

if uploaded_file:

    content = uploaded_file.getvalue().decode("utf-8").splitlines()

    sequence = ""

    for line in content:
        line = line.strip()
        if not line.startswith(">"):   # Ignore headers
            sequence += line

    if not sequence:
        st.error("No DNA sequence found in file.")
        st.stop()

    if not validate_seq(sequence):
        st.error("Invalid DNA sequence! Only A, T, G, C allowed.")
        st.stop()

    validatedSeq = sequence.upper()
    st.success("Valid FASTA DNA sequence loaded ✔")

    st.write("Sequence length:", len(validatedSeq))
     # Count nucleotides
    freq = {
            "A": 0,
            "T": 0,
            "G": 0,
            "C": 0,
        }

    for base in validatedSeq:
        freq[base] += 1

    st.subheader("Nucleotide Count")
    st.write(freq)

    length = len(validatedSeq)
    gc_content = (freq["G"] + freq["C"]) / length * 100

    st.subheader("GC Content (%)")
    st.write(round(gc_content, 2))

    replacedString = replaceStrain(validatedSeq)

    st.subheader("Complement Strand")
    st.write(replacedString)
