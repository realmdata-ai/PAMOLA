"""
PAMOLA.CORE - Privacy-Preserving AI Data Processors
Part of PAMOLA.CORE, the open-source privacy-engineering library of the PAMOLA ecosystem.

Copyright (c) 2024-2026 Realm Inveo Inc. (REALMDATA)
Licensed under the MIT License; see the LICENSE file or
https://github.com/realmdata-ai/PAMOLA/blob/main/LICENSE

Module: Attack Simulation
This module provides an abstract base class for attack simulation feature
in PAMOLA.CORE. It defines the general structure and required methods for
implementing specific attack simulation

NOTE: This is a template and will be updated as development progresses.

Author: Realm Inveo Inc.
"""

from abc import ABC, abstractmethod


class AttackInitialization(ABC):
    """
    Abstract base class for attack simulation in PAMOLA.CORE.
    This class extends BaseProcessor and declare methods used for attack simulation.
    """

    @abstractmethod
    def preprocess_data(self, data1, data2):
        """
        Data preprocessing: Use TF-ID to convert all string elements of data1 and data2 to numbers

        Parameters
        -----------
        data1: First dataset
        data_test: Second dataset

        Returns
        -----------
        data1_final: The dataset contains numeric values corresponding to data1
        data2_final: The dataset contains numeric values corresponding to data2
        """

        pass

    @abstractmethod
    def process(self, data):
        """
        Process the input data.

        Parameters
        -----------
        data : Any
            The input data to be processed.

        Returns
        --------
        Processed data, transformed according to the specific processor logic.
        """
        pass
