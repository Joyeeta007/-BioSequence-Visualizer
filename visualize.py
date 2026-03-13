# python visualize.py

# Validate the sequence — check if the input contains only A, T, G, C letters
# Count nucleotides — count how many A, T, G, C are in the sequence
# Calculate GC content — (G+C) divided by total length, multiplied by 100
# Get complement strand — replace each letter: A→T, T→A, G→C, C→G
import re

# seq=input("Enter Sequence: ")

def get_complement(seq):
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

def get_reverse_complement(seq):
    return get_complement(seq)[::-1]

def get_nucleotide_freq(seq):
    return {
        "A": seq.count("A"),
        "T": seq.count("T"),
        "G": seq.count("G"),
        "C": seq.count("C"),
    }

# def get_gc_content(freq, length):
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

def validate_seq(sequence):
    validSeq='ATGC'
    while True:
        valid=True
        for base in sequence:
            if base.upper() not in validSeq:
                valid=False
                print(f'{base} detected. Try Again')
                sequence=input("Enter Sequence: ")
                break
        if(valid and sequence):
            return sequence
            break

def nucleotide_freq(seq):
    validatedSeq= validate_seq(seq).upper()
    freq={
        "A":0,
        "T":0,
        "G":0,
        "C":0,
    }
    for base in validatedSeq:
        if base == "A":
            freq["A"]+=1
        elif base == "T":
            freq["T"]+=1
        elif base == "C":
            freq["C"]+=1
        elif base == "G":
            freq["G"]+=1
    return freq

# def get_at_gc_ratio(freq):
#    at = freq["A"]+freq["T"]
#    gc = freq["G"]+freq["C"]
#    ratio=at/gc
#    return ratio
# def findMotif(seq,motif):
#     # print(seq.index(motif))
#         seq=seq

# length=len(validatedSeq)
# gc_content= (freq["G"]+freq["C"])/length*100
# print(gc_content)

# replacedString= get_complement(validatedSeq)
# print(replacedString)

# index= findMotif(replacedString, "ATG")
# print(index)

def findMotif(seq,pattern):
    pos=[]

    for match in re.finditer(pattern,seq):
        pos.append(match.start())
    return pos

# print(findMotif(seq,r"(?=(AT[GC]))"))
input="AT[GC]"
# print(f'(?=({input}))')

def calculate_gc_content(sequence):
    """Calculates the GC content of a DNA sequence."""
    g_count = sequence.count('G')
    c_count = sequence.count('C')
    # Handle ambiguous nucleotides or empty windows gracefully
    if len(sequence) == 0:
        return 0.0
    return (g_count + c_count) / len(sequence) * 100.0


def sliding_window(seq,window,step=1):
    gc_values=[]
    pos=[]
    for i in range(0, len(seq) - window + 1, step):
        calcuGC=seq[i:i+window]
        gc_content=calculate_gc_content(calcuGC)
        gc_values.append(gc_content)
        pos.append(i+1)
    return gc_values,pos

# print(sliding_window(seq,2,1))

def get_annotations(seq):
    annotations=[]
    startPositions=findMotif(seq,"ATG")
    for pos in startPositions:
        annotations.append({
            "Codon" : "ATG",
            "Position" : pos,
            "Type" : "Start Codon"
        })
    stopCodon=["TAA","TAG","TGA"]
    for i in range(0,len(stopCodon)):
        # print(stopCodon[i])
        stopPositions=findMotif(seq,stopCodon[i])
        # print(stopPositions)
        for pos in stopPositions:
            annotations.append({
            "Codon" : stopCodon[i],
            "Position" : pos,
            "Type" : "Stop Codon" 
            })
    return sorted(annotations, key=lambda x: x["Position"])
    
  

get_annotations("ATGTAATAGAAA")
