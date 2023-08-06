# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tools for colors"""
import colorcet as cc
from kaleidoscope.colors.cmap import cmap_to_plotly

# The Blue->Magenta->Yellow sequential color map from ColorCet for plotly
BMY_PLOTLY = cmap_to_plotly(cc.cm.bmy)

# Dark2 from colorbrewer
DARK2 = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a",
         "#66a61e", "#e6ab02", "#a6761d", "#666666"]
