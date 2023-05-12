"""
This module will contain code necessary to preprocess and prepare 
offerwall data for ingestion by our database.
"""

import pandas as pd
import numpy as np

def clean_ayet(ayet_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Ayet offerwall.

    Parameters
    ----------
        ayet_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Ayet offerwall.

    Returns
    -------
        clean_ayet_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Ayet offerwall.
    """

    keyword_list = ['Multiple rewards']
    # Add proper description from the 'Additonal' column instead of
    # a generic 'Mulitple rewards' description.
    for index,row in ayet_dataframe.iterrows():
        if row['Description'] in keyword_list:
            row['Description'] = row['Additional']

    # Drop unneeded columns from the dataframe.
    ayet_dataframe = ayet_dataframe.drop(['offerLow','Additional','Difficulty','Ignore3'], axis=1)

    # Drop rows containing 'None' values as these rows represent
    # duplicate data.
    ayet_dataframe = ayet_dataframe.dropna()

    return ayet_dataframe

def clean_revu(revu_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Revenue Universe offerwall.

    Parameters
    ----------
        revu_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Revenue Universe offerwall.

    Returns
    -------
        clean_revu_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Revenue Universe offerwall.
    """
    return

def clean_adgem(adgem_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Adgem offerwall.

    Parameters
    ----------
        adgem_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Adgem offerwall.

    Returns
    -------
        clean_adgem_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Adgem offerwall.
    """
    return

def clean_toro(toro_dataframe):
    """
    This function cleans and prepares
    the informations retrieve from the
    Offertoro offerwall.

    Parameters
    ----------
        toro_dataframe: `pandas.DataFrame`
            A pandas Dataframe containing offer information from the
            Offertoro offerwall.

    Returns
    -------
        clean_toro_dataframe: `pandas.DataFrame`
            A pandas DataFrame containing the cleaned and processed
            offer information from the Offertoro offerwall.
    """
    return