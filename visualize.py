# python visualize.py

# Validate the sequence — check if the input contains only A, T, G, C letters
# Count nucleotides — count how many A, T, G, C are in the sequence
# Calculate GC content — (G+C) divided by total length, multiplied by 100
# Get complement strand — replace each letter: A→T, T→A, G→C, C→G

seq=input("Enter Sequence: ")

def replaceStrain(seq):
    length-len(seq)
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

validatedSeq=validate_seq(seq).upper()
print(validatedSeq)

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

print(freq.items())
length=len(validatedSeq)
gc_content= (freq["G"]+freq["C"])/length*100
print(gc_content)

replacedString= replaceStrain(validatedSeq)
print(replacedString)