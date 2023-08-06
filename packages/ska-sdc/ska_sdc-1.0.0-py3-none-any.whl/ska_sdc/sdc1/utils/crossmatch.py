import logging

import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

from ska_sdc.common.models.exceptions import BadConfigException
from ska_sdc.sdc1.dc_defns import MODE_CENTR, MODE_CORE


def crossmatch_kdtree(sub_cat_df, truth_cat_df, mode):
    """
    Construct and query a k-dimensional tree for sources within 5 sigma of the core
    position.

    Yield a DataFrame with all the data for both submission and truth sources.
    """
    # Will use new 0-indexed lists of coords for matches, reset indices of catalogue
    # DataFrames so that indices match these lists
    truth_cat_df = truth_cat_df.reset_index(drop=True)
    sub_cat_df = sub_cat_df.reset_index(drop=True)

    truth_cat_idx_arr = truth_cat_df["id"].values
    sub_cat_idx_arr = sub_cat_df["id"].values

    truth_cat_racore_arr = truth_cat_df["ra_core"].values
    truth_cat_deccore_arr = truth_cat_df["dec_core"].values
    truth_cat_racent_arr = truth_cat_df["ra_cent"].values
    truth_cat_deccent_arr = truth_cat_df["dec_cent"].values
    truth_cat_flux_arr = truth_cat_df["flux"].values
    truth_cat_corefrac_arr = truth_cat_df["core_frac"].values
    truth_cat_bmaj_arr = truth_cat_df["b_maj"].values
    truth_cat_bmin_arr = truth_cat_df["b_min"].values
    truth_cat_pa_arr = truth_cat_df["pa"].values
    truth_cat_sizeid_arr = truth_cat_df["size"].values
    truth_cat_class_arr = truth_cat_df["class"].values
    truth_cat_aflux_arr = truth_cat_df["a_flux"].values
    truth_cat_size_arr = truth_cat_df["conv_size"].values

    sub_cat_racore_arr = sub_cat_df["ra_core"].values
    sub_cat_deccore_arr = sub_cat_df["dec_core"].values
    sub_cat_racent_arr = sub_cat_df["ra_cent"].values
    sub_cat_deccent_arr = sub_cat_df["dec_cent"].values
    sub_cat_flux_arr = sub_cat_df["flux"].values
    sub_cat_corefrac_arr = sub_cat_df["core_frac"].values
    sub_cat_bmaj_arr = sub_cat_df["b_maj"].values
    sub_cat_bmin_arr = sub_cat_df["b_min"].values
    sub_cat_pa_arr = sub_cat_df["pa"].values
    sub_cat_sizeid_arr = sub_cat_df["size"].values
    sub_cat_class_arr = sub_cat_df["class"].values
    sub_cat_aflux_arr = sub_cat_df["a_flux"].values
    sub_cat_size_arr = sub_cat_df["conv_size"].values

    if mode == MODE_CORE:
        sub_coord_arr = np.array(list(zip(sub_cat_racore_arr, sub_cat_deccore_arr,)))
        truth_coord_arr = np.array(
            list(zip(truth_cat_racore_arr, truth_cat_deccore_arr,))
        )
    elif mode == MODE_CENTR:
        sub_coord_arr = np.array(list(zip(sub_cat_racent_arr, sub_cat_deccent_arr,)))
        truth_coord_arr = np.array(
            list(zip(truth_cat_racent_arr, truth_cat_deccent_arr,))
        )
    else:
        err_msg = (
            "Unknown mode, use {}, {} "
            "for core and centroid position modes respectively"
        ).format(MODE_CORE, MODE_CENTR)
        logging.error(err_msg)
        raise BadConfigException(err_msg)

    # Construct k-d tree
    point_kdtree = KDTree(truth_coord_arr)

    # Query for conv_size around submitted values
    # TODO: Consider widening this search?
    size_series = sub_cat_df["conv_size"].astype("float64") * (1 / 3600)
    size_arr = size_series.values

    # Instantiate output arrays (used to construct match DataFrame)
    sub_idx_list = []
    sub_racore_list = []
    sub_deccore_list = []
    sub_racent_list = []
    sub_deccent_list = []
    sub_flux_list = []
    sub_corefrac_list = []
    sub_bmaj_list = []
    sub_bmin_list = []
    sub_pa_list = []
    sub_sizeid_list = []
    sub_class_list = []
    sub_aflux_list = []
    sub_size_list = []

    truth_idx_list = []
    truth_racore_list = []
    truth_deccore_list = []
    truth_racent_list = []
    truth_deccent_list = []
    truth_flux_list = []
    truth_corefrac_list = []
    truth_bmaj_list = []
    truth_bmin_list = []
    truth_pa_list = []
    truth_sizeid_list = []
    truth_class_list = []
    truth_aflux_list = []
    truth_size_list = []

    if len(sub_coord_arr > 0):
        for sub_index, (center, group) in enumerate(
            zip(sub_coord_arr, point_kdtree.query_radius(sub_coord_arr, r=size_arr))
        ):

            for match_index in group:

                sub_idx_list.append(sub_cat_idx_arr[sub_index])
                sub_racore_list.append(sub_cat_racore_arr[sub_index])
                sub_deccore_list.append(sub_cat_deccore_arr[sub_index])
                sub_racent_list.append(sub_cat_racent_arr[sub_index])
                sub_deccent_list.append(sub_cat_deccent_arr[sub_index])
                sub_flux_list.append(sub_cat_flux_arr[sub_index])
                sub_corefrac_list.append(sub_cat_corefrac_arr[sub_index])
                sub_bmaj_list.append(sub_cat_bmaj_arr[sub_index])
                sub_bmin_list.append(sub_cat_bmin_arr[sub_index])
                sub_pa_list.append(sub_cat_pa_arr[sub_index])
                sub_sizeid_list.append(sub_cat_sizeid_arr[sub_index])
                sub_class_list.append(sub_cat_class_arr[sub_index])
                sub_aflux_list.append(sub_cat_aflux_arr[sub_index])
                sub_size_list.append(sub_cat_size_arr[sub_index])

                truth_idx_list.append(truth_cat_idx_arr[match_index])
                truth_racore_list.append(truth_cat_racore_arr[match_index])
                truth_deccore_list.append(truth_cat_deccore_arr[match_index])
                truth_racent_list.append(truth_cat_racent_arr[match_index])
                truth_deccent_list.append(truth_cat_deccent_arr[match_index])
                truth_flux_list.append(truth_cat_flux_arr[match_index])
                truth_corefrac_list.append(truth_cat_corefrac_arr[match_index])
                truth_bmaj_list.append(truth_cat_bmaj_arr[match_index])
                truth_bmin_list.append(truth_cat_bmin_arr[match_index])
                truth_pa_list.append(truth_cat_pa_arr[match_index])
                truth_sizeid_list.append(truth_cat_sizeid_arr[match_index])
                truth_class_list.append(truth_cat_class_arr[match_index])
                truth_aflux_list.append(truth_cat_aflux_arr[match_index])
                truth_size_list.append(truth_cat_size_arr[match_index])

    match_df = pd.DataFrame(
        {
            "id": sub_idx_list,
            "ra_core": sub_racore_list,
            "dec_core": sub_deccore_list,
            "ra_cent": sub_racent_list,
            "dec_cent": sub_deccent_list,
            "flux": sub_flux_list,
            "core_frac": sub_corefrac_list,
            "b_maj": sub_bmaj_list,
            "b_min": sub_bmin_list,
            "pa": sub_pa_list,
            "size_id": sub_sizeid_list,
            "class": sub_class_list,
            "a_flux": sub_aflux_list,
            "conv_size": sub_size_list,
            "id_t": truth_idx_list,
            "ra_core_t": truth_racore_list,
            "dec_core_t": truth_deccore_list,
            "ra_cent_t": truth_racent_list,
            "dec_cent_t": truth_deccent_list,
            "flux_t": truth_flux_list,
            "core_frac_t": truth_corefrac_list,
            "b_maj_t": truth_bmaj_list,
            "b_min_t": truth_bmin_list,
            "pa_t": truth_pa_list,
            "size_id_t": truth_sizeid_list,
            "class_t": truth_class_list,
            "a_flux_t": truth_aflux_list,
            "conv_size_t": truth_size_list,
        }
    )

    return match_df
