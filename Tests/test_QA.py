"""
Main Testing Framework to confirm Data Quality
"""

import pandas as pd
import pytest
import os
from dotenv import load_dotenv
import sys
sys.path.append('./Functions')
import adgem_info
import ayet_info
import offertoro_info
import revu_info
import offer_cleanup

#Load environment variables
load_dotenv()
#The environment variables should be present in your CI/CD pipeline
#and/or server side as well.

@pytest.mark.usefixtures("qa_ayet")
class Test_QA_AYET:
    """
    Test suite for the Ayet offerwall.

    This test suite is designed to test the expected data structure
    resulting from the `ayet_info.py` file.
    """

    def test_description_replacement(self, qa_ayet):
        """
        Tests if the description is replaced with the title when the value
        is 'Multiple rewards'
        """
        clean_ayet = offer_cleanup.clean_ayet(qa_ayet)
        assert clean_ayet.loc[2, 'Description'] == 'Additional 2'

    def test_columns_dropped(self, qa_ayet):
        """
        Tests that unneeded columns were dropped and are not present in the dataframe.
        """
        dropped_cols = ['offerLow', 'Additional', 'Difficulty', 'Ignore3']
        clean_ayet = offer_cleanup.clean_ayet(qa_ayet)
        assert dropped_cols not in clean_ayet.columns.values.tolist()

    def test_no_null_values(self, qa_ayet):
        """
        Tests that no null values are present in the dataframe.
        """
        clean_ayet = offer_cleanup.clean_ayet(qa_ayet)
        assert not clean_ayet.isnull().values.any()

@pytest.mark.usefixtures("qa_adgem")
class Test_QA_ADGEM:
    """
    Test suite for the Ayet offerwall.

    This test suite is designed to test the expected data structure
    resulting from the `ayet_info.py` file.
    """

    def test_dropped_duplicates(self, qa_adgem):
        """
        Tests if duplicate values were succesfully removed.
        """
        clean_adgem = offer_cleanup.clean_adgem(qa_adgem)
        assert not clean_adgem.duplicated().any()

    def test_commas_removed(self, qa_adgem):
        """
        Tests that unneeded commas were removed from the `offer_amount` column.
        """
        clean_adgem = offer_cleanup.clean_adgem(qa_adgem)
        assert not clean_adgem['offer_amount'].str.contains(',').any()

    def test_only_numeric_values(self, qa_adgem):
        """
        Tests that only numeric values are in the `offer_amount` column.
        """
        clean_adgem = offer_cleanup.clean_adgem(qa_adgem)
        assert clean_adgem['offer_amount'].str.isnumeric().all()