"""
This module contains the tests to check offpele's molecular representations.
"""

import pytest

from offpele.topology import Molecule
from offpele.utils.toolkits import (RDKitToolkitWrapper,
                                    OpenForceFieldToolkitWrapper)
from offpele.utils import get_data_file_path
from .utils import SET_OF_LIGAND_PATHS


class TestMolecule(object):
    """
    It wraps all tests that involve the Molecule class.
    """

    def test_bad_init_parameterization(self):
        """
        It checks that a call to the parameterize function with a Molecule
        unsuccessfully initialized raises an Exception.
        """
        FORCEFIELD_NAME = 'openff_unconstrained-1.1.1.offxml'
        LIGAND_PATH = SET_OF_LIGAND_PATHS[0]
        ligand_path = get_data_file_path(LIGAND_PATH)

        molecule = Molecule()
        with pytest.raises(Exception):
            molecule.parameterize(FORCEFIELD_NAME)

        rdkit_toolkit = RDKitToolkitWrapper()
        molecule._rdkit_molecule = rdkit_toolkit.from_pdb(ligand_path)
        molecule._off_molecule = None

        with pytest.raises(Exception):
            molecule.parameterize(FORCEFIELD_NAME)

        openforcefield_toolkit = OpenForceFieldToolkitWrapper()
        molecule._off_molecule = openforcefield_toolkit.from_rdkit(molecule)
        molecule._rdkit_molecule = None

        with pytest.raises(Exception):
            molecule.parameterize(FORCEFIELD_NAME)

    def test_good_init_parameterization(self):
        """
        It checks that a call to the parameterize function with a Molecule
        successfully initialized does not raise any Exception.
        """
        FORCEFIELD_NAME = 'openff_unconstrained-1.1.1.offxml'
        LIGAND_PATH = SET_OF_LIGAND_PATHS[0]
        ligand_path = get_data_file_path(LIGAND_PATH)

        molecule = Molecule(ligand_path)
        molecule.parameterize(FORCEFIELD_NAME)
