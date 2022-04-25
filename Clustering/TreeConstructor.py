
'''
Modified BioPython Phylo Tree constructors to get rid of inner namings.
'''

import copy
from Bio.Phylo import BaseTree
from Bio.Phylo.TreeConstruction import DistanceMatrix

def upgma(distance_matrix):
    """Construct and return an UPGMA tree.
    Constructs and returns an Unweighted Pair Group Method
    with Arithmetic mean (UPGMA) tree.
    :Parameters:
        distance_matrix : DistanceMatrix
            The distance matrix for tree construction.
    """
    if not isinstance(distance_matrix, DistanceMatrix):
        raise TypeError("Must provide a DistanceMatrix object.")

    # make a copy of the distance matrix to be used
    dm = copy.deepcopy(distance_matrix)
    # init terminal clades
    clades = [BaseTree.Clade(None, name) for name in dm.names]
    # init minimum index
    min_i = 0
    min_j = 0
    inner_count = 0
    while len(dm) > 1:
        min_dist = dm[1, 0]
        # find minimum index
        for i in range(1, len(dm)):
            for j in range(0, i):
                if min_dist >= dm[i, j]:
                    min_dist = dm[i, j]
                    min_i = i
                    min_j = j

        # create clade
        clade1 = clades[min_i]
        clade2 = clades[min_j]
        inner_count += 1
        inner_clade = BaseTree.Clade(None, "C" + str(inner_count))
        inner_clade.clades.append(clade1)
        inner_clade.clades.append(clade2)
        # assign branch length
        if clade1.is_terminal():
            clade1.branch_length = min_dist * 1.0 / 2
        else:
            clade1.branch_length = min_dist * 1.0 / 2 - _height_of(clade1)

        if clade2.is_terminal():
            clade2.branch_length = min_dist * 1.0 / 2
        else:
            clade2.branch_length = min_dist * 1.0 / 2 - _height_of(clade2)

        # update node list
        clades[min_j] = inner_clade
        del clades[min_i]

        # rebuild distance matrix,
        # set the distances of new node at the index of min_j
        for k in range(0, len(dm)):
            if k != min_i and k != min_j:
                dm[min_j, k] = (dm[min_i, k] + dm[min_j, k]) * 1.0 / 2

        dm.names[min_j] = "C" + str(inner_count)

        del dm[min_i]
    inner_clade.branch_length = 0
    return BaseTree.Tree(inner_clade)



def nj(distance_matrix):
    """Construct and return a Neighbor Joining tree.
    :Parameters:
        distance_matrix : DistanceMatrix
            The distance matrix for tree construction.
    """
    if not isinstance(distance_matrix, DistanceMatrix):
        raise TypeError("Must provide a DistanceMatrix object.")

    # make a copy of the distance matrix to be used
    dm = copy.deepcopy(distance_matrix)
    # init terminal clades
    clades = [BaseTree.Clade(None, name) for name in dm.names]
    # init node distance
    node_dist = [0] * len(dm)
    # init minimum index
    min_i = 0
    min_j = 0
    inner_count = 0
    # special cases for Minimum Alignment Matrices
    if len(dm) == 1:
        root = clades[0]

        return BaseTree.Tree(root, rooted=False)
    elif len(dm) == 2:
        # minimum distance will always be [1,0]
        min_i = 1
        min_j = 0
        clade1 = clades[min_i]
        clade2 = clades[min_j]
        clade1.branch_length = dm[min_i, min_j] / 2.0
        clade2.branch_length = dm[min_i, min_j] - clade1.branch_length
        inner_clade = BaseTree.Clade(None, "Inner")
        inner_clade.clades.append(clade1)
        inner_clade.clades.append(clade2)
        clades[0] = inner_clade
        root = clades[0]

        return BaseTree.Tree(root, rooted=False)
    while len(dm) > 2:
        # calculate nodeDist
        for i in range(0, len(dm)):
            node_dist[i] = 0
            for j in range(0, len(dm)):
                node_dist[i] += dm[i, j]
            node_dist[i] = node_dist[i] / (len(dm) - 2)

        # find minimum distance pair
        min_dist = dm[1, 0] - node_dist[1] - node_dist[0]
        min_i = 0
        min_j = 1
        for i in range(1, len(dm)):
            for j in range(0, i):
                temp = dm[i, j] - node_dist[i] - node_dist[j]
                if min_dist > temp:
                    min_dist = temp
                    min_i = i
                    min_j = j
        # create clade
        clade1 = clades[min_i]
        clade2 = clades[min_j]
        inner_count += 1
        inner_clade = BaseTree.Clade(None, "I" + str(inner_count))
        inner_clade.clades.append(clade1)
        inner_clade.clades.append(clade2)
        # assign branch length
        clade1.branch_length = (
            dm[min_i, min_j] + node_dist[min_i] - node_dist[min_j]
        ) / 2.0
        clade2.branch_length = dm[min_i, min_j] - clade1.branch_length

        # update node list
        clades[min_j] = inner_clade
        del clades[min_i]

        # rebuild distance matrix,
        # set the distances of new node at the index of min_j
        for k in range(0, len(dm)):
            if k != min_i and k != min_j:
                dm[min_j, k] = (
                    dm[min_i, k] + dm[min_j, k] - dm[min_i, min_j]
                ) / 2.0

        dm.names[min_j] = "I" + str(inner_count)
        del dm[min_i]

    # set the last clade as one of the child of the inner_clade
    root = None
    if clades[0] == inner_clade:
        clades[0].branch_length = 0
        clades[1].branch_length = dm[1, 0]
        clades[0].clades.append(clades[1])
        root = clades[0]
    else:
        clades[0].branch_length = dm[1, 0]
        clades[1].branch_length = 0
        clades[1].clades.append(clades[0])
        root = clades[1]

    return BaseTree.Tree(root, rooted=False)


def _height_of(clade):
    """Calculate clade height -- the longest path to any terminal (PRIVATE)."""
    height = 0
    if clade.is_terminal():
        height = clade.branch_length
    else:
        height = height + max(_height_of(c) for c in clade.clades)
    return height