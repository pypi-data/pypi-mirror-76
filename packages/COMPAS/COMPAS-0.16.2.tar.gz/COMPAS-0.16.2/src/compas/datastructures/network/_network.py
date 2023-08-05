from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures.network.core import BaseNetwork
from compas.datastructures.network.core import network_split_edge


__all__ = ['Network']


class Network(BaseNetwork):

    split_edge = network_split_edge


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
