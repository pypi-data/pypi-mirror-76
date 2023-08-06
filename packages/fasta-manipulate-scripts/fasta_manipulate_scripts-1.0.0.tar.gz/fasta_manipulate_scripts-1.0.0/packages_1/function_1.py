def Fasta_OnelineFasta(inputfile,outputfile):
    file1=open(inputfile,"r")
    file2=file1.read().strip().split(">")[1:]    
    for elements1 in file2:
        elements2 = elements1.strip().split("\n")
        name = elements2[0]
        length = len(elements2)
        i=1
        seq = ""
        while i < length:
            seq = seq + elements2[i]
            i = i+1
        i = 1
        with open(outputfile,"a+")as f:
            f.write(">" + name + "\n"  + seq +"\n" )

