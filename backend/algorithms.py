from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Sequence:
    seq_id: int
    gene: str
    locus_tag: str
    db_xref: str
    protein: str
    protein_id: str
    location: str
    gb_key: str
    sequence: str
    id: int = 0

class Sequences:

    def __init__(self, file_contents: str):
        # populate data structure
        self.sequences = []
        # go line by line through fc and populate sequences
        current_sequence_str = ''
        current_sequence = None
        lines = file_contents.splitlines()
        for i, line in enumerate(lines):
            line = line.decode('ascii')
            if i == (len(lines)-1):
                # last run
                current_sequence.sequence = current_sequence_str
                self.sequences.append(current_sequence)
                break
            if line == '':
                continue
            if line[0] == '>':
                # parse definition line
                if current_sequence and current_sequence_str:
                    current_sequence.sequence = current_sequence_str
                    self.sequences.append(current_sequence)
                    current_sequence_str = ''
                i = 1
                while line[i] != ' ':
                    i += 1
                name = line[1:i]
                remainder = line[i+1:]
                items = remainder.split('[')
                field_dict = defaultdict(str)
                for item in items:
                    if item == '':
                        continue
                    # strip off space (if present) and closing bracket
                    if item[-1] == ' ':
                        item = item[:-1]
                    if item[-1] == ']':
                        item = item[:-1]
                    k_v = item.split('=')
                    field_dict[k_v[0]] = k_v[1]
                s = Sequence(name, field_dict['gene'], field_dict['locus_tag'],
                    field_dict['db_xref'], field_dict['protein'], 
                    field_dict['protein_id'], field_dict['location'], field_dict['gbkey'],
                    field_dict['sequence'])
                current_sequence = s
            else:
                current_sequence_str = current_sequence_str + line


class DynoLibrary:

    instance = None

    @classmethod
    def set_instance(self, instance: Sequences):
        self.instance = instance

    def __init__(self):
        self.singleton
    
    def search(sequences: Sequences, target, max_distance=0):
        # search sequences for target (exact or hamming)
        # think about optimizations like using a db or building an index from scratch
        def serialize_sequence(seq: Sequence):
            output = {}
            output['seq_id'] = seq.seq_id
            output['gene'] = seq.gene
            output['locus_tag'] = seq.locus_tag
            output['db_xref'] = seq.db_xref
            output['protein'] = seq.protein
            output['protein_id'] = seq.protein_id
            output['location'] = seq.location
            output['gb_key'] = seq.gb_key
            output['sequence'] = seq.sequence
            output['id'] = 0
            return output

        matches = []
        if max_distance == 0:
            # exact matches
            for sequence in sequences.sequences:
                if target in sequence.sequence:
                    matches.append(serialize_sequence(sequence))
        elif max_distance > 0:
            # hamming matches
            for sequence in sequences.sequences:
                sequence_str = sequence.sequence
                # calculate hamming distance
                # for each possible substring
                # until finding a match
                start = 0
                end = len(target) - 1
                while end < len(sequence_str):
                    distance = 0
                    count = 0
                    for i in range(start, end + 1):
                        if sequence_str[i] != target[count]:
                            distance += 1
                        count += 1
                    if distance <= max_distance:
                        matches.append(serialize_sequence(sequence))
                        break
                    start += 1
                    end += 1
        else:
            return []
        return matches