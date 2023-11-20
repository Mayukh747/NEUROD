import requests

fastaFile = open("fasta.txt")
with open("sequences.txt", 'w') as seq_file:
      for line in fastaFile:
            seq = line.strip()
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db" \
                  "=nucleotide&id=" + seq + "&rettype=fasta&retmode=text"
            # url = "https://www.ncbi.nlm.nih.gov/nuccore/NC_000017.11?report=fasta&from=45894554&to=46028334"
            res = requests.get(url)
            seq_file.write(res.text)