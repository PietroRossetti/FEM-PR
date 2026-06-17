from numpy import ndarray
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod


class ElementState():

    eleDeformationsCommitted: ndarray
    elementForcesCommitted: ndarray

    eleDeformationsTrial: ndarray
    eleForcesTrial: ndarray