#!/usr/bin/env python3
import sys


def get_blocks(stdin):
    """
    Retrieve records from stdin. Each record starts with a ">".
    """
    block = []
    for line in stdin:
        if block and line.startswith('>'):
            yield block
            block = []
        block.append(line.strip())
    if block:
        yield block


def compute_hp(block):
    """
    Compute the H_p
    """
    header = block.pop(0).split(" ")[0]
    header = header[1:]  # Trim the >
    header = header.split(":")
    chromosome, position = header[0:2]
    sum_major = 0
    sum_minor = 0

    for line in block:

        if not line:
            break

        line = line.strip().split("\t")
        genotypes = map(int, line[4:8])
        genotypes = sorted(genotypes, reverse=True)
        major, minor, *_ = genotypes
        sum_major += major
        sum_minor += minor

    if sum_major > 0 and sum_minor > 0:
        hp = 2 * sum_major * sum_minor / (sum_major + sum_minor)**2
    else:
        hp = "NA"

    result_string = f"{chromosome}\t{position}\t{hp}\n"

    return result_string


if __name__ == "__main__":
    hps = (compute_hp(block) for block in get_blocks(sys.stdin))
    for result in hps:
        sys.stdout.write(result)
