# i = 25
#
# destination = open("BirdNeurod1/bird_neurod1.txt", 'x')
# for i in range(1, 26):
#     with open("BirdNeurod1/sequence (" + str(i) + ").fasta") as source:
#         for line in source:
#             destination.write(line)

def determine_smallest_training_set(is_primate: bool):
    '''
    Searches through sequences and divides them into two groups based on sequence length
    :param is_primate:
    :return:
    '''
    l = []
    taxa = ("Primate" if is_primate else "Bird")

    for i in range(1, 26):
        with open(taxa + "Neurod1/sequence (" + str(i) + ").fasta") as source:
            total = 0
            source.readline()
            for line in source:
                total += len(line)
            l.append((total, i))
    l.sort()
    l = [item[1] for item in l]
    return l[:20], l[20:]

def build_training_fasta(is_primate: bool, seq_nums: list[int]) -> None:
    """
    Given a list of sequence numbers, prepare an unaligned text file containing all training sequenecs 
    """
    taxa = ("Primate" if is_primate else "Bird")

    destination = open(taxa + "Protein/" + taxa.lower() + "_training.fa", 'x')
    for n in range(len(seq_nums)):
        i = seq_nums[n]
        with open(taxa + "Protein/sequence (" + str(i) + ").fasta") as source:
            for line in source:
                destination.write(line)


def build_test_set(is_primate: bool, seq_nums: list[int]):
    """
    Given a list of sequence numbers, writes a fasta file for the HMM test set to /DataSets
    :param is_primate:
    :param seq_nums:
    :return:
    """
    taxa = ("Primate" if is_primate else "Bird")

    destination = open("DataSets/" + taxa.lower() + "_test_set.fa", "w")
    for n in reversed(range(len(seq_nums))):
        i = seq_nums[n]
        with open(taxa + "Protein/sequence (" + str(i) + ").fasta",
                  "r") as source:
            destination.write(source.readline())

            # ignore the first line
            # source.readline()
            for line in source:
                destination.write(line.strip("\n>"))
            destination.write("\n")

def compact_all(is_gene: bool) -> None:
    destination = open("DataSets/" + "all_" + ("gene" if is_gene else "protein") +".fa", "w")

    for n in range(1,26):

        with open("Primate" + ("Neurod1" if is_gene else "Protein") + "/sequence (" + str(n) + ").fasta") as source:
            line = source.readline()
            if is_gene:
                destination.write(">" + '-'.join(line.split()[1:3]) + "_primate\n")
            else:
                destination.write(">" + line[line.index("["):-1].replace(" ", "-") + "primate\n")
            for line in source:
                destination.write(line)


        with open("Bird" + ("Neurod1" if is_gene else "Protein") + "/sequence (" + str(n) + ").fasta") as source:
            line = source.readline()
            if is_gene:
                destination.write(">" + '-'.join(line.split()[1:3]) + "_bird\n")
            else:
                destination.write(">" + line[line.index("["):-1].replace(" ", "-") +"bird\n")
            for line in source:
                destination.write(line)

# def clean_compacted(is_gene: bool) -> None:
#     dest = open("DataSets/clean_all_" + ("gene" if is_gene else "protein") + ".fa", "w")
#     with open("DataSets/all_" + ("gene" if is_gene else "protein") + ".fa") as source:
#         for line in source:
#             if line[0] == ">":
#                 if is_gene:
#                     dest.write(">" + '-'.join(line.split()[1:3]) + "\n")
#                 else:
#                     dest.write(">" + line[line.index("["):].replace(" ", "-"))
#             else:
#                 dest.write(line)


# build_test_set(1, [21,22,23,24,25])
#build_training_fasta(0, list(range(1,21)))
# build_test_set(0,list(range(20,26)))
compact_all(1)
# clean_compacted(1)
# clean_compacted(0)