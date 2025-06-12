import os
import sys
import importlib
import math
from math import log, sqrt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from text import Text
from collections import defaultdict #comment
import spacy  # for LatinCy
import csv  # for hashtable of Diderich -> lexical sophistication
import matplotlib.font_manager as fm
import time
import numpy as np
from scipy.signal import savgol_filter
from pymongo import MongoClient

from fastapi import APIRouter, WebSocket, Request, File, Form, UploadFile, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime
import DefinitionTools
from pathlib import Path
import MongoDefinitionTools
from MongoDefinitionTools import db, dict_db


'''
Files:
Text files -> Text class, get_text().book
Working File -> FastBridgeApp\Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310.xlsx
Latin Dictionary -> FastBridgeApp\bridge_latin_dictionary.csv
Diederich 300,1500 -> FastBridgeApp\Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020_BridgeImport.csv
DCC -> FastBridgeApp\Bridge-Vocab-Latin-List-DCC.csv
'''

# Get the directory containing the current script.
current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)#FastBridgeApp

# Decorators
# times the method you give to it, apply using @timer_decorator above method
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return result, elapsed_time
    return wrapper


def round_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, tuple):
            return tuple(round(val, 2) if isinstance(val, (int, float)) else val for val in result)
        elif isinstance(result, (int, float)):
            return round(result, 2)
        else:
            return result
    return wrapper


# Define FontProperties
prop = fm.FontProperties(family='serif', size=9)

# LatinCy
# pip install https://huggingface.co/latincy/la_core_web_trf/resolve/main/la_core_web_trf-any-py3-none-any.whl

# Seaborn Themes
title_font = {'fontname': 'serif', 'size': '13', 'color': 'black', 'weight': 'normal',
              'verticalalignment': 'bottom'}  # This is for the title properties
axis_font = {'fontname': 'serif', 'size': '11'}  # This is for the axis labels
colorblind_palette = ['#E69F00', '#56B4E9', '#009E73',
                      '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

# Dictionary File


@timer_decorator
def mg_get_latin_dictionary(db):
    word_dictionary = {}
    cursor = db.bridge_latin_dictionary.find()
    for row in cursor:
        if 'TITLE' in row:
            word_dictionary[row['TITLE']] = row
    return word_dictionary

@timer_decorator
def mg_get_diederich1500(db, collection_name):
    diederich1500 = {}
    cursor = db[collection_name].find()
    for row in cursor:
        diederich1500[row['head_word']] = row
    return diederich1500

@timer_decorator
def mg_get_dcc(db, collection_name):
    dcc = set()
    cursor = db[collection_name].find()
    for row in cursor:
        dcc.add(row['head_word'])
    return dcc

@timer_decorator
def mg_get_diederich300(db):
    diederich300 = set()
    cursor = db.diederich300.find()
    count = 0
    for row in cursor:
        if count <= 306:
            diederich300.add(row['TITLE'])
            count += 1
        else:
            break
    return diederich300

@timer_decorator
def mg_get_diederich(collection_name):
    diederich300 = set()
    diederich1500 = set()
    cursor = db[collection_name].find()
    for row in cursor:
        if row['counter'] <= 306:
            diederich300.add(row['head_word'])
        diederich1500.add(row['head_word'])
    return diederich300, diederich1500

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def get_text(form_request: str, language: str):
    """
    Imports the text that was requested. This way, we only load the texts that the user is requesting each time.
    """
    return importlib.import_module(f'data.{language}.{form_request}')  # point to the data folder

#used for getting slices of each text
def get_slice(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words
    mongo_v = ['PVMEX', 'EXPOLIO/2', 'DONO', 'SOLEO', 'ITALVS/A', 'TVM', 'TV', 'DO', 'MEVS', 'OMNIS', 'EXPLICO', 'DELICIA/1', 'SOLEO', 'ET/2', 'QVALISCVMQVE/2', 'PASSER', 'IVPPITER/N', 'NVGAE', 'QVARE/1', 'PATRONA', 'SINVS', 'APPETO', 'LIBELLVS', 'MODO/1', 'NAMQVE', 'CORNELIVS/N', 'PVELLA', 'MEVS', 'DOCTVS', 'HIC/1', 'QVI/1', 'QVI/1', 'PVTO', 'IAM', 'SVM/1', 'TRES', 'NOVVS', 'LIBELLVS', 'TV', 'QVIS/1', 'ALIQVIS', 'LEPIDVS', 'LABORIOSVS', 'O', 'VNVS', 'VIRGO', 'CVM/3', 'HABEO', 'QVI/1', 'ET/2', 'CHARTA', 'QVISQVIS/2', 'MVLTVM/2', 'PERENNIS', 'DIGITVS', 'TV', 'ARIDVS', 'AEVVM', 'AVDEO', 'SVM/1', 'VNVS', 'MANEO', 'SAECVLVM', 'CVM/2', 'SVVS', 'POSSVM/1', 'PRIMVS', 'ACQVIESCO', 'CARVS', 'ACER/2', 'PVELLA', 'IOCOR', 'LVDO', 'TAM', 'GRATVS', 'SVM/1', 'TAM', 'TV', 'QVI/1', 'SOLVO', 'DIV', 'CREDO', 'TRISTIS', 'CVRA', 'VENVSTVS', 'MORSVS', 'DESIDERIVM', 'MEVS', 'IN', 'SVM/1', 'ET/2', 'CVM/2', 'CVPIDO/N', 'ET/2', 'ET/2', 'INCITO/1', 'CVM/3', 'LVDO', 'EGO', 'QVANTVM/3', 'VENVS/N', 'QVAM/1', 'PERNIX', 'AVREOLVS', 'LEVO/1', 'GRAVIS', 'FERO', 'LVGEO', 'PVELLA', 'MALVM/2', 'SVM/1', 'O', 'TENEO', 'NITENS', 'NESCIOQVIS', 'QVI/1', 'DOLOR', 'LIBET', 'SOLACIOLVM', 'ZONA', 'SICVT/1', 'NEGO', 'QVE', 'ANIMVS', 'ET/2', 'IPSE', 'ARDOR', 'MEVS', 'QVE', 'MEVS', 'MELLITVS', 'IPSE', 'SVVS', 'NOSCO', 'NEC/2', 'GREMIVM', 'REDEO/1', 'QVISQVAM', 'TENEBRAE', 'ORCVS/N', 'BELLVS', 'DEVORO', 'NAM', 'RVBEO', 'HIC/1', 'PROPONTIS/N', 'VE', 'HIC/1', 'EX', 'HERVS', 'VENIO', 'VSQVE', 'PANDO/2', 'VOLO/3', 'VERSVS/1', 'LASERPITIFER', 'SIDVS', 'SACER', 'CATVLLVS/N', 'CVRIOSVS', 'LINGVA', 'TVM', 'NEC/2', 'MENS', 'VALEO', 'ROGO', 'QVIS/1', 'AT/2', 'ANVS/2', 'IBERVS/A', 'SVM/1', 'QVI/1', 'AES', 'HOMO', 'GRABATVS', 'EXTER', 'PVELLA', 'MODO/1', 'CIRCVMSILIO', 'ILLVC', 'ILLE', 'NEGO', 'VBI/1', 'EDO/1', 'AMASTRIS/N', 'LITORALIS', 'HIC/1', 'SENEO', 'MEVS', 'CENTVM', 'ILLE', 'MALVS/3', 'SCORTVM', 'NIHIL', 'QVARE/1', 'BASIATIO', 'SEPVLCRVM', 'SVM/1', 'ILLE', 'NON', 'ROGO', 'CATVLLVS/N', 'MOS', 'TVVS', 'SVM/1', 'OS/1', 'SVAVIOR', 'HOMO', 'NOS', 'IN', 'IS', 'RESPONDEO', 'NEQVE', 'SVI/1', 'DECET', 'SVM/1', 'SED', 'PER', 'EGO', 'QVI/1', 'EGO', 'VE', 'PARTHVS/A', 'NILVS/N', 'HYRCANVS/A', 'QVE', 'FERO', 'SIMVL/1', 'SVM/1', 'SVM/1', 'ILLE', 'HVC', 'QVI/1', 'ISTE', 'CYTORIVS/A', 'COMA', 'TVVS', 'ET/2', 'PHASELVS', 'SVI/1', 'LIMPIDVS', 'HIC/1', 'SVM/1', 'DEINDE', 'CENTVM', 'DEINDE', 'SECVNDVS/1', 'TV', 'NESCIOQVIS', 'AC/1', 'FACIO', 'NOS', 'QVAM/1', 'BASIVM', 'VESANVS', 'QVANTVM/3', 'NVLLVS', 'FIO', 'QVI/1', 'IAM', 'QVOQVE', 'AMO', 'DICO/2', 'EGO', 'TRECENTI', 'QVE', 'MATER', 'EGO', 'FORVM/1', 'HVC', 'QVOMODO/1', 'PROSVM/1', 'VNCTVS/2', 'COHORS', 'SVM/1', 'VT/4', 'COLLOCO', 'EGO', 'COMMODO/1', 'ISTE', 'EGO', 'VTRVM', 'VT/4', 'SIVE/1', 'VE', 'COLORO', 'QVE', 'CAELES/1', 'VISO', 'MODO/1', 'MALE', 'QVI/1', 'MEVS', 'CELER', 'NEQVE', 'HADRIATICVS/A', 'PHASELVS', 'ORIGO', 'IMPOTENS', 'AVRA', 'FRETVM', 'VOTVM', 'ET/2', 'VIVO', 'OCCIDO/1', 'BREVIS', 'DORMIO', 'DEINDE', 'MVLTVS', 'CONTVRBO/2', 'POSSVM/1', 'NAM', 'PVDEO', 'PERAEQVE', 'TREMVLVS/3', 'ISTE', 'QVIS/2', 'IACEO', 'TACEO', 'POSSVM/1', 'VIDEO', 'SOL', 'TV', 'VIDEO', 'NVNC', 'MILLE', 'TV', 'NARRO', 'QVANTVM/3', 'SCORTILLVM', 'TVM', 'LAETVS/2', 'CAPVT', 'DICO/2', 'FACIO', 'INQVIO', 'NON', 'AD/2', 'INQVIO', 'EGO', 'HABEO', 'FVGIO', 'PARO/2', 'MOLESTVS', 'VIVO', 'INDVS/A', 'SEPTEMGEMINVS', 'NVNTIO', 'MORIOR', 'NAM', 'AT/2', 'VNDE/1', 'SVM/1', 'SIBILVM', 'IN', 'AEQVOR', 'SVM/1', 'CVM/3', 'SVI/1', 'DEDICO/1', 'QVE', 'PERPETVVS', 'VNVS', 'NON', 'NIHIL', 'ET/2', 'VALEO', 'ILLIC/1', 'QVISQVIS/2', 'AMOR', 'EGO', 'VIDEO', 'MVLTVS', 'SVPER/2', 'TV', 'CVM/3', 'FVLGEO', 'TV', 'IMPOTENS', 'NOLO', 'IAM', 'OBDVRO', 'TV', 'NVLLVS', 'QVIS/1', 'MANEO', 'ANTESTO', 'PENATES/N', 'VENIO', 'INCOLVMIS', 'QVE', 'QVE', 'SVM/1', 'OTIOSVS', 'VIDEO', 'SVM/1', 'EGO', 'EGO', 'NAM', 'QVI/1', 'EGO', 'MALE', 'EOVS/A', 'AEQVOR', 'NON', 'MAGNVS', 'VIVO', 'PASSER', 'HOMO', 'QVI/1', 'NVNC', 'MOVEO', 'OMNIS', 'O', 'TRABS', 'IMPETVS', 'SIVE/1', 'DICO/2', 'PALMVLA', 'INCIDO/1', 'PES', 'AD/2', 'RVMOR', 'OCCIDO/1', 'CVM/3', 'EGO', 'SCIO', 'DELICIA/1', 'CATVLLVS/N', 'TV', 'LESBIA/N', 'SVM/1', 'NVMERVS', 'ORACVLVM', 'VETVS', 'DESINO', 'ET/2', 'PERDITVS', 'NEC/2', 'CVM/3', 'QVIS/1', 'BEATVS', 'AD/2', 'QVISNAM', 'QVI/1', 'PILVM', 'ILLIC/2', 'TAM', 'MALIGNVS', 'PARO/2', 'RECTVS', 'QVAESO', 'SERAPIS/N', 'RATIO', 'SVI/1', 'ET/2', 'FVRIVS/N', 'CATVLLVS/N', 'VNDA', 'ARABES/N', 'IN', 'BRITANNVS/A', 'OMNIS', 'DICTVM', 'SVVS', 'VALEO', 'MOECHVS', 'PVELLA', 'BENE', 'SED', 'NEGO', 'FACTVM', 'PHASELVS', 'OPVS/2', 'CYCLADES/N', 'QVE', 'POST/2', 'NAM', 'SVM/1', 'COGNITVS/2', 'IMBVO', 'IVPPITER/N', 'SECVNDVS/1', 'IN', 'NOS', 'LVX', 'DEINDE', 'CENTVM', 'VSQVE', 'QVIS/2', 'NE/4', 'NISI', 'ILLEPIDVS', 'TACITVS', 'SERTVM', 'ARGVTATIO', 'TV', 'AD/2', 'BATTVS/N', 'QVAM/1', 'NOX', 'ET/2', 'ET/2', 'QVI/1', 'PERNVMERO/1', 'QVONDAM', 'MVLTVS', 'SED', 'DOLEO', 'PERFERO', 'SCELESTVS', 'QVIS/1', 'VENIO', 'DOMVS', 'AD/2', 'VT/4', 'VARVS/N', 'SANE', 'ILLEPIDVS', 'VT/4', 'INCIDO/1', 'NEC/2', 'AT/2', 'QVI/1', 'AD/2', 'MALVS/3', 'LECTICA', 'AT/2', 'QVI/1', 'VETVS', 'ILLE', 'DEFERO', 'SVI/1', 'AB', 'MALE', 'SIVE/1', 'LITVS/2', 'RHODVS/N', 'VOLO/2', 'BVXIFER', 'IN', 'PER', 'SIVE/1', 'NEQVE', 'LAEVA/3', 'QVIES', 'AMO', 'NVNC', 'SED', 'SENEX/1', 'ET/2', 'VNVS', 'NE/4', 'VOLO/3', 'LECTVS/1', 'INEPTIAE', 'LEPIDVS', 'SVPER/2', 'IVPPITER/N', 'MVLTVS', 'TAM', 'FASCINO', 'QVI/1', 'CANDIDVS', 'VIVO', 'TV', 'EGO', 'VARIVS', 'SVM/1', 'VT/4', 'EGO', 'DICO/2', 'IS', 'NEGLIGENS', 'IN', 'HIC/1', 'VOLVNTAS', 'TAM', 'SVVS', 'ILLE', 'ITER', 'SVM/1', 'BELLVS', 'PASSER', 'FLEO', 'MISELLVS', 'VE', 'SINVS', 'VLTIMVS', 'CACVMEN', 'VTERQVE', 'DEVS', 'GEMELLVS', 'INVIDEO', 'TVVS', 'FEBRICVLOSVS', 'NEC/2', 'IACEO', 'NEQVIQVAM', 'CVBILE', 'DICO/2', 'NAM', 'VERVM/4', 'CVR/1', 'LATVS/1', 'NEC/2', 'TVVS', 'QVAERO', 'INEPTIO', 'DVCO', 'VERE', 'PVELLA', 'AT/2', 'NVNTIVS/1', 'VT/4', 'O', 'SVVS', 'ET/2', 'EGO', 'SVI/1', 'TAMEN', 'SVM/1', 'INCIDO/1', 'ILLIC/2', 'COLLVM', 'ISTE', 'VERVM/4', 'ILLE', 'TAM', 'PENETRO', 'HORRIBILIS', 'QVI/1', 'AD/2', 'QVAM/1', 'VSQVE', 'QVE', 'NOBILIS/2', 'AIO', 'INDE', 'SIVE/1', 'MARE', 'NOVVS', 'DO', 'DEINDE', 'TANTVM/2', 'INELEGANS', 'OLIVVM', 'INAMBVLATIO', 'TAM', 'HABEO', 'QVE', 'VOCO', 'CYRENAE/N', 'HOMO', 'BASIO', 'SATIS/2', 'FVRTIVVS', 'NEC/2', 'NEC/2', 'MISER', 'PEREO/1', 'SOL', 'TV', 'NVNC', 'FVLGEO', 'NVNC', 'VITA', 'LABELLVM/2', 'VAE', 'VERANIVS/N', 'AMICVS/2', 'COLLVM', 'EX', 'NEC/2', 'INQVIO', 'NASCOR', 'COMPARO/2', 'NEC/2', 'NVLLVS', 'HIC/2', 'INQVIO', 'CATVLLVS/N', 'NON', 'LONGVS', 'ALTVS', 'TENTO', 'QVE', 'PASSER', 'PIPIO/2', 'NAVIS', 'NEQVEO', 'INSVLA', 'LINTEVM', 'ET/2', 'RECONDITVS', 'AESTIMO', 'SEMEL', 'AS', 'MILLE', 'FACIO', 'SVM/1', 'TACEO', 'POSSVM/1', 'HIC/1', 'DILIGO/3', 'CLAMO', 'ET/2', 'CVM/3', 'CATVLLVS/N', 'QVO/2', 'PVELLA', 'PVELLA', 'ADEO/1', 'QVIS/1', 'BASIO', 'TVVS', 'EX', 'O', 'APPLICO', 'AVDIO', 'MEVS', 'AMOR', 'VIDEO', 'REPENTE', 'IPSE', 'SVM/1', 'PVELLA', 'SVM/1', 'VT/4', 'IRRVMATOR', 'SVM/1', 'FRANGO', 'PES', 'MEVS', 'INSVLSVS', 'SACAE/N', 'ALPES/N', 'RHENVS/N', 'MONVMENTVM', 'OCVLVS', 'MATER', 'SOLVS', 'O', 'TVRGIDVLVS', 'OCELLVS', 'HOSPES', 'AIO', 'PRAETEREO/1', 'ANTEA', 'SILVA', 'IN', 'SVM/1', 'TOT', 'DEXTERA', 'FERO', 'VLLVS', 'TV', 'REDEO/1', 'AVT', 'FRAGRO', 'BONVM', 'TVVS', 'MALVS/3', 'AMO', 'AMO', 'VOLO/3', 'QVIS/1', 'BEATVS', 'VISO', 'QVE', 'VE', 'NEQVE', 'VENIO', 'HABEO', 'NIHIL', 'NEQVE', 'BITHYNIA/N', 'QVISQVAM', 'REFERO', 'FACIO', 'PROVINCIA', 'IN', 'MODO/1', 'CINNA/N', 'AN', 'QVAM/1', 'COMES', 'SAGITTIFER/2', 'SIVE/1', 'SIVE/1', 'VLTIMVS', 'SODALIS/1', 'BENE', 'AD/2', 'LICET/1', 'MOLLIS', 'SIVE/1', 'DELICIA/1', 'AVFERO', 'NATO', 'SVM/1', 'MINAX', 'ET/2', 'TVVS', 'FACIO', 'SVM/1', 'QVE', 'NOX', 'DEINDE', 'BASIVM', 'MILLE', 'CAELVM/1', 'AC/1', 'QVOT/1', 'AESTVOSVS', 'IBI', 'TV', 'FVGIO', 'MISER', 'OBSTINATVS', 'TV', 'BELLVS', 'MORDEO', 'OBDVRO', 'QVE', 'NATIO/1', 'BEATVS', 'PRAETOR', 'COHORS', 'CERTE', 'NON', 'HOMO', 'EGO', 'PAVLVM/2', 'PARO/2', 'VTOR', 'RESONO/1', 'GRADIOR', 'PAVCI', 'BONVS', 'CAESAR/N', 'GALLICVS/A', 'PER', 'VOS', 'TENEBRICOSVS', 'ILLE', 'NVNC', 'QVI/1', 'VLLVS', 'PONTICVS/A', 'VOCO', 'LACVS', 'GEMELLVS', 'LESBIA/N', 'OMNIS', 'SEVERVS', 'CVM/3', 'FLAVIVS/N', 'FATEOR', 'NON', 'TACEO', 'MAGNVS', 'LIBYS/N', 'INTER', 'TV', 'VENTITO', 'NOS', 'IOCOSVS', 'VOLO/3', 'SECTOR/2', 'NEC/2', 'CATVLLVS/N', 'QVIS/1', 'MEVS', 'TV', 'VNANIMVS', 'FACTVM', 'LOCVS', 'OCVLVS', 'EGO', 'SERMO', 'VNVS', 'POSSVM/1', 'TV', 'QVIS/1', 'SVM/1', 'AVRELIVS/N', 'TRANS/2', 'QVICVMQVE/1', 'MEVS', 'EO/1', 'MALVS/3', 'TVVS', 'PASSER', 'OPERA', 'VIDEO', 'PVELLA', 'PALMVLA', 'NEGO', 'HORRIDVS', 'THRACIVS/A', 'TRVX', 'IVGVM', 'COMATVS', 'SAEPE', 'CYTORVS/N', 'TV', 'AB', 'ATQVE/1', 'POSSVM/1', 'MILLE', 'ALTER', 'MILLE', 'BASIVM', 'HIC/1', 'ATTRITVS/2', 'QVATIO', 'QVE', 'QVE', 'EFFVTVO', 'MALVM/1', 'SATIS/2', 'CANDIDVS', 'NOLO', 'REQVIRO', 'NE/2', 'SVM/1', 'NON', 'INVENVSTVS', 'QVIS/1', 'IAM', 'CVR/1', 'QVI/1', 'OCTO', 'BEATVS', 'NEC/2', 'MEVS', 'SIVE/1', 'LITVS/2', 'QVI/1', 'PARO/2', 'CVM/2', 'MVLTVM/2', 'AMO', 'DOMINA', 'EGO', 'LOQVOR', 'PONTICVS/A', 'ET/2', 'SVM/1', 'STO', 'SIMVL/1', 'CASTOR/N', 'PRIVS', 'CASTOR/N', 'SOL', 'CVM/3', 'ALTER', 'SCIO', 'SVM/1', 'ATQVE/1', 'VIDVVS', 'NOX', 'SYRIVS/A', 'PVLVINVS', 'QVE', 'DICO/2', 'QVE', 'ARENA', 'AVT', 'AMOR', 'DVCO', 'ILLE', 'QVI/1', 'OBDVRO', 'NEC/2', 'NEC/2', 'INVITVS', 'QVIS/1', 'SVM/1', 'TV', 'FRATER', 'DESTINATVS', 'IVCVNDVS', 'OMNIS', 'DVCO', 'EGO', 'PRAESERTIM', 'PRAETOR', 'QVOD/1', 'POSSVM/1', 'HIC/2', 'CINAEDVS/2', 'VOLO/3', 'MANEO', 'PVELLA', 'GAIVS/N', 'ET/2', 'TVNDO', 'PVELLA', 'TRECENTI', 'MARRVCINVS/A', 'TANGO', 'AMOR', 'LINTEVM', 'NON', 'MANVS/1', 'FVGIO', 'POLLIO/N', 'QVI/1', 'SINISTER', 'EGO', 'IDENTIDEM', 'CADO', 'VTOR', 'IOCVS', 'ATQVE/1', 'TOLLO', 'AMO', 'VELVT/1', 'COMPLECTOR', 'FRATER', 'MEVS', 'ARATRVM', 'SVM/1', 'PRAETEREO/1', 'RES', 'QVI/1', 'VINVM', 'NON', 'BELLVS', 'SVM/1', 'NVLLVS', 'TENEO', 'NEC/2', 'ILLE', 'NEGLIGENS', 'PVTO', 'INEPTVS', 'TV', 'QVAMVIS/1', 'SIMVL/1', 'CREDO', 'ILIA', 'IN', 'INVENVSTVS', 'OMNIS', 'RVMPO', 'VT/4', 'VERE', 'SVM/1', 'CREDO', 'ANTE/2', 'ET/2', 'FVRTVM', 'TVVS', 'RESPECTO', 'CVLPA', 'SED', 'PRATVM', 'VLTIMVS', 'ASINIVS/N', 'FLOS', 'SORDIDVS', 'SVM/1', 'HIC/1', 'MVTO/2', 'VOLO/3', 'TALENTVM', 'NECESSE', 'POSTQVAM', 'FACETIAE', 'DEVS', 'EGO', 'FAVEO', 'REMITTO', 'MEVS', 'PAVCI', 'TRECENTI', 'MOVEO', 'DISERTVS', 'SODALIS/1', 'SAETABVS/A', 'CENO', 'FABVLLVS/N', 'EGO', 'AESTIMATIO', 'MNEMOSYNON', 'AMO', 'SVM/1', 'VERVM/4', 'SVDARIVM', 'BENE', 'TV', 'AC/1', 'LINTEVM', 'MEVS', 'MITTO', 'ENIM/2', 'EXSPECTO', 'VERANIOLVS/N', 'ET/2', 'APVD', 'SALSVS', 'PVER', 'AVT', 'EX', 'MVNVS', 'FABVLLVS/N', 'NAM', 'SI/2', 'VEL/1', 'EGO', 'LEPOR', 'VERANIVS/N', 'HIC/1', 'QVARE/1', 'QVI/1', 'NON', 'EGO', 'SVM/1', 'FABVLLVS/N', 'MEVS', 'HENDECASYLLABVS', 'VT/4', 'ET/2', 'AVT', 'IBERVS/A', 'VINVM', 'DIES', 'SIVE/1', 'SINE', 'SACCVLVS', 'ACCIPIO', 'PVELLA', 'CVPIDO/N', 'NAM', 'AMOR', 'ELEGANS', 'VE', 'DO', 'DEVS', 'SI/2', 'ET/2', 'CANDIDVS', 'SAL', 'VENVSTVS', 'VNGVENTVM', 'DONO', 'BONVS', 'QVI/1', 'MEVS', 'TV', 'ET/2', 'CACHINNVS', 'AFFERO', 'CENA', 'NOSTER', 'QVI/1', 'CVM/3', 'AFFERO', 'HIC/1', 'TOTVS', 'BENE', 'SVM/1', 'ROGO', 'VT/4', 'ET/2', 'ARANEA', 'QVIS/2', 'SI/2', 'PLENVS', 'QVE', 'OLFACIO', 'NON', 'MAGNVS', 'OMNIS', 'INQVIO', 'CONTRA/2', 'SVAVIS', 'NAM', 'PVELLA', 'VENVS/N', 'SVM/1', 'ATQVE/1', 'SED', 'TVVS', 'MERVS', 'CVM/2', 'TV', 'CENO', 'CATVLLVS/N', 'NAM', 'FACIO', 'NASVS', 'DO', 'QVIS/1', 'CVR/1', 'IVCVNDVS', 'SI/2', 'AC/1', 'SVM/1', 'MALVM/1', 'ODI', 'PERDO', 'QVIS/1', 'MITTO', 'TV', 'QVI/1', 'MVNVS', 'DISPEREO/1', 'LOQVOR', 'LITTERATOR', 'EGO', 'CALVVS/N', 'TV', 'MVLTVS', 'IMPIVS', 'DEVS', 'AC/1', 'TV', 'NISI', 'SED', 'OCVLVS', 'EGO', 'FABVLLVS/N', 'ODIVM', 'TV', 'MVNVS', 'ISTE', 'VE', 'MALE', 'VT/4', 'DO', 'FACIO', 'AMO', 'MVLTVM/2', 'QVOD/1', 'CLIENS', 'SVLLA/N', 'TV', 'SVM/1', 'ISTE', 'SVSPICOR', 'VATINIANVS/A', 'POETA', 'TANTVM/2', 'QVOD/1', 'HIC/1', 'NON', 'BENE', 'MEVS', 'TOT', 'NOVVS', 'REPERIO', 'DEVS', 'SACER', 'NON', 'HIC/1', 'TV', 'CONTINVVS', 'ABEO/1', 'MITTO', 'VT/4', 'SVFFENVS/N', 'VNDE/1', 'LIBRARIVS/1', 'LVCEO', 'SVPPLICIVM', 'CAESIVS/N', 'REMVNEROR', 'ABEO/1', 'AC/1', 'MALVS/3', 'SCILICET', 'HORRIBILIS', 'MALE', 'TV', 'COLLIGO/3', 'ET/2', 'PEREO/1', 'AD/2', 'INTEREA', 'MALVS/3', 'QVI/1', 'NON', 'LIBELLVS', 'LABOR/1', 'MAGNVS', 'AD/2', 'BEATVS', 'SATVRNALIA/N', 'AFFERO', 'PES', 'SAECVLVM', 'NON', 'DIES', 'VOS', 'ILLVC', 'VENENVM', 'TVVS', 'BONVS', 'FALSVS', 'SCRINIVM', 'AQVINVS/N', 'NAM', 'CVRRO', 'OMNIS', 'TV', 'TVVS', 'CATVLLVS/N', 'DIES', 'SI/2', 'VALEO', 'INCOMMODVM', 'SIC', 'POETA', 'EGO', 'HINC', 'HIC/1', 'QVIS/2', 'FORTE', 'MANVS/1', 'VESTER', 'NOS', 'LECTOR', 'AVRELIVS/N', 'ANIMVS', 'PVDENS', 'CASTVS/2', 'LIBET', 'PVTO', 'AH', 'QVE', 'AC/1', 'MODO/1', 'DICO/2', 'INFESTVS', 'AB', 'VT/4', 'ADMOVEO', 'ET/2', 'NIHIL', 'IN', 'RES', 'PENIS', 'TV', 'PARO/2', 'SI/2', 'TVM', 'SI/2', 'VT/4', 'POPVLVS/1', 'IN', 'HVC', 'QVOD/1', 'QVI/1', 'SI/2', 'INTEGELLVS', 'CONSERVO', 'METVO', 'MOVEO', 'SVM/1', 'PORTA', 'VOS', 'QVI/1', 'PETO', 'PLATEA/1', 'AB', 'QVE', 'QVE', 'QVI/1', 'TV', 'MALVS/3', 'ISTE', 'LIBET', 'VOLO/3', 'TVVS', 'MISER', 'MVGILIS', 'PAEDICO/2', 'QVISQVAM', 'EXPETO', 'QVE', 'VEREOR', 'MALVS/3', 'SVM/1', 'MEVS', 'TVVS', 'VENIA', 'SVVS', 'OCCVPATVS', 'QVA/1', 'PVDENTER', 'NOSTER', 'PES', 'EGO', 'PVER', 'PRAETEREO/1', 'QVANTVM/3', 'MENS', 'QVE', 'MALVS/3', 'PERCVRRO', 'RAPHANVS', 'TV', 'ILLVC', 'NON', 'VT/4', 'VECORS', 'VT/4', 'QVI/1', 'TV', 'VBI/1', 'HIC/1', 'INSIDIAE', 'ATTRAHO', 'LACESSO', 'FORIS/2', 'IN', 'TANTVS', 'FVROR/1', 'CVLPA', 'MODO/1', 'MEVS', 'EGO', 'IMPELLO', 'SCELESTVS', 'NON', 'AMOR', 'CVPIO', 'PVDICVS', 'VNVS', 'CAPVT', 'HORREO', 'INEPTIAE', 'COMMENDO', 'EGO', 'BONVS', 'EXCIPIO', 'QVE', 'FATVM', 'PATEO', 'QVE', 'ET/2', 'PVER', 'VERVM/4', 'TV', 'NAM', 'VERSICVLVS', 'ET/2', 'PVTO', 'HABEO', 'PIVS', 'QVI/1', 'LEGO/2', 'MAS', 'QVI/1', 'TVM', 'LEPOR', 'SVM/1', 'DICO/2', 'DECET', 'SAL', 'PATHICVS', 'PVDICVS', 'CINAEDVS/2', 'FVRIVS/N', 'MOLLICVLVS', 'POSSVM/1', 'DVRVS', 'QVOD/1', 'SI/2', 'ET/2', 'AC/1', 'PRVRIO', 'PILOSVS', 'MALE', 'SVM/1', 'NIHIL', 'AC/1', 'INCITO/1', 'NON', 'PVER', 'PVTO', 'EGO', 'AVRELIVS/N', 'MEVS', 'PARVM/2', 'VERSICVLVS', 'HIC/1', 'IPSE', 'PARVM/2', 'QVI/1', 'VOS', 'PVDICVS', 'EGO', 'POETA', 'QVI/1', 'DENIQVE', 'CASTVS/2', 'MOLLICVLVS', 'IRRVMO', 'LVMBVS', 'MILLE', 'NECESSE', 'EX', 'SVM/1', 'SVM/1', 'SED', 'MOVEO', 'QVOD/1', 'QVI/1', 'EGO', 'MVLTVS', 'PARO/2', 'NEQVEO', 'ET/2', 'TVVS', 'VEREOR', 'FIO', 'HIC/1', 'SVBSILIO', 'SACRVM', 'HABEO', 'SED', 'QVI/1', 'DO', 'PONTICVLVS', 'NE/4', 'BONVS', 'EX', 'RECVMBO', 'VOLO/3', 'O', 'PONS', 'INEPTVS', 'SVPINVS', 'IN', 'SALVM', 'EGO', 'COLONIA/1', 'MEVS', 'STO', 'LONGVS', 'VOS', 'PAEDICO/2', 'BASIVM', 'IRRVMO', 'TV', 'IN', 'PONS', 'VEL/1', 'SVSCIPIO', 'MVNVS', 'MAGNVS', 'SIC', 'IN', 'LVDO', 'TVVS', 'CRVS', 'ASSVLA', 'CAVVS/2', 'SALIO/1', 'EO/1', 'DE', 'MVNICEPS', 'QVIDAM', 'CVPIO', 'PALVS/2', 'LIBIDO', 'RISVS', 'ET/2', 'COLONIA/1', 'REDIVIVVS', 'QVE', 'QVE', 'VT/4', 'INSVLSVS', 'PVER', 'SED', 'IS', 'SI/2', 'AVT', 'SVM/1', 'NAM', 'FRVSTRA', 'IDEM', 'QVE', 'AVT', 'AVT', 'POSSVM/1', 'MANTICA', 'TERGVM', 'PATER', 'ET/2', 'ET/2', 'DENS', 'LIGNEVS', 'INCENDIVM', 'TV', 'PVTIDVS', 'SVM/1', 'VELVT/1', 'LIGVR/A', 'SECVRIS', 'SVM/1', 'POTIS', 'CLAM/1', 'INSIDIAE', 'QVARE/1', 'VARVS/N', 'NEC/2', 'PALIMPSESTVS', 'BELLVS', 'ABHORREO', 'RVRSVS', 'RES', 'SED', 'SERVVS/1', 'NEQVE', 'FVRIVS/N', 'NAM', 'NIHIL', 'ATQVI', 'VERVM/4', 'ASSERVO', 'SVM/1', 'DILIGENS', 'IACEO', 'OMNIS', 'TALIS', 'PONS', 'VETERNVS/1', 'SVM/1', 'VNA', 'SITIO', 'SIC', 'HIC/1', 'VIDEO', 'PVTO', 'SVI/1', 'ATTRIBVO', 'VEL/1', 'CVM/2', 'PARENS/1', 'CORPVS', 'ALNVS', 'QVAM/1', 'STVPOR', 'PRONVS', 'QVOQVE', 'DERELINQVO', 'SVM/1', 'INSTRVO', 'LONGVS', 'MVLTVS', 'SVM/1', 'PVMEX', 'VMBILICVS', 'SATVR', 'ET/2', 'HIC/1', 'SI/2', 'POEMA', 'BEATVS', 'SVM/1', 'QVISQVAM', 'IN', 'VIDEO', 'CIMEX', 'IGNIS', 'COMEDO/2', 'BENE', 'IMPIVS', 'AVT', 'BIMVLVS', 'HIC/1', 'QVE', 'PVELLA', 'IN', 'SI/2', 'QVOT/1', 'DOLEO', 'DISCO', 'VERSVS/1', 'DECEM', 'QVIS/2', 'IPSE', 'MIROR', 'IDEM', 'ERROR', 'QVI/1', 'NEQVE', 'VERVM/4', 'QVI/1', 'CVM/2', 'FACTVM', 'NON', 'ALIVS', 'FACIO', 'SVBLEVO/1', 'ISTE', 'TVVS', 'ET/2', 'STOLIDVS', 'MVLA', 'AD/2', 'EGO', 'LICET/1', 'SVFFENVS/N', 'FACIO', 'PVTO', 'ILLE', 'QVIS/1', 'INFACETVS', 'TAM', 'NEQVE', 'VIDEO', 'SVFFENVS/N', 'ARANEVS/1', 'TIMEO', 'PERICVLVM', 'MAGIS/2', 'EO/1', 'IN', 'PER', 'PALVS/2', 'PATER', 'PRAECEPS/2', 'NEC/2', 'TREMVLVS/3', 'TENELLVLVS', 'PVELLA', 'NEC/2', 'NON', 'CVPIO', 'SED', 'ATQVE/1', 'DESINO', 'VRBANVS', 'ET/2', 'LORVM', 'RVS', 'IN', 'NEC/2', 'POSSVM/1', 'NON', 'BENE', 'LVTVM/1', 'HOMO', 'QVI/1', 'SVM/1', 'DELICATVS/2', 'ET/2', 'LIBET', 'AVDIO', 'IS', 'FERREVS', 'SOLEA', 'AVT', 'ALIVS', 'SVM/1', 'HAEREO', 'QVI/1', 'PROBE', 'DICAX', 'REFERO', 'AC/1', 'AVT', 'INFACETVS', 'SVM/1', 'CVM/3', 'NOVERCA', 'TVVS', 'NON', 'VENENVM', 'ARIDVS', 'HABEO', 'FLOS', 'HAEDVS', 'EX', 'PARS', 'SVVS', 'IPSE', 'CAENVM', 'MODO/1', 'AVT', 'AMOR', 'DVM/2', 'NOSCO', 'SVM/1', 'RVBER', 'NON', 'IN', 'TV', 'CASVS', 'QVIS/2', 'LVDO', 'NIHIL', 'QVIS/1', 'SIMVL/1', 'NON', 'SI/2', 'PVER', 'PVDICVS', 'NE/4', 'FIO', 'AVT', 'HIC/1', 'VIDEO', 'SIMVL/1', 'NEQVE', 'SVI/1', 'TAM', 'NIMIRVM', 'NEQVE', 'FALLO', 'ARCA', 'SVM/1', 'SILEX', 'CORNV', 'ET/2', 'TANTVMDEM/2', 'SENTIO', 'SVM/1', 'NVNC', 'ANIMVS', 'IN', 'VT/4', 'TENAX', 'ANNVS', 'IOCOR', 'TV', 'IS', 'TACEO', 'IPSE', 'AH', 'SED', 'FACIO', 'IRRVMO', 'MEMBRANA', 'CVM/3', 'AC/1', 'GAVDEO', 'OMNIS', 'VMQVAM', 'QVI/1', 'CONIVX', 'CONCOQVO', 'DOLVS', 'SVM/1', 'QVE', 'INSTAR', 'CVM/3', 'VLNA', 'VT/4', 'VNVS', 'MEVS', 'VIDEO', 'NIHIL', 'VTRVM', 'DE', 'VOLO/3', 'TANGO', 'FINIS', 'ET/2', 'ET/2', 'EGO', 'MILLE', 'DIRIGO', 'NOVVS', 'ILLE', 'MVTO/2', 'SVM/1', 'POEMA', 'SVVS', 'SVM/1', 'OMNIS', 'NON', 'GRAVIS', 'BEATVS', 'CAPVT', 'PONS', 'QVE', 'TOTVS', 'LACVS', 'SINO', 'FOSSA', 'NVLLVS', 'NESCIO', 'EXCITO/1', 'HIC/1', 'IN', 'PAEDICO/2', 'OMNIS', 'EXPERIOR', 'EGO', 'FACIO', 'IS', 'QVOD/1', 'ET/2', 'HOMO', 'OMNIS', 'PLVMBVM', 'LEGO/2', 'VRBANVS', 'NON', 'NEQVE', 'PARENS/1', 'NEC/2', 'VALEO', 'RVINA', 'SICCVS', 'QVARE/1', 'FRIGVS', 'PROFVNDVS', 'PES', 'LIVIDVS', 'VORAGO', 'NEC/2', 'SVI/1', 'VSQVAM', 'SVM/1', 'SVPINVS', 'GRAVIS', 'AVRELIVS/N', 'PATER', 'IRRVMATIO', 'ESVRIO/2', 'VT/4', 'REGIVS', 'VNVS', 'SVM/1', 'TRITVS/2', 'QVI/1', 'SVM/1', 'SVM/1', 'PVLCHRE', 'SOL', 'MAGIS/2', 'SAPIO', 'DORMIO', 'VIRIDIS', 'NVBO', 'NIGER', 'VVA', 'PILVM', 'IN', 'NEC/2', 'NAM', 'PRIOR', 'ISTE', 'AEQVO', 'CAPRIMVLGVS', 'SVFFENVS/N', 'FOSSOR', 'TANTVM/2', 'SCVRRA', 'SVM/1', 'PVLCHRE', 'NON', 'ESVRITIO', 'SVM/1', 'IN', 'SVPPERNATVS', 'SVM/1', 'AN', 'MITTO', 'REPENTE', 'VORAGO', 'ESVRITIO', 'MEVS', 'LATVS/1', 'NVNC', 'VENVSTVS', 'MVLTVS', 'PERSCRIBO', 'IN', 'NOVVS', 'CHARTA', 'TV', 'LIBER/1', 'MODO/1', 'RES', 'IDEM', 'ATTINGO', 'IDEM', 'SCRIBO', 'QVE', 'ALIQVIS', 'QVI/1', 'QVISQVE/2', 'NEQVE', 'ET/2', 'MIRVS', 'SI/2', 'ET/2', 'NON', 'SVDOR', 'MVCVS', 'AB', 'ABSVM/1', 'IN', 'SALIVA', 'ET/2', 'FRICO', 'SI/2', 'INQVINO', 'ADDO', 'HIC/1', 'NEC/2', 'QVE', 'LAPILLVS', 'ET/2', 'HIC/1', 'PARVVM', 'MALVS/3', 'POSSVM/1', 'QVI/1', 'ET/2', 'NEC/2', 'TV', 'AC/1', 'QVOD/1', 'SALILLVM', 'DIGITVS', 'NOLO', 'CVLVS', 'MVNDVS/2', 'ABSVM/1', 'TOTVS', 'CACO', 'ANNVS', 'ATQVE/1', 'TERO', 'QVE', 'SVM/1', 'QVI/1', 'DECIES', 'COMMODVM/1', 'FVRIVS/N', 'SOLEO', 'TV', 'DVRVS', 'TAM', 'PITVITA', 'IS', 'TV', 'SPERNO', 'CENTVM', 'FABA', 'AD/2', 'NASVS', 'BEATVS', 'MANVS/1', 'PVRVS', 'SVM/1', 'MVNDITIES', 'NON', 'VMQVAM', 'PVTO', 'TV', 'SESTERTIVM', 'DESINO', 'ALIVS', 'FLOSCVLVS', 'BEATVS', 'ANNVS', 'PRECOR', 'HIC/1', 'NON', 'QVI/2', 'NEQVE', 'SIC', 'SVM/1', 'DIVITIAE', 'QVI/1', 'IN', 'SVM/1', 'NON', 'AVT', 'HOMO', 'SINO', 'QVI/1', 'ISTE', 'MALO', 'AMO', 'SATIS/2', 'DO', 'SED', 'SVM/1', 'AVT', 'ARCA', 'SERVVS/1', 'INQVIO', 'SVM/1', 'QVOT/1', 'NAM', 'IVVENTIVS/N', 'MIDAS/N', 'SVM/1', 'AB', 'ILLE', 'BELLVS', 'NEQVE', 'TV', 'POSTHAC', 'QVAM/1', 'O', 'MODO/1']

    '''
    for x in text_slice:
        if x[0] not in mongo_v:
            print(x[0])
        else:
            mongo_v.remove(x[0])
    '''

    return text_slice


def find_hapax_legomena(words, dictionary:dict):
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[dictionary[word]['SIMPLE_LEMMA']] += 1
    return [word.capitalize() for word, freq in word_frequencies.items() if freq == 1]


class TextAnalyzer:

    def __init__(self):

        self.texts = [] 
        self.num_words_ct = None
        
        self.dictionary, self.dictionary_time = mg_get_latin_dictionary(dict_db)
        print("Dictionary Loaded: {} seconds".format(self.dictionary_time))

        (result, self.diederich_time) = mg_get_diederich("Diederich Frequency List (General)_LIST")
        self.diederich300, self.diederich1500 = result

        self.dcc, self.dcc_time = mg_get_dcc(db, "DCC Latin Core_LOCAL_LIST")
        print("DCC Loaded: {} seconds".format(self.dcc_time))


    # Add working file for subordinations/section?
    def add_text(self, form_request: str, language: str, start_section, end_section):
        location_list = MongoDefinitionTools.mg_get_locations(language, form_request)
        location_words = MongoDefinitionTools.mg_get_location_words(language, form_request)
        self.texts.append((MongoDefinitionTools.mg_get_text_as_Text(language, form_request, location_list, location_words),start_section, end_section))

    def get_textname(self):
        if len(self.texts) == 0: return -1
        elif len(self.texts) == 1: return self.texts[0][0].name
        else: return " + ".join([text[0].name for text in self.texts])

    def num_words(self) -> int:
        if self.num_words_ct: return self.num_words_ct # no need to recompute every time
        if not self.texts: return -1

        total = 0
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            # head_word is a guaranteed field so len(text_slice) should be sufficient
            total += len(text_slice) 
        
        self.num_words_ct = total
        return self.num_words_ct

    def vocab_size(self) -> int:
        if len(self.texts) == 0:
            return -1
        elif len(self.texts) == 1:
            text_slice = get_slice(
                self.texts[0][0], self.texts[0][1], self.texts[0][2])
            vocabulary = set(word[0] for word in text_slice)
            return len(vocabulary)
        else:
            vocab = set()
            for text in self.texts:
                text_slice = get_slice(text[0], text[1], text[2])
                vocabulary = set(word[0] for word in text_slice)
                vocab = vocab.union(vocabulary)
            return len(vocab)

    @round_decorator
    def hapax_legonema(self, tupleFlag=False):
        if not self.texts: return ([], 0)

        allwords = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word:
                    allwords.append(word)

        if not allwords: return ([], 0)

        hapax_legomena = find_hapax_legomena(allwords, self.dictionary)
        hapax_legomena = sorted(hapax_legomena)
        percentage = len(hapax_legomena) / len(allwords) * 100

        return (hapax_legomena, percentage)

    @round_decorator
    def lex_density(self):
        lexical_categories = {"Adjective", "Adverb", "Noun", "Verb"}

        if not self.texts:
            return -1

        lexical_sum = 0
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PART_OF_SPEECH"] in lexical_categories:
                    lexical_sum += 1

        total_words = self.num_words()
        lexical_density = lexical_sum / total_words if total_words > 0 else 0
        return lexical_density


    @round_decorator
    def lex_sophistication(self):
        if len(self.texts) == 0:
            return -1

        rare_count = 0
        total_words = 0

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word not in self.diederich1500:
                    rare_count += 1
                total_words += 1

        lexical_sophistication = rare_count / total_words if total_words > 0 else 0
        return lexical_sophistication


    @round_decorator
    def lex_variation(self):
        if len(self.texts) == 0:
            return -1

        all_words = []

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word:  # skip empty/null words
                    all_words.append(word)

        total_words = len(all_words)
        num_unique = len(set(all_words))

        if total_words > 0 and num_unique > 0:
            TTR = num_unique / total_words
            RootTTR = num_unique / sqrt(total_words)
            CTTR = num_unique / sqrt(2 * total_words)
            LogTTR = log(num_unique) / log(total_words)
            return (TTR, RootTTR, CTTR, LogTTR)
        else:
            return (0, 0, 0, 0)


    @round_decorator
    def LexR(self):
        if len(self.texts) == 0:
            return 0

        text_slice = get_slice(self.texts[0][0], self.texts[0][1], self.texts[0][2])

        out300 = 0
        outDCC = 0
        out1500 = 0
        countWords = 0

        for word_tuple in text_slice:
            word = word_tuple[0]
            if word not in self.diederich300:
                out300 += 1
            if word not in self.dcc:
                outDCC += 1
            if word not in self.diederich1500:
                out1500 += 1
            countWords += 1

        if countWords == 0:
            return 0  # Avoid division by zero

        freq300 = (out300 / countWords) * 100
        freqDCC = (outDCC / countWords) * 100
        freq1500 = (out1500 / countWords) * 100

        mean_word_length = get_avg_word_length(self.texts[0][0], self.texts[0][1], self.texts[0][2])
        lexical_sophistication = get_lexical_sophistication(self.texts[0][0], self.texts[0][1], self.texts[0][2])
        lexical_variation = get_lexical_variation(self.texts[0][0], self.texts[0][1], self.texts[0][2])
        logTTR = lexical_variation[3]
        rootTTR = lexical_variation[1]

        lex_r = ((mean_word_length * 0.457) + (freq300 * 0.063) + (freqDCC * 0.076) + (freq1500 * 0.092) +
                 (lexical_sophistication * 0.059) + (logTTR * 0.312) + (rootTTR * 0.143))

        lex_r -= 11.7
        lex_r += 6
        lex_r *= 0.833

        return lex_r


    def totalWordsNoProper(self):
        if len(self.texts) == 0:
            return -1

        words = []

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        return len(words)


    def uniqueWordsNoProper(self):
        if len(self.texts) == 0:
            return -1

        vocabulary = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    vocabulary.add(word)

        return len(vocabulary)


    def top20NoDie300(self):
        properNounCats = ["1", "T"]
        if len(self.texts) == 0:
            return -1

        word_counts = defaultdict(int)

        for text in self.texts: # adapted to work for multi text
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0] # head_word
                if word in self.dictionary:
                    word_info = self.dictionary[word]
                    if word_info["PROPER"] not in properNounCats and int(word_info["CORPUSFREQ"]) > 300:
                        lemma = word_info.get("SIMPLE_LEMMA")
                        if lemma: word_counts[lemma] += 1

        top_20_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        return [word for word, freq in top_20_words]

    @round_decorator
    def freqBinMetrics(self):
        if not self.texts:
            return -1

        words = []

        # Process all texts
        for text_data in self.texts:
            text_obj, start, end = text_data
            text_slice = get_slice(text_obj, start, end)

            for word_tuple in text_slice:
                word = word_tuple[0]
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        # Frequency bins
        bins = {"0_200": 0, "201_500": 0, "501_1000": 0, "1001_1500": 0, "1501_2500": 0, "2500_plus": 0}

        for word in words:
            if word in self.dictionary:
                try:
                    freq = float(self.dictionary[word]["CORPUSFREQ"])
                except (ValueError, TypeError):
                    continue  # skip malformed frequencies

                if freq <= 200:
                    bins["0_200"] += 1
                elif freq <= 500:
                    bins["201_500"] += 1
                elif freq <= 1000:
                    bins["501_1000"] += 1
                elif freq <= 1500:
                    bins["1001_1500"] += 1
                elif freq <= 2500:
                    bins["1501_2500"] += 1
                else:
                    bins["2500_plus"] += 1

        total_words = len(words)
        if total_words == 0:
            return 0, 0, 0, 0, 0, 0

        return tuple(
            (count / total_words) * 100 for count in [
                bins["0_200"],
                bins["201_500"],
                bins["501_1000"],
                bins["1001_1500"],
                bins["1501_2500"],
                bins["2500_plus"]
            ]
        )        

    @round_decorator
    def avgWordLength(self):
        if len(self.texts) == 0:
            return -1

        words = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            words.extend(word_tuple[0] for word_tuple in text_slice)

        if len(words) > 0: return sum(len(word) for word in words) / len(words)
        else: return 0

    def plot_word_freq(self, plot_num=0):
        if len(self.texts) == 0:
            return
        
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])
        
        # Create DataFrame
        df = pd.DataFrame(text_slices_concat, columns=[
            "Word", "Index", "Lemma", "Definition", "Notes", "Section", 
            "Word Count", "Sentence", "Case", "Lasla_Subordination_Code", "Grammatical_Subcategory"
        ])
        
        # Calculate word frequency
        word_frequency = df['Word'].value_counts().reset_index()
        word_frequency.columns = ['Word', 'Frequency']
        
        # Plot setup
        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.barplot(data=word_frequency[:30], x='Word', y='Frequency', palette=colorblind_palette)
        sns.despine()
        
        title = f"Word Frequency of {self.get_textname()}"
        plt.title(title, **title_font)
        
        plt.xlabel('Word', **axis_font)
        plt.ylabel('Frequency', **axis_font)
        plt.xticks(rotation=90)
        
        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)
        
        # Save path
        plot_partial = f'/static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial
        
        plt.savefig(plot_path)
        plt.close()
        
        # Return a relative path suitable for front-end use
        return f'/plot{plot_num}.png'


    def plot_lin_lex_load(self, plot_num=2):
        if len(self.texts) == 0:
            return "/blank_plot.png"

        # Gather all word tuples from all texts
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])

        scores = []
        for word_tuple in text_slices_concat:
            word = word_tuple[0]
            if word in self.dictionary:
                freq = int(self.dictionary[word]["CORPUSFREQ"])
                if freq <= 200:
                    scores.append(2)
                elif 200 < freq <= 1000:
                    scores.append(1)
                elif 1000 < freq <= 2000:
                    scores.append(-1)
                elif 2000 < freq <= 5000:
                    scores.append(-2)
                elif freq > 5000:
                    scores.append(-4)
            else:
                scores.append(-4)

        if len(scores) == 0:
            return "/blank_plot.png"

        rolling_window_size = 25
        rolling_average = pd.Series(scores).rolling(window=rolling_window_size).mean()
        rolling_average.dropna(inplace=True)

        savgol_num = min(51, len(rolling_average))
        if savgol_num < 3:
            return "/blank_plot.png"
        if savgol_num % 2 == 0:
            savgol_num -= 1

        smoothed_scores = savgol_filter(rolling_average, savgol_num, 3)
        x_indexes = list(range(len(smoothed_scores)))

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=x_indexes, y=smoothed_scores, color=colorblind_palette[0])
        sns.despine()

        if len(self.texts) == 1:
            title = f"Rolling Linear Lexical Load of {self.texts[0][0].name}"
        else:
            title = f"Rolling Linear Lexical Load of {self.get_textname()}"
        plt.title(title, **title_font)

        plt.xlabel('Word Index', **axis_font)
        plt.ylabel('Smoothed Lexical Load', **axis_font)

        plot_partial = f'/static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial

        plt.savefig(plot_path)
        plt.close()

        return f'/plot{plot_num}.png'


    def plot_cum_lex_load(self, plot_num=1):
        if len(self.texts) == 0:
            return '/blank_plot.png'

        # Combine all slices to support multi-text
        text_slices_concat = []
        for text in self.texts:
            text_slices_concat += get_slice(text[0], text[1], text[2])

        scores = []
        for word_tuple in text_slices_concat:
            word = word_tuple[0]
            if word in self.dictionary:
                freq = int(self.dictionary[word]["CORPUSFREQ"])
                if freq <= 200:
                    scores.append(2)
                elif 200 < freq <= 1000:
                    scores.append(1)
                elif 1000 < freq <= 2000:
                    scores.append(-1)
                elif 2000 < freq <= 5000:
                    scores.append(-2)
                else:
                    scores.append(-4)
            else:
                scores.append(-4)

        if len(scores) == 0:
            return '/blank_plot.png'

        cumulative_scores = pd.Series(scores).cumsum()
        x_indexes = list(range(len(cumulative_scores)))

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=x_indexes, y=cumulative_scores, color='blue')

        sns.despine()
        title = f"Cumulative Lexical Load of {self.get_textname()}"
        plt.title(title, fontdict={'fontsize': 12})
        plt.xlabel('Word Index', fontdict={'fontsize': 10})
        plt.ylabel('Cumulative Lexical Load', fontdict={'fontsize': 10})

        plot_partial = f'/static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial

        plt.savefig(plot_path)
        plt.close()

        return f'/plot{plot_num}.png'


    def plot_freq_bin(self, plot_num=3):
        if len(self.texts) == 0:
            return '/blank_plot.png'

        # Gather words from all text slices
        words = []
        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word_tuple in text_slice:
                word = word_tuple[0]
                # filter out proper nouns
                if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                    words.append(word)

        if not words:
            return '/blank_plot.png'

        # Initialize frequency bins
        count0_200 = 0
        count201_500 = 0
        count501_1000 = 0
        count1001_1500 = 0
        count1501_2500 = 0
        count2500plus = 0

        for word in words:
            if word in self.dictionary:
                freq = int(self.dictionary[word]["CORPUSFREQ"])
                if freq <= 200:
                    count0_200 += 1
                elif freq <= 500:
                    count201_500 += 1
                elif freq <= 1000:
                    count501_1000 += 1
                elif freq <= 1500:
                    count1001_1500 += 1
                elif freq <= 2500:
                    count1501_2500 += 1
                else:
                    count2500plus += 1

        total = len(words)
        data = {
            'Frequency Range': ['0-200', '201-500', '501-1000', '1001-1500', '1501-2500', '2500+'],
            'Percentage of Words': [
                count0_200 / total,
                count201_500 / total,
                count501_1000 / total,
                count1001_1500 / total,
                count1501_2500 / total,
                count2500plus / total
            ]
        }

        df = pd.DataFrame(data)

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        barplot = sns.barplot(x='Frequency Range', y='Percentage of Words', data=df, palette=colorblind_palette)
        sns.despine()

        title = f"Percentage of Words in Frequency Ranges of {self.get_textname()}" if len(self.texts) > 1 else f"Percentage of Words in Frequency Ranges of {self.texts[0][0].name}"
        plt.title(title, **title_font)

        plt.xlabel('Frequency Range', **axis_font)
        plt.ylabel('Percentage of Words', **axis_font)

        # Tick label fonts
        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)

        # Annotate bars
        for p in barplot.patches:
            barplot.annotate(f"{p.get_height():.2f}",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center',
                            xytext=(0, 10),
                            textcoords='offset points')

        # Save and return path
        plot_partial = f'/static/assets/plots/plot{plot_num}.png'
        plot_path = parent_dir + plot_partial

        plt.savefig(plot_path)
        plt.close()

        return f'/plot{plot_num}.png'


    def _flatten_texts(self):
        text_slice = []
        for text in self.texts:
            text_slice.extend(get_slice(text[0], text[1], text[2]))
        return text_slice
    
    @round_decorator
    def spache_score(self):
        if len(self.texts) == 0:
            return 0

        sections = set()
        total_words = 0
        unique_words = set()
        unfamiliar_words = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]
                if section is not None:
                    sections.add(section)
                total_words += 1
                unique_words.add(lemma)
                if lemma not in self.dcc:
                    unfamiliar_words.add(lemma)

        if len(sections) <= 1:
            return 0
        avg_sentence_length = total_words / len(sections)
        percent_unfamiliar = (len(unfamiliar_words) / len(unique_words)) * 100

        spache_score = (0.121 * avg_sentence_length) + (0.082 * percent_unfamiliar) + 0.659
        return spache_score

    
    @round_decorator
    def dale_chall_score(self):
        if len(self.texts) == 0:
            return 0

        total_words = 0
        difficult_words = 0
        sections = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]

                total_words += 1
                if section is not None:
                    sections.add(section)

                if lemma not in self.dcc:
                    difficult_words += 1

        if len(sections) <= 1:
            return 0

        # Compute PDW and ASL
        pdw = (difficult_words / total_words) * 100
        asl = total_words / len(sections)

        # Dale-Chall formula
        score = (0.1579 * pdw) + (0.0496 * asl)
        if pdw >= 5:
            score += 3.6365

        return score
    
    @round_decorator
    def ari_score(self):
        if len(self.texts) == 0:
            return 0

        total_words = 0
        total_chars = 0
        sections = set()

        for text in self.texts:
            text_slice = get_slice(text[0], text[1], text[2])
            for word in text_slice:
                lemma = word[0]
                section = word[7]

                total_words += 1
                total_chars += len(lemma)

                if section is not None:
                    sections.add(section)
        if len(sections) <= 1 or total_words == 0:
            return 0

        sentence_count = len(sections)

        # ARI formula
        score = (4.71 * (total_chars / total_words)) + (0.5 * (total_words / sentence_count)) - 21.43
        return score

    @round_decorator
    def coleman_liau_score(self):
        if len(self.texts) == 0:
            return 0

        text_slice = self._flatten_texts()

        if len(text_slice) < 100:
            return 0

        sample = text_slice[:100]
        total_letters = 0
        sentence_sections = set()

        for word in sample:
            orthographic_form = word[2] 
            section = word[7]            

            total_letters += len(orthographic_form)

            if section is not None:
                sentence_sections.add(section)

        L = total_letters / 100  # Avg letters per 100 words
        S = len(sentence_sections)  # Approx. number of sentences in first 100 words

        score = (0.0588 * L) - (0.296 * S) - 15.8
        return score

    def _get_word_stats(self, text_slice): # helper for lix and rix
        total_words = 0
        long_words = 0
        sentence_sections = set()

        for word in text_slice:
            orthographic_form = word[2]
            section = word[7]

            if orthographic_form:
                total_words += 1
                if len(orthographic_form) > 6: long_words += 1

            if section is not None: sentence_sections.add(section)

        return total_words, long_words, len(sentence_sections)

    @round_decorator
    def lix_score(self):
        if not self.texts:
            return 0

        text_slice = self._flatten_texts()
        total_words, long_words, sentence_count = self._get_word_stats(text_slice)

        if total_words == 0 or sentence_count <= 1: return 0

        percent_long_words = (long_words * 100) / total_words
        lix = (total_words / sentence_count) + percent_long_words
        
        return lix

    @round_decorator
    def rix_score(self):
        if not self.texts:
            return 0

        text_slice = self._flatten_texts()
        _, long_words, sentence_count = self._get_word_stats(text_slice)

        if sentence_count <= 1:
            return 0

        rix = long_words / sentence_count
        return rix

    @round_decorator
    def smog_score(self):
        if len(self.texts) == 0:
            return 0

        text_slice = self._flatten_texts()

        complex_words = 0
        sentence_sections = set()

        for word in text_slice:
            orthographic_form = word[2]  # orthographic form
            section = word[7]            

            if orthographic_form and len(orthographic_form) > 6:
                complex_words += 1

            if section is not None:
                sentence_sections.add(section)

        sentence_count = len(sentence_sections)

        if sentence_count <= 1 or complex_words == 0:
            return 0

        smog = 1.043 * math.sqrt((complex_words * 30) / sentence_count) + 3.1291
        return smog
    
    def plot_rolling_lin_lex_load(self, text_object: Text, start_section, end_section, rolling_window_size=25):
        start_index = text_object.sections[start_section]
        end_index = text_object.sections[end_section]
        text_slice = text_object.words[start_index:end_index]

        if start_section == 'start' and end_section == 'end':
            text_slice = text_object.words

        # Go through the words of text_slice
        # Connect to Dictionary to filter out PROPER, "1" and "T"
        words = []
        scores = []
        for word_tuple in text_slice:
            word = word_tuple[0]
            # filter out proper nouns
            if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                words.append(word)

        for word in words:
            if word in self.dictionary:
                if int(self.dictionary[word]["CORPUSFREQ"]) <= 200:
                    scores.append(2)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 200 and int(self.dictionary[word]["CORPUSFREQ"]) <= 1000:
                    scores.append(1)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 1000 and int(self.dictionary[word]["CORPUSFREQ"]) <= 2000:
                    scores.append(-1)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 2000 and int(self.dictionary[word]["CORPUSFREQ"]) <= 5000:
                    scores.append(-2)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 5000:
                    scores.append(-4)
                    continue
            else:
                scores.append(-4)
                continue

        # Calculate rolling average of the scores
        rolling_average = pd.Series(scores).rolling(
            window=rolling_window_size).mean()

        # Apply Savitzky-Golay filter
        # window size 51, polynomial order 3
        smoothed_scores = savgol_filter(rolling_average, 101, 3)

        x_indexes = list(range(len(words)))

        # calculate average linear lexical score for the entire text
        average_score = np.mean(scores)

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=x_indexes, y=smoothed_scores,
                    errorbar=None, color=colorblind_palette[0])

        # add a horizontal line representing the average linear lexical score
        plt.axhline(y=average_score, color=colorblind_palette[1], linestyle='--')

        sns.despine()
        plt.title(f"Linear Lexical Load of {text_object.name}", **title_font)
        plt.xlabel('Word', **axis_font)
        plt.ylabel(
            f'{rolling_window_size}-Word Rolling Average of Linear Lexical Load Score', **axis_font)

        # Get the current Axes instance
        ax = plt.gca()

        # set x-axis ticks to window size?  -> Only activate this if you want to see all the numbers jumble up at the bottom
        # tick_spacing = rolling_window_size  # change this to the size of your slices
        # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        # set font properties to x and y tick labels
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)

        plt.show()

    def plot_linear_heatmap(self, text_object: Text, start_section, end_section, slice_divisor=25, slice_override=0):
        start_index = text_object.sections[start_section]
        end_index = text_object.sections[end_section]
        text_slice = text_object.words[start_index:end_index]

        if start_section == 'start' and end_section == 'end':
            text_slice = text_object.words

        # Go through the words of text_slice
        # Connect to Dictionary to filter out PROPER, "1" and "T"
        words = []
        scores = []
        for word_tuple in text_slice:
            word = word_tuple[0]
            # filter out proper nouns
            if word in self.dictionary and self.dictionary[word]["PROPER"] not in ["1", "T"]:
                words.append(word)

        for word in words:
            if word in self.dictionary:
                if int(self.dictionary[word]["CORPUSFREQ"]) <= 200:
                    scores.append(2)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 200 and int(self.dictionary[word]["CORPUSFREQ"]) <= 1000:
                    scores.append(1)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 1000 and int(self.dictionary[word]["CORPUSFREQ"]) <= 2000:
                    scores.append(-1)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 2000 and int(self.dictionary[word]["CORPUSFREQ"]) <= 5000:
                    scores.append(-2)
                    continue
                if int(self.dictionary[word]["CORPUSFREQ"]) > 5000:
                    scores.append(-4)
                    continue
            else:
                scores.append(-4)
                continue

        # Convert scores to an array of floats->FOR PADDING
        scores = np.array(scores, dtype=float)

        slice_size = len(scores)//slice_divisor

        if slice_override != 0:
            slice_size = slice_override

        # Calculate the remainder of the division
        remainder = len(scores) % slice_size

        # If there's a remainder, pad the scores array
        if remainder != 0:
            # Calculate how many elements we need to add
            pad_size = slice_size - remainder

        # Pad the scores array with np.nan values
        scores = np.pad(scores, (0, pad_size), mode='constant',
                        constant_values=np.nan)

        # Reshape the scores into 2D array where each row corresponds to a slice of words
        scores_matrix = np.array(scores).reshape((-1, slice_size))

        sns.set_style("ticks")
        sns.set_context("paper")
        plt.figure(figsize=(10, 5))

        # Create a heatmap
        sns.heatmap(scores_matrix, cmap='cividis')

        sns.despine()
        plt.title(
            f"Heatmap of Linear Lexical Load of {text_object.name}", **title_font)
        plt.xlabel('Word within Word Slice', **axis_font)
        plt.ylabel(f'{slice_size}-Word Slice', **axis_font)

        # calculate average linear lexical score for the entire text
        average_score = np.mean(scores)

        # Get the current Axes instance
        ax = plt.gca()

        # set font properties to x and y tick labels
        plt.setp(ax.get_xticklabels(), fontproperties=prop)
        plt.setp(ax.get_yticklabels(), fontproperties=prop)

        plt.show()


    def __str__(self) -> str:
        toReturn = ""
        toReturn += f"Number of words:\t{self.num_words()}\n"
        toReturn += f"Vocabulary Size:\t{self.vocab_size()}\n"
        toReturn += f"Hapax Legonema:\t{self.hapax_legonema()}\n"
        toReturn += f"Lexical Density:\t{self.lex_density()}\n"
        toReturn += f"Lexical Sophistication:\t{self.lex_sophistication()}\n"
        toReturn += f"Lexical Variation:\t{self.lex_variation()}\n"
        toReturn += f"LexR:\t{self.LexR()}\n"
        return toReturn


##########################################################################################

# All functions below the hashtag line can find attributes of text in specific sections

# Function to get the number of words in a text
def get_number_of_words(text_object: Text, start_section, end_section):
    '''
    Find the number of words in a predefined section of the book by subtracting the word numbers within Text.sections
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    word_count = end_index - start_index
    if start_section == 'start' and end_section == 'end':
        word_count = text_object.words[-1][1]
    return word_count

# Function to get the size of the text's vocabulary


def get_vocabulary_size(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    vocabulary = set(word[0] for word in text_slice)
    return len(vocabulary)

# Function to display distribution of average word length


def plot_avg_word_length(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=[
                      "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()

    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    # adjust this factor to change the number of labels displayed
    step_size = max(1, n_sections // 20)

    plt.figure(figsize=(10, 5))

    sns.set_style("ticks")
    sns.set_context("paper")
    lineplot = sns.barplot(data=avg_word_length, x='Section',
                           y='Word Length', palette=colorblind_palette, width=0.9)
    sns.despine()
    plt.title(
        f"Average Word Length per Section of {text_object.name}", **title_font)
    plt.xlabel('Section', **axis_font)
    plt.ylabel('Word length', **axis_font)
    # set x-tick labels with a step size
    for ind, label in enumerate(lineplot.get_xticklabels()):
        if ind % step_size == 0:  # only show labels for every nth section
            label.set_visible(True)
        else:
            label.set_visible(False)

    plt.xticks(rotation=90)
    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)
    plt.show()


def plot_avg_word_length2(text_object, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=[
                    "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    df['Word Length'] = df['Word'].apply(len)
    avg_word_length = df.groupby('Section')['Word Length'].mean().reset_index()

    # determine the step size for x-axis labels
    n_sections = avg_word_length['Section'].nunique()
    # adjust this factor to change the number of labels displayed
    step_size = max(1, n_sections // 20)

    fig = px.bar(avg_word_length, x='Section', y='Word Length',
                hover_data=['Word Length'], labels={'Word Length': 'Average Word Length per Section'})

    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
        xaxis_tickangle=-90,
    )

    fig.update_xaxes(
        tickmode='array',
        tickvals=avg_word_length['Section'][::step_size]
    )

    fig.show()


# Function to display distribution of word frequency
def plot_word_frequency(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    df = pd.DataFrame(text_slice, columns=[
                    "Word", "Index", "Lemma", "Definition", "Notes", "Section", "Word Count"])
    word_frequency = df['Word'].value_counts().reset_index()
    word_frequency.columns = ['Word', 'Frequency']

    sns.set_style("ticks")
    sns.set_context("paper")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=word_frequency[:30], x='Word',
                y='Frequency', palette=colorblind_palette)
    sns.despine()
    plt.title(f"Word Frequency of {text_object.name}", **title_font)
    plt.xlabel('Word', **axis_font)
    plt.ylabel('Frequency', **axis_font)
    plt.xticks(rotation=90)

    # Get the current Axes instance
    ax = plt.gca()

    # set font properties to x and y tick labels
    plt.setp(ax.get_xticklabels(), fontproperties=prop)
    plt.setp(ax.get_yticklabels(), fontproperties=prop)
    plt.show()


def get_lexical_sophistication(text_object: Text, start_section, end_section):

    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    hashTable, _ = mg_get_diederich1500(db, "Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020")

    rareCount = 0
    totalWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in hashTable:
            rareCount += 1
        totalWords += 1

    lexical_sophistication = rareCount/totalWords
    return lexical_sophistication


def calculate_unique_words(text_object: Text, start_section, end_section):
    '''
    Calculate the total amount of unique words
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # unique_words = len(set(word[0] for word in text_instance.words))
    unique_words = len(set([word_tuple[0] for word_tuple in text_slice]))
    return unique_words


def get_lexical_variation(text_object: Text, start_section, end_section):
    num_unique = calculate_unique_words(
        text_object, start_section, end_section)  # V
    total_words = get_number_of_words(
        text_object, start_section, end_section)  # N

    TTR = num_unique/total_words
    RootTTR = num_unique/sqrt(total_words)
    CTTR = num_unique/sqrt(2*total_words)
    LogTTR = log(num_unique)/log(total_words)

    return (TTR, RootTTR, CTTR, LogTTR)


def get_average_subordinations_per_section(db, start_location_1, start_location_2, end_location_1, end_location_2):
    '''
    Goes into Full AP MongoDB collection for text, so different LOCATION numbers, i.e., no more 1.4622, now it should be 1_4
    '''
    collection = db["Bridge_Latin_Text_Vergilius_Aeneis_VerAen_newAP_localdef_20230310"]

    # Fetch data from MongoDB
    cursor = collection.find({
        'LOCATION_1': {'$gte': start_location_1, '$lte': end_location_1},
        'LOCATION_2': {'$gte': start_location_2, '$lte': end_location_2}
    })

    # Convert cursor to DataFrame
    df = pd.DataFrame(list(cursor))

    # Ensure 'LOCATION_1' and 'LOCATION_2' are integers
    df[['LOCATION_1', 'LOCATION_2']] = df['LOCATION'].str.split('_', expand=True).astype(int)

    # Filter the DataFrame based on start and end locations
    start_condition = ((df['LOCATION_1'] >= start_location_1) & (df['LOCATION_2'] >= start_location_2))
    end_condition = ((df['LOCATION_1'] <= end_location_1) & (df['LOCATION_2'] <= end_location_2))
    df = df[start_condition & end_condition]

    # Count the total number of non-null entries in the 'SUBORDINATION_CODE' column for each section
    subordinations_per_section = df['SUBORDINATION_CODE'].notnull().groupby(df['SECTION']).sum()

    # Count the total number of sections
    num_sections = df['SECTION'].nunique()

    # Calculate the average subordinations
    if num_sections == 0:
        return 0  # Avoid division by zero
    average_subordinations = subordinations_per_section.sum() / num_sections

    return average_subordinations


def calculate_average_word_length(words):
    if len(words) > 0:
        return sum(len(word) for word in words) / len(words)
    else: return 0


def get_avg_word_length(text_object: Text, start_section, end_section):
    '''
    Get mean word length for a section
    '''
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    sections = []
    for word_tuple in text_slice:
        word = word_tuple[0]
        sections.append(word)

    average_word_length = calculate_average_word_length(sections)
    return average_word_length


def get_gen_lex_r(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    countTokens = 0
    countTitles = 0
    titles = []
    for word_tuple in text_slice:
        countTokens += 1
        word = word_tuple[0]
        if word not in titles:
            countTitles += 1
            titles.append(word)

    gen_lex_r = countTokens/sqrt(countTitles)
    return gen_lex_r


def get_gen_lex_c(text_object: Text, start_section, end_section):
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    countTokens = 0
    countTitles = 0
    titles = []
    for word_tuple in text_slice:
        countTokens += 1
        word = word_tuple[0]
        if word not in titles:
            countTitles += 1
            titles.append(word)

    gen_lex_c = log(countTokens)/log(countTitles)
    return gen_lex_c


def get_lex_r(db, text_object: Text, start_section, end_section):
    # Get the Diederich 300 -> Adjusted MongoDB method
    diederich300, _ = mg_get_diederich300(db)
    
    dcc, _ = mg_get_dcc(db, "Bridge-Vocab-Latin-List-DCC")
    
    diederich1500, _ = mg_get_diederich1500(db, "Bridge_Latin_List_Diederich_all_prep_fastbridge_7_2020")

    # Stats boilerplate
    start_index = text_object.sections[start_section]
    end_index = text_object.sections[end_section]
    text_slice = text_object.words[start_index:end_index]

    if start_section == 'start' and end_section == 'end':
        text_slice = text_object.words

    # Bad naming standards, these are counting which words are NOT in these lists
    in300 = 0
    inDCC = 0
    in1500 = 0
    countWords = 0
    for word_tuple in text_slice:
        if word_tuple[0] not in diederich300:
            in300 += 1
        if word_tuple[0] not in dcc:
            inDCC += 1
        if word_tuple[0] not in diederich1500:
            in1500 += 1
        countWords += 1

    freq300 = in300 / countWords
    freqDCC = inDCC / countWords
    freq1500 = in1500 / countWords

    mean_word_length = get_avg_word_length(
        text_object, start_section, end_section)
    lexical_sophistication = get_lexical_sophistication(
        text_object, start_section, end_section)

    lexical_variation = get_lexical_variation(
        text_object, start_section, end_section)
    logTTR = lexical_variation[3]
    rootTTR = lexical_variation[1]

    lex_r = ((mean_word_length * 0.457) + (freq300 * 0.063) + (freqDCC * 0.076) + (freq1500 *
            0.092) + (lexical_sophistication * 0.059) + (logTTR * 0.312) + (rootTTR * 0.143))

    lex_r -= 11.7
    lex_r *= 0.833

    return lex_r

def stats_compare_result(request, context, sourcetexts, starts, ends, language):
    analyzer_texts = sourcetexts.split('+')
    analyzer_starts = starts.split('+')
    analyzer_ends = ends.split('+')

    # Add text info to analyzer
    analyzers = []
    for i in range(len(analyzer_texts)):
        analyzer = TextAnalyzer()
        analyzer.add_text(analyzer_texts[i], language, analyzer_starts[i], analyzer_ends[i])
        analyzers.append(analyzer)
    

    # Getting Metrics, Hapax
    text_names = [a.texts[0][0].name for a in analyzers]
    text_starts = [a.texts[0][1] for a in analyzers]
    text_ends = [a.texts[0][2] for a in analyzers]

    texts_and_sections = DefinitionTools.get_sections("Latin")

    # add analyzer stats from each text to context
    context.update({
        "request": request,
        "textNames": text_names,
        "textStarts": text_starts,
        "textEnds": text_ends,
        "texts_and_sections": texts_and_sections
    })

    return templates.TemplateResponse("stats-multiple-texts.html", context)

# Routing
router = APIRouter()
router_path = Path.cwd()
templates = Jinja2Templates(directory="templates")
"""Expected Prefix: /stats"""

selected_texts = []


@router.get("/")
async def stats_index(request: Request):
    return templates.TemplateResponse("stats-list-index.html", {"request": request})

@router.get("/mode-select/")
async def stats_mode_selector(request: Request):
    return templates.TemplateResponse("stats-mode-selector.html", {"request": request})

@router.get("/{language}/{mode}/")
async def stats_select(request: Request, language: str, mode: str):
    return templates.TemplateResponse("stats_select.html", {"request": request,
                                                            "mode": mode,
                                                            "titles": MongoDefinitionTools.mg_render_titles(language), 
                                                            'titles2': MongoDefinitionTools.mg_render_titles(language, "2")})


@router.get("/select/sections/{textname}/{language}/")
async def stats_select_section(request: Request, textname: str, language: str):
    sectionDict = MongoDefinitionTools.mg_get_locations(language, textname)
    return sectionDict


@router.post("/{language}/{mode}/result/{sourcetexts}/{starts}-{ends}/{running_list}/")
async def stats_simple_result(request: Request, starts: str, ends: str, sourcetexts: str, language: str, running_list: str, mode: str):
    context = {"request": request}
    running_list = running_list == "running"

    if mode == 'Compare': return stats_compare_result(request, context, sourcetexts, starts, ends, language)
    
    analyzer = TextAnalyzer()

    # check for multiple texts
    multiple_texts = '+' in sourcetexts

    if multiple_texts:
        analyzer_texts = sourcetexts.split('+')
        analyzer_starts = starts.split('+')
        analyzer_ends = ends.split('+')

        for i in range(len(analyzer_texts)):
            analyzer.add_text(analyzer_texts[i], language, analyzer_starts[i], analyzer_ends[i])
    else:
        analyzer.add_text(sourcetexts, language, starts, ends)

    textname = analyzer.get_textname()
    word_count = analyzer.num_words()
    vocab_size = analyzer.vocab_size()
    hapax, hapax_percentage = analyzer.hapax_legonema()
    lex_dens = analyzer.lex_density()
    lex_sophistication = analyzer.lex_sophistication()
    lex_variation = analyzer.lex_variation()
    lex_r = analyzer.LexR()
    total_words_no_p = analyzer.totalWordsNoProper()
    unique_words_no_p = analyzer.uniqueWordsNoProper()
    avgWordLength = analyzer.avgWordLength()
    top20NoDie300 = analyzer.top20NoDie300()
    freqBin1, freqBin2, freqBin3, freqBin4, freqBin5, freqBin6 = analyzer.freqBinMetrics()
    spache_score = analyzer.spache_score()
    dale_chall = analyzer.dale_chall_score()
    ari = analyzer.ari_score()
    coleman_liau = analyzer.coleman_liau_score()
    lix_score = analyzer.lix_score()
    rix_score = analyzer.rix_score()
    smog_score = analyzer.smog_score()


    freq_plot_path = analyzer.plot_word_freq()
    cum_lex_plot_path = analyzer.plot_cum_lex_load()
    lin_lex_plot_path = analyzer.plot_lin_lex_load()
    freq_bins_plot_path = analyzer.plot_freq_bin()
    
    # check if server works using above. if not, uncomment/figure something out
    # base_path = '/FastBridge/FastBridgeApp/static/assets/plots/'
    # freq_relative_plot_path = os.path.relpath(freq_plot_path, start=base_path)
    # cum_lex_relative_plot_path = os.path.relpath(cum_lex_plot_path, start=base_path)
    # lin_lex_relative_plot_path = os.path.relpath(lin_lex_plot_path, start=base_path)
    # freq_bins_relative_plot_path = os.path.relpath(freq_bins_plot_path, start=base_path)

    context.update({
        "text_name": textname if not multiple_texts else textname.split(" + "),
        "start_section": starts if not multiple_texts else starts.split("+"),
        "end_section": ends if not multiple_texts else ends.split("+"),
        "word_count": word_count,
        "vocab_size": vocab_size,
        "hapax_legonema": hapax,
        "hapax_percentage": hapax_percentage,
        "lexical_density": lex_dens,
        "lexical_sophistication": lex_sophistication,
        "lexical_variation": lex_variation,
        "LexR": lex_r,
        "smog": smog_score,
        "total_words_no_proper": total_words_no_p,
        "unique_words_no_proper": unique_words_no_p,
        "avg_word_length": avgWordLength,
        "top20_NoDie300": top20NoDie300,
        "freq1": freqBin1,
        "freq2": freqBin2,
        "freq3": freqBin3,
        "freq4": freqBin4,
        "freq5": freqBin5,
        "freq6": freqBin6,
        "spache": spache_score,
        "dale_chall": dale_chall,
        "ari": ari,
        "coleman_liau": coleman_liau,
        "lix": lix_score,
        "rix": rix_score,
        "freq_plot_path": freq_plot_path,
        "cum_lex_plot_path": cum_lex_plot_path,
        "lin_lex_plot_path": lin_lex_plot_path,
        "freq_bins_plot_path": freq_bins_plot_path,
        # "freq_plot_path": freq_relative_plot_path,
        # "cum_lex_plot_path": cum_lex_relative_plot_path,
        # "lin_lex_plot_path": lin_lex_relative_plot_path,
        # "freq_bins_plot_path": freq_bins_relative_plot_path
    })

    return templates.TemplateResponse("stats-single-text.html", context)
   
@router.get("/get_metrics/{text_name}/{section_start}-{section_end}/{selected_index}")
async def get_metrics_html(request: Request, text_name: str, section_start: str, section_end: str, selected_index: int):
    context = {"request": request}
    
    analyzer = TextAnalyzer()
    
    analyzer.add_text(text_name, "Latin", section_start, section_end)

    textname = analyzer.get_textname()
    word_count = analyzer.num_words()
    vocab_size = analyzer.vocab_size()
    hapax, hapax_percentage = analyzer.hapax_legonema()
    lex_dens = analyzer.lex_density()
    lex_sophistication = analyzer.lex_sophistication()
    lex_variation = analyzer.lex_variation()
    lex_r = analyzer.LexR()
    total_words_no_p = analyzer.totalWordsNoProper()
    unique_words_no_p = analyzer.uniqueWordsNoProper()
    avgWordLength = analyzer.avgWordLength()
    top20NoDie300 = analyzer.top20NoDie300()
    freqBin1, freqBin2, freqBin3, freqBin4, freqBin5, freqBin6 = analyzer.freqBinMetrics()
    spache_score = analyzer.spache_score()
    dale_chall = analyzer.dale_chall_score()
    ari = analyzer.ari_score()
    coleman_liau = analyzer.coleman_liau_score()
    lix_score = analyzer.lix_score()
    rix_score = analyzer.rix_score()
    smog_score = analyzer.smog_score()
    
    # Remove file path references and use database for plots (if applicable)
    plotpath_nums = [0, 1, 2, 3]
    if selected_index > 0:  # if the selected index isn't the first set of graphs
        plotpath_nums = [num + (4 * selected_index) for num in plotpath_nums]

    # Example plot paths assuming they're stored in the database
    freq_plot_path = f'/plot{plotpath_nums[0]}.png'
    cum_lex_plot_path = f'/plot{plotpath_nums[1]}.png'
    lin_lex_plot_path = f'/plot{plotpath_nums[2]}.png'
    freq_bins_plot_path = f'/plot{plotpath_nums[3]}.png'

    now = datetime.utcnow()  # for caching issue with plots
    
    context.update({
        "request": request,
        "text_name": textname,
        "start_section": section_start,
        "end_section": section_end,
        "word_count": word_count,
        "vocab_size": vocab_size,
        "hapax_legomena": hapax,
        "hapax_percentage": hapax_percentage,
        "lexical_density": lex_dens,
        "lexical_sophistication": lex_sophistication,
        "lexical_variation": lex_variation,
        "LexR": lex_r,
        "smog": smog_score,
        "total_words_no_proper": total_words_no_p,
        "unique_words_no_proper": unique_words_no_p,
        "avg_word_length": avgWordLength,
        "top20_NoDie300": top20NoDie300,
        "freq1": freqBin1,
        "freq2": freqBin2,
        "freq3": freqBin3,
        "freq4": freqBin4,
        "freq5": freqBin5,
        "freq6": freqBin6,
        "spache": spache_score,
        "dale_chall": dale_chall,
        "ari": ari,
        "coleman_liau": coleman_liau,
        "lix": lix_score,
        "rix": rix_score,
        "freq_plot_path": freq_plot_path,
        "cum_lex_plot_path": cum_lex_plot_path,
        "lin_lex_plot_path": lin_lex_plot_path,
        "freq_bins_plot_path": freq_bins_plot_path,
        "now": now
    })

    return templates.TemplateResponse('stats-column-data.html', context)


@router.get("/formulas")
async def read_formulas(request: Request):
    return templates.TemplateResponse("stats-formulas.html", {"request": request})


@router.get("/cumulative/{language}/")
async def stats_cumulative(request: Request, language: str):
    # Retrieve the selected text names from the session or storage
    # Replace with your storage retrieval logic
    selected_texts = retrieve_selected_texts()

    # Process the selected text names and retrieve the corresponding book data
    sectionDict = DefinitionTools.get_sections(language)
    sectionBooks = [sectionDict[textname] for textname in selected_texts]

    # Perform cumulative statistics calculations or any other operations on sectionBooks

    return templates.TemplateResponse("stats_cumulative.html", {"request": request, "sectionBooks": sectionBooks})
