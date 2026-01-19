"""
Source adapters for the Grant Guide scraper.
"""
from .base import BaseSourceAdapter
from .dtic import DTICAdapter
from .dsbd import DSBDAdapter
from .nyda import NYDAAdapter
from .tia import TIAAdapter
from .idc import IDCAdapter
from .nef import NEFAdapter
from .sefa import SEFAAdapter
from .gep import GEPAdapter
from .ecdc import ECDCAdapter
from .dedat import DEDATAdapter
from .seta import ServicesSETAAdapter, HWSETAAdapter, CETAAdapter
from .sab import SABFoundationAdapter
from .aecf import AECFAdapter
from .tef import TEFAdapter

__all__ = [
    'BaseSourceAdapter',
    'DTICAdapter',
    'DSBDAdapter',
    'NYDAAdapter',
    'TIAAdapter',
    'IDCAdapter',
    'NEFAdapter',
    'SEFAAdapter',
    'GEPAdapter',
    'ECDCAdapter',
    'DEDATAdapter',
    'ServicesSETAAdapter',
    'HWSETAAdapter',
    'CETAAdapter',
    'SABFoundationAdapter',
    'AECFAdapter',
    'TEFAdapter',
]
