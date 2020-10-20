import text
nan=""
section_words = {'start': -1, '1.1': 8, '1.2': 14, '1.3': 22, '1.4': 29, '1.5': 37, '1.6': 44, '1.7': 51, '1.8': 58, '1.9': 66, '1.10': 72, '1.11': 78, '1.12': 84, '1.13': 90, '1.14': 97, '1.15': 104, '1.16': 110, '1.17': 118, '1.18': 128, '1.19': 135, '1.20': 141, '1.21': 148, '1.22': 154, '1.23': 161, '1.24': 169, '1.25': 176, '1.26': 182, '1.27': 188, '1.28': 195, '1.29': 201, '1.30': 207, '1.31': 214, '1.32': 220, '1.33': 226, '1.34': 233, '1.35': 241, '1.36': 248, '1.37': 256, '1.38': 262, '1.39': 269, '1.40': 275, '1.41': 282, '1.42': 289, '1.43': 296, '1.44': 301, '1.45': 307, '1.46': 315, '1.47': 324, '1.48': 331, '1.49': 337, '1.50': 344, '1.51': 351, '1.52': 358, '1.53': 363, '1.54': 370, '1.55': 376, '1.56': 383, '1.57': 391, '1.58': 399, '1.59': 408, '1.60': 414, '1.61': 422, '1.62': 429, '1.63': 437, '1.64': 446, '1.65': 454, '1.66': 461, '1.67': 467, '1.68': 474, '1.69': 481, '1.70': 488, '1.71': 495, '1.72': 500, '1.73': 506, '1.74': 514, '1.75': 521, '1.76': 529, '1.77': 536, '1.78': 545, '1.79': 551, '1.80': 557, '1.81': 564, '1.82': 572, '1.83': 580, '1.84': 587, '1.85': 596, '1.86': 603, '1.87': 610, '1.88': 617, '1.89': 624, '1.90': 631, '1.91': 637, '1.92': 642, '1.93': 649, '1.94': 658, '1.95': 666, '1.96': 672, '1.97': 678, '1.98': 686, '1.99': 694, '1.100': 701, '1.101': 709, '1.102': 714, '1.103': 722, '1.104': 729, '1.105': 736, '1.106': 744, '1.107': 751, '1.108': 758, '1.109': 766, '1.110': 774, '1.111': 781, '1.112': 788, '1.113': 795, '1.114': 802, '1.115': 809, '1.116': 817, '1.117': 825, '1.118': 831, '1.119': 840, '1.120': 847, '1.121': 855, '1.122': 861, '1.123': 867, '1.124': 872, '1.125': 879, '1.126': 886, '1.127': 892, '1.128': 898, '1.129': 904, '1.130': 911, '1.131': 920, '1.132': 927, '1.133': 935, '1.134': 941, '1.135': 948, '1.136': 955, '1.137': 962, '1.138': 969, '1.139': 977, '1.140': 985, '1.141': 991, '1.142': 999, '1.143': 1006, '1.144': 1012, '1.145': 1018, '1.146': 1025, '1.147': 1031, '1.148': 1040, '1.149': 1046, '1.150': 1055, '1.151': 1064, '1.152': 1070, '1.153': 1077, '1.154': 1084, '1.155': 1090, '1.156': 1098, '1.157': 1104, '1.158': 1111, '1.159': 1118, '1.160': 1125, '1.161': 1133, '1.162': 1141, '1.163': 1148, '1.164': 1155, '1.165': 1162, '1.166': 1168, '1.167': 1175, '1.168': 1182, '1.169': 1189, '1.170': 1195, '1.171': 1202, '1.172': 1207, '1.173': 1214, '1.174': 1220, '1.175': 1227, '1.176': 1234, '1.177': 1241, '1.178': 1247, '1.179': 1254, '1.180': 1260, '1.181': 1267, '1.182': 1273, '1.183': 1281, '1.184': 1288, '1.185': 1294, '1.186': 1302, '1.187': 1310, '1.188': 1316, '1.189': 1323, '1.190': 1330, '1.191': 1337, '1.192': 1343, '1.193': 1351, '1.194': 1359, '1.195': 1366, '1.196': 1372, '1.197': 1378, '1.198': 1386, '1.199': 1394, '1.200': 1401, '1.201': 1407, '1.202': 1413, '1.203': 1420, '1.204': 1427, '1.205': 1434, '1.206': 1440, '1.207': 1446, '1.208': 1453, '1.209': 1460, '1.418': 1466, '1.419': 1473, '1.420': 1479, '1.421': 1484, '1.422': 1491, '1.423': 1497, '1.424': 1504, '1.425': 1511, '1.426': 1518, '1.427': 1525, '1.428': 1531, '1.429': 1537, '1.430': 1544, '1.431': 1551, '1.432': 1557, '1.433': 1563, '1.434': 1570, '1.435': 1576, '1.436': 1583, '1.437': 1589, '1.438': 1595, '1.439': 1601, '1.440': 1609, '1.494': 1615, '1.495': 1623, '1.496': 1629, '1.497': 1634, '1.498': 1642, '1.499': 1648, '1.500': 1655, '1.501': 1662, '1.502': 1667, '1.503': 1674, '1.504': 1681, '1.505': 1687, '1.506': 1694, '1.507': 1702, '1.508': 1708, '1.509': 1714, '1.510': 1721, '1.511': 1728, '1.512': 1734, '1.513': 1740, '1.514': 1747, '1.515': 1753, '1.516': 1759, '1.517': 1766, '1.518': 1773, '1.519': 1779, '1.520': 1786, '1.521': 1792, '1.522': 1799, '1.523': 1805, '1.524': 1812, '1.525': 1818, '1.526': 1826, '1.527': 1833, '1.528': 1840, '1.529': 1848, '1.530': 1854, '1.531': 1861, '1.532': 1867, '1.533': 1873, '1.534': 1876, '1.535': 1882, '1.536': 1890, '1.537': 1899, '1.538': 1905, '1.539': 1915, '1.540': 1920, '1.541': 1927, '1.542': 1934, '1.543': 1941, '1.544': 1948, '1.545': 1956, '1.546': 1964, '1.547': 1970, '1.548': 1977, '1.549': 1983, '1.550': 1991, '1.551': 1996, '1.552': 2003, '1.553': 2010, '1.554': 2017, '1.555': 2025, '1.556': 2033, '1.557': 2040, '1.558': 2047, '1.559': 2053, '1.560': 2054, '1.561': 2060, '1.562': 2066, '1.563': 2074, '1.564': 2080, '1.565': 2087, '1.566': 2095, '1.567': 2101, '1.568': 2110, '1.569': 2117, '1.570': 2124, '1.571': 2130, '1.572': 2138, '1.573': 2145, '1.574': 2152, '1.575': 2159, '1.576': 2165, '1.577': 2171, '1.578': 2178, '2.40': 2185, '2.41': 2191, '2.42': 2199, '2.43': 2205, '2.44': 2212, '2.45': 2218, '2.46': 2226, '2.47': 2232, '2.48': 2240, '2.49': 2248, '2.50': 2254, '2.51': 2262, '2.52': 2269, '2.53': 2275, '2.54': 2284, '2.55': 2289, '2.56': 2298, '2.200': 2304, '2.201': 2309, '2.202': 2315, '2.203': 2323, '2.204': 2328, '2.205': 2335, '2.206': 2342, '2.207': 2348, '2.208': 2355, '2.209': 2363, '2.210': 2370, '2.211': 2375, '2.212': 2381, '2.213': 2387, '2.214': 2392, '2.215': 2398, '2.216': 2405, '2.217': 2412, '2.218': 2418, '2.219': 2425, '2.220': 2431, '2.221': 2437, '2.222': 2443, '2.223': 2449, '2.224': 2455, '2.225': 2462, '2.226': 2468, '2.227': 2477, '2.228': 2484, '2.229': 2490, '2.230': 2496, '2.231': 2502, '2.232': 2509, '2.233': 2511, '2.234': 2517, '2.235': 2523, '2.236': 2529, '2.237': 2534, '2.238': 2541, '2.239': 2548, '2.240': 2555, '2.241': 2564, '2.242': 2571, '2.243': 2578, '2.244': 2584, '2.245': 2590, '2.246': 2596, '2.247': 2603, '2.248': 2610, '2.249': 2617, '2.268': 2624, '2.269': 2630, '2.270': 2637, '2.271': 2644, '2.272': 2651, '2.273': 2658, '2.274': 2666, '2.275': 2672, '2.276': 2678, '2.277': 2684, '2.278': 2692, '2.279': 2698, '2.280': 2704, '2.281': 2711, '2.282': 2719, '2.283': 2726, '2.284': 2734, '2.285': 2740, '2.286': 2747, '2.287': 2754, '2.288': 2761, '2.289': 2771, '2.290': 2779, '2.291': 2787, '2.292': 2793, '2.293': 2800, '2.294': 2807, '2.295': 2813, '2.296': 2821, '2.297': 2827, '2.559': 2834, '2.560': 2839, '2.561': 2845, '2.562': 2850, '2.563': 2857, '2.564': 2865, '2.565': 2871, '2.566': 2878, '2.567': 2887, '2.568': 2894, '2.569': 2900, '2.570': 2907, '2.571': 2914, '2.572': 2921, '2.573': 2927, '2.574': 2933, '2.575': 2939, '2.576': 2945, '2.577': 2952, '2.578': 2958, '2.579': 2966, '2.580': 2972, '2.581': 2978, '2.582': 2983, '2.583': 2990, '2.584': 2998, '2.585': 3004, '2.586': 3010, '2.587': 3016, '2.588': 3022, '2.589': 3031, '2.590': 3039, '2.591': 3046, '2.592': 3053, '2.593': 3060, '2.594': 3067, '2.595': 3075, '2.596': 3082, '2.597': 3088, '2.598': 3095, '2.599': 3103, '2.600': 3110, '2.601': 3116, '2.602': 3122, '2.603': 3130, '2.604': 3137, '2.605': 3144, '2.606': 3151, '2.607': 3157, '2.608': 3164, '2.609': 3171, '2.610': 3177, '2.611': 3184, '2.612': 3190, '2.613': 3198, '2.614': 3201, '2.615': 3207, '2.616': 3213, '2.617': 3220, '2.618': 3227, '2.619': 3234, '2.620': 3242, '4.160': 3247, '4.161': 3252, '4.162': 3259, '4.163': 3266, '4.164': 3273, '4.165': 3279, '4.166': 3286, '4.167': 3293, '4.168': 3299, '4.169': 3306, '4.170': 3314, '4.171': 3320, '4.172': 3326, '4.173': 3333, '4.174': 3340, '4.175': 3346, '4.176': 3354, '4.177': 3362, '4.178': 3368, '4.179': 3375, '4.180': 3381, '4.181': 3389, '4.182': 3395, '4.183': 3403, '4.184': 3411, '4.185': 3417, '4.186': 3424, '4.187': 3431, '4.188': 3439, '4.189': 3445, '4.190': 3452, '4.191': 3457, '4.192': 3464, '4.193': 3472, '4.194': 3478, '4.195': 3486, '4.196': 3492, '4.197': 3499, '4.198': 3505, '4.199': 3511, '4.200': 3518, '4.201': 3524, '4.202': 3531, '4.203': 3539, '4.204': 3546, '4.205': 3552, '4.206': 3558, '4.207': 3564, '4.208': 3572, '4.209': 3579, '4.210': 3585, '4.211': 3592, '4.212': 3598, '4.213': 3605, '4.214': 3612, '4.215': 3619, '4.216': 3625, '4.217': 3631, '4.218': 3638, '4.259': 3644, '4.260': 3650, '4.261': 3656, '4.262': 3663, '4.263': 3670, '4.264': 3676, '4.265': 3682, '4.266': 3688, '4.267': 3695, '4.268': 3702, '4.269': 3709, '4.270': 3717, '4.271': 3726, '4.272': 3733, '4.274': 3739, '4.275': 3746, '4.276': 3751, '4.277': 3756, '4.278': 3764, '4.279': 3770, '4.280': 3778, '4.281': 3785, '4.282': 3791, '4.283': 3799, '4.284': 3805, '4.285': 3813, '4.286': 3822, '4.287': 3828, '4.288': 3835, '4.289': 3843, '4.290': 3851, '4.291': 3857, '4.292': 3864, '4.293': 3870, '4.294': 3877, '4.295': 3883, '4.296': 3890, '4.297': 3896, '4.298': 3903, '4.299': 3909, '4.300': 3917, '4.301': 3922, '4.302': 3928, '4.303': 3934, '4.304': 3940, '4.305': 3945, '4.306': 3952, '4.307': 3961, '4.308': 3967, '4.309': 3973, '4.310': 3980, '4.311': 3988, '4.312': 3994, '4.313': 4000, '4.314': 4011, '4.315': 4019, '4.316': 4025, '4.317': 4035, '4.318': 4042, '4.319': 4050, '4.320': 4057, '4.321': 4063, '4.322': 4070, '4.323': 4077, '4.324': 4084, '4.325': 4092, '4.326': 4098, '4.327': 4106, '4.328': 4114, '4.329': 4121, '4.330': 4128, '4.331': 4134, '4.332': 4141, '4.333': 4149, '4.334': 4154, '4.335': 4160, '4.336': 4169, '4.337': 4178, '4.338': 4185, '4.339': 4192, '4.340': 4199, '4.341': 4205, '4.342': 4211, '4.343': 4217, '4.344': 4223, '4.345': 4229, '4.346': 4234, '4.347': 4243, '4.348': 4249, '4.349': 4255, '4.350': 4263, '4.351': 4269, '4.352': 4276, '4.353': 4283, '4.354': 4290, '4.355': 4297, '4.356': 4305, '4.357': 4312, '4.358': 4319, '4.359': 4326, '4.360': 4334, '4.361': 4338, '4.659': 4345, '4.660': 4354, '4.661': 4361, '4.662': 4369, '4.663': 4376, '4.664': 4382, '4.665': 4390, '4.666': 4396, '4.667': 4402, '4.668': 4408, '4.669': 4416, '4.670': 4423, '4.671': 4431, '4.672': 4437, '4.673': 4444, '4.674': 4451, '4.675': 4458, '4.676': 4467, '4.677': 4474, '4.678': 4481, '4.679': 4489, '4.680': 4496, '4.681': 4504, '4.682': 4513, '4.683': 4520, '4.684': 4528, '4.685': 4535, '4.686': 4541, '4.687': 4548, '4.688': 4554, '4.689': 4560, '4.690': 4567, '4.691': 4575, '4.692': 4581, '4.693': 4587, '4.694': 4593, '4.695': 4600, '4.696': 4608, '4.697': 4616, '4.698': 4622, '4.699': 4628, '4.700': 4635, '4.701': 4641, '4.702': 4649, '4.703': 4657, '4.704': 4666, '4.705': 4673, '6.295': 4681, '6.296': 4688, '6.297': 4694, '6.298': 4701, '6.299': 4707, '6.300': 4713, '6.301': 4719, '6.302': 4726, '6.303': 4731, '6.304': 4739, '6.305': 4746, '6.306': 4753, '6.307': 4759, '6.308': 4766, '6.309': 4773, '6.310': 4782, '6.311': 4789, '6.312': 4796, '6.313': 4801, '6.314': 4807, '6.315': 4815, '6.316': 4821, '6.317': 4827, '6.318': 4836, '6.319': 4844, '6.320': 4851, '6.321': 4858, '6.322': 4863, '6.323': 4870, '6.324': 4877, '6.325': 4886, '6.326': 4894, '6.327': 4901, '6.328': 4906, '6.329': 4914, '6.330': 4920, '6.331': 4926, '6.332': 4933, '6.384': 4940, '6.385': 4949, '6.386': 4957, '6.387': 4964, '6.388': 4972, '6.389': 4981, '6.390': 4989, '6.391': 4995, '6.392': 5002, '6.393': 5008, '6.394': 5015, '6.395': 5022, '6.396': 5029, '6.397': 5035, '6.398': 5042, '6.399': 5048, '6.400': 5056, '6.401': 5061, '6.402': 5067, '6.403': 5073, '6.404': 5080, '6.405': 5087, '6.406': 5095, '6.407': 5102, '6.408': 5109, '6.409': 5115, '6.410': 5121, '6.411': 5129, '6.412': 5136, '6.413': 5142, '6.414': 5148, '6.415': 5156, '6.416': 5163, '6.417': 5169, '6.418': 5175, '6.419': 5182, '6.420': 5188, '6.421': 5195, '6.422': 5201, '6.423': 5208, '6.424': 5213, '6.425': 5219, '6.450': 5226, '6.451': 5233, '6.452': 5241, '6.453': 5247, '6.454': 5255, '6.455': 5262, '6.456': 5268, '6.457': 5274, '6.458': 5282, '6.459': 5292, '6.460': 5298, '6.461': 5308, '6.462': 5316, '6.463': 5322, '6.464': 5329, '6.465': 5337, '6.466': 5346, '6.467': 5352, '6.468': 5358, '6.469': 5364, '6.470': 5370, '6.471': 5378, '6.472': 5384, '6.473': 5391, '6.474': 5397, '6.475': 5403, '6.476': 5409, '6.477': 5410, '6.847': 5415, '6.848': 5422, '6.849': 5428, '6.850': 5434, '6.851': 5440, '6.852': 5448, '6.853': 5453, '6.854': 5460, '6.855': 5466, '6.856': 5472, '6.857': 5478, '6.858': 5485, '6.859': 5492, '6.860': 5499, '6.861': 5505, '6.862': 5513, '6.863': 5521, '6.864': 5528, '6.865': 5536, '6.866': 5543, '6.867': 5549, '6.868': 5556, '6.869': 5563, '6.870': 5569, '6.871': 5577, '6.872': 5584, '6.873': 5591, '6.874': 5596, '6.875': 5603, '6.876': 5611, '6.877': 5617, '6.878': 5625, '6.879': 5632, '6.880': 5640, '6.881': 5646, '6.882': 5654, '6.883': 5661, '6.884': 5667, '6.885': 5674, '6.886': 5680, '6.887': 5687, '6.888': 5694, '6.889': 5700, '6.890': 5707, '6.891': 5714, '6.892': 5723, '6.893': 5730, '6.894': 5737, '6.895': 5742, '6.896': 5749, '6.897': 5757, '6.898': 5763, '6.899': 5771, 'end': -2}
section_list ={'1.1': 'start', '1.2': '1.1', '1.3': '1.2', '1.4': '1.3', '1.5': '1.4', '1.6': '1.5', '1.7': '1.6', '1.8': '1.7', '1.9': '1.8', '1.10': '1.9', '1.11': '1.10', '1.12': '1.11', '1.13': '1.12', '1.14': '1.13', '1.15': '1.14', '1.16': '1.15', '1.17': '1.16', '1.18': '1.17', '1.19': '1.18', '1.20': '1.19', '1.21': '1.20', '1.22': '1.21', '1.23': '1.22', '1.24': '1.23', '1.25': '1.24', '1.26': '1.25', '1.27': '1.26', '1.28': '1.27', '1.29': '1.28', '1.30': '1.29', '1.31': '1.30', '1.32': '1.31', '1.33': '1.32', '1.34': '1.33', '1.35': '1.34', '1.36': '1.35', '1.37': '1.36', '1.38': '1.37', '1.39': '1.38', '1.40': '1.39', '1.41': '1.40', '1.42': '1.41', '1.43': '1.42', '1.44': '1.43', '1.45': '1.44', '1.46': '1.45', '1.47': '1.46', '1.48': '1.47', '1.49': '1.48', '1.50': '1.49', '1.51': '1.50', '1.52': '1.51', '1.53': '1.52', '1.54': '1.53', '1.55': '1.54', '1.56': '1.55', '1.57': '1.56', '1.58': '1.57', '1.59': '1.58', '1.60': '1.59', '1.61': '1.60', '1.62': '1.61', '1.63': '1.62', '1.64': '1.63', '1.65': '1.64', '1.66': '1.65', '1.67': '1.66', '1.68': '1.67', '1.69': '1.68', '1.70': '1.69', '1.71': '1.70', '1.72': '1.71', '1.73': '1.72', '1.74': '1.73', '1.75': '1.74', '1.76': '1.75', '1.77': '1.76', '1.78': '1.77', '1.79': '1.78', '1.80': '1.79', '1.81': '1.80', '1.82': '1.81', '1.83': '1.82', '1.84': '1.83', '1.85': '1.84', '1.86': '1.85', '1.87': '1.86', '1.88': '1.87', '1.89': '1.88', '1.90': '1.89', '1.91': '1.90', '1.92': '1.91', '1.93': '1.92', '1.94': '1.93', '1.95': '1.94', '1.96': '1.95', '1.97': '1.96', '1.98': '1.97', '1.99': '1.98', '1.100': '1.99', '1.101': '1.100', '1.102': '1.101', '1.103': '1.102', '1.104': '1.103', '1.105': '1.104', '1.106': '1.105', '1.107': '1.106', '1.108': '1.107', '1.109': '1.108', '1.110': '1.109', '1.111': '1.110', '1.112': '1.111', '1.113': '1.112', '1.114': '1.113', '1.115': '1.114', '1.116': '1.115', '1.117': '1.116', '1.118': '1.117', '1.119': '1.118', '1.120': '1.119', '1.121': '1.120', '1.122': '1.121', '1.123': '1.122', '1.124': '1.123', '1.125': '1.124', '1.126': '1.125', '1.127': '1.126', '1.128': '1.127', '1.129': '1.128', '1.130': '1.129', '1.131': '1.130', '1.132': '1.131', '1.133': '1.132', '1.134': '1.133', '1.135': '1.134', '1.136': '1.135', '1.137': '1.136', '1.138': '1.137', '1.139': '1.138', '1.140': '1.139', '1.141': '1.140', '1.142': '1.141', '1.143': '1.142', '1.144': '1.143', '1.145': '1.144', '1.146': '1.145', '1.147': '1.146', '1.148': '1.147', '1.149': '1.148', '1.150': '1.149', '1.151': '1.150', '1.152': '1.151', '1.153': '1.152', '1.154': '1.153', '1.155': '1.154', '1.156': '1.155', '1.157': '1.156', '1.158': '1.157', '1.159': '1.158', '1.160': '1.159', '1.161': '1.160', '1.162': '1.161', '1.163': '1.162', '1.164': '1.163', '1.165': '1.164', '1.166': '1.165', '1.167': '1.166', '1.168': '1.167', '1.169': '1.168', '1.170': '1.169', '1.171': '1.170', '1.172': '1.171', '1.173': '1.172', '1.174': '1.173', '1.175': '1.174', '1.176': '1.175', '1.177': '1.176', '1.178': '1.177', '1.179': '1.178', '1.180': '1.179', '1.181': '1.180', '1.182': '1.181', '1.183': '1.182', '1.184': '1.183', '1.185': '1.184', '1.186': '1.185', '1.187': '1.186', '1.188': '1.187', '1.189': '1.188', '1.190': '1.189', '1.191': '1.190', '1.192': '1.191', '1.193': '1.192', '1.194': '1.193', '1.195': '1.194', '1.196': '1.195', '1.197': '1.196', '1.198': '1.197', '1.199': '1.198', '1.200': '1.199', '1.201': '1.200', '1.202': '1.201', '1.203': '1.202', '1.204': '1.203', '1.205': '1.204', '1.206': '1.205', '1.207': '1.206', '1.208': '1.207', '1.209': '1.208', '1.418': '1.209', '1.419': '1.418', '1.420': '1.419', '1.421': '1.420', '1.422': '1.421', '1.423': '1.422', '1.424': '1.423', '1.425': '1.424', '1.426': '1.425', '1.427': '1.426', '1.428': '1.427', '1.429': '1.428', '1.430': '1.429', '1.431': '1.430', '1.432': '1.431', '1.433': '1.432', '1.434': '1.433', '1.435': '1.434', '1.436': '1.435', '1.437': '1.436', '1.438': '1.437', '1.439': '1.438', '1.440': '1.439', '1.494': '1.440', '1.495': '1.494', '1.496': '1.495', '1.497': '1.496', '1.498': '1.497', '1.499': '1.498', '1.500': '1.499', '1.501': '1.500', '1.502': '1.501', '1.503': '1.502', '1.504': '1.503', '1.505': '1.504', '1.506': '1.505', '1.507': '1.506', '1.508': '1.507', '1.509': '1.508', '1.510': '1.509', '1.511': '1.510', '1.512': '1.511', '1.513': '1.512', '1.514': '1.513', '1.515': '1.514', '1.516': '1.515', '1.517': '1.516', '1.518': '1.517', '1.519': '1.518', '1.520': '1.519', '1.521': '1.520', '1.522': '1.521', '1.523': '1.522', '1.524': '1.523', '1.525': '1.524', '1.526': '1.525', '1.527': '1.526', '1.528': '1.527', '1.529': '1.528', '1.530': '1.529', '1.531': '1.530', '1.532': '1.531', '1.533': '1.532', '1.534': '1.533', '1.535': '1.534', '1.536': '1.535', '1.537': '1.536', '1.538': '1.537', '1.539': '1.538', '1.540': '1.539', '1.541': '1.540', '1.542': '1.541', '1.543': '1.542', '1.544': '1.543', '1.545': '1.544', '1.546': '1.545', '1.547': '1.546', '1.548': '1.547', '1.549': '1.548', '1.550': '1.549', '1.551': '1.550', '1.552': '1.551', '1.553': '1.552', '1.554': '1.553', '1.555': '1.554', '1.556': '1.555', '1.557': '1.556', '1.558': '1.557', '1.559': '1.558', '1.560': '1.559', '1.561': '1.560', '1.562': '1.561', '1.563': '1.562', '1.564': '1.563', '1.565': '1.564', '1.566': '1.565', '1.567': '1.566', '1.568': '1.567', '1.569': '1.568', '1.570': '1.569', '1.571': '1.570', '1.572': '1.571', '1.573': '1.572', '1.574': '1.573', '1.575': '1.574', '1.576': '1.575', '1.577': '1.576', '1.578': '1.577', '2.40': '1.578', '2.41': '2.40', '2.42': '2.41', '2.43': '2.42', '2.44': '2.43', '2.45': '2.44', '2.46': '2.45', '2.47': '2.46', '2.48': '2.47', '2.49': '2.48', '2.50': '2.49', '2.51': '2.50', '2.52': '2.51', '2.53': '2.52', '2.54': '2.53', '2.55': '2.54', '2.56': '2.55', '2.200': '2.56', '2.201': '2.200', '2.202': '2.201', '2.203': '2.202', '2.204': '2.203', '2.205': '2.204', '2.206': '2.205', '2.207': '2.206', '2.208': '2.207', '2.209': '2.208', '2.210': '2.209', '2.211': '2.210', '2.212': '2.211', '2.213': '2.212', '2.214': '2.213', '2.215': '2.214', '2.216': '2.215', '2.217': '2.216', '2.218': '2.217', '2.219': '2.218', '2.220': '2.219', '2.221': '2.220', '2.222': '2.221', '2.223': '2.222', '2.224': '2.223', '2.225': '2.224', '2.226': '2.225', '2.227': '2.226', '2.228': '2.227', '2.229': '2.228', '2.230': '2.229', '2.231': '2.230', '2.232': '2.231', '2.233': '2.232', '2.234': '2.233', '2.235': '2.234', '2.236': '2.235', '2.237': '2.236', '2.238': '2.237', '2.239': '2.238', '2.240': '2.239', '2.241': '2.240', '2.242': '2.241', '2.243': '2.242', '2.244': '2.243', '2.245': '2.244', '2.246': '2.245', '2.247': '2.246', '2.248': '2.247', '2.249': '2.248', '2.268': '2.249', '2.269': '2.268', '2.270': '2.269', '2.271': '2.270', '2.272': '2.271', '2.273': '2.272', '2.274': '2.273', '2.275': '2.274', '2.276': '2.275', '2.277': '2.276', '2.278': '2.277', '2.279': '2.278', '2.280': '2.279', '2.281': '2.280', '2.282': '2.281', '2.283': '2.282', '2.284': '2.283', '2.285': '2.284', '2.286': '2.285', '2.287': '2.286', '2.288': '2.287', '2.289': '2.288', '2.290': '2.289', '2.291': '2.290', '2.292': '2.291', '2.293': '2.292', '2.294': '2.293', '2.295': '2.294', '2.296': '2.295', '2.297': '2.296', '2.559': '2.297', '2.560': '2.559', '2.561': '2.560', '2.562': '2.561', '2.563': '2.562', '2.564': '2.563', '2.565': '2.564', '2.566': '2.565', '2.567': '2.566', '2.568': '2.567', '2.569': '2.568', '2.570': '2.569', '2.571': '2.570', '2.572': '2.571', '2.573': '2.572', '2.574': '2.573', '2.575': '2.574', '2.576': '2.575', '2.577': '2.576', '2.578': '2.577', '2.579': '2.578', '2.580': '2.579', '2.581': '2.580', '2.582': '2.581', '2.583': '2.582', '2.584': '2.583', '2.585': '2.584', '2.586': '2.585', '2.587': '2.586', '2.588': '2.587', '2.589': '2.588', '2.590': '2.589', '2.591': '2.590', '2.592': '2.591', '2.593': '2.592', '2.594': '2.593', '2.595': '2.594', '2.596': '2.595', '2.597': '2.596', '2.598': '2.597', '2.599': '2.598', '2.600': '2.599', '2.601': '2.600', '2.602': '2.601', '2.603': '2.602', '2.604': '2.603', '2.605': '2.604', '2.606': '2.605', '2.607': '2.606', '2.608': '2.607', '2.609': '2.608', '2.610': '2.609', '2.611': '2.610', '2.612': '2.611', '2.613': '2.612', '2.614': '2.613', '2.615': '2.614', '2.616': '2.615', '2.617': '2.616', '2.618': '2.617', '2.619': '2.618', '2.620': '2.619', '4.160': '2.620', '4.161': '4.160', '4.162': '4.161', '4.163': '4.162', '4.164': '4.163', '4.165': '4.164', '4.166': '4.165', '4.167': '4.166', '4.168': '4.167', '4.169': '4.168', '4.170': '4.169', '4.171': '4.170', '4.172': '4.171', '4.173': '4.172', '4.174': '4.173', '4.175': '4.174', '4.176': '4.175', '4.177': '4.176', '4.178': '4.177', '4.179': '4.178', '4.180': '4.179', '4.181': '4.180', '4.182': '4.181', '4.183': '4.182', '4.184': '4.183', '4.185': '4.184', '4.186': '4.185', '4.187': '4.186', '4.188': '4.187', '4.189': '4.188', '4.190': '4.189', '4.191': '4.190', '4.192': '4.191', '4.193': '4.192', '4.194': '4.193', '4.195': '4.194', '4.196': '4.195', '4.197': '4.196', '4.198': '4.197', '4.199': '4.198', '4.200': '4.199', '4.201': '4.200', '4.202': '4.201', '4.203': '4.202', '4.204': '4.203', '4.205': '4.204', '4.206': '4.205', '4.207': '4.206', '4.208': '4.207', '4.209': '4.208', '4.210': '4.209', '4.211': '4.210', '4.212': '4.211', '4.213': '4.212', '4.214': '4.213', '4.215': '4.214', '4.216': '4.215', '4.217': '4.216', '4.218': '4.217', '4.259': '4.218', '4.260': '4.259', '4.261': '4.260', '4.262': '4.261', '4.263': '4.262', '4.264': '4.263', '4.265': '4.264', '4.266': '4.265', '4.267': '4.266', '4.268': '4.267', '4.269': '4.268', '4.270': '4.269', '4.271': '4.270', '4.272': '4.271', '4.274': '4.272', '4.275': '4.274', '4.276': '4.275', '4.277': '4.276', '4.278': '4.277', '4.279': '4.278', '4.280': '4.279', '4.281': '4.280', '4.282': '4.281', '4.283': '4.282', '4.284': '4.283', '4.285': '4.284', '4.286': '4.285', '4.287': '4.286', '4.288': '4.287', '4.289': '4.288', '4.290': '4.289', '4.291': '4.290', '4.292': '4.291', '4.293': '4.292', '4.294': '4.293', '4.295': '4.294', '4.296': '4.295', '4.297': '4.296', '4.298': '4.297', '4.299': '4.298', '4.300': '4.299', '4.301': '4.300', '4.302': '4.301', '4.303': '4.302', '4.304': '4.303', '4.305': '4.304', '4.306': '4.305', '4.307': '4.306', '4.308': '4.307', '4.309': '4.308', '4.310': '4.309', '4.311': '4.310', '4.312': '4.311', '4.313': '4.312', '4.314': '4.313', '4.315': '4.314', '4.316': '4.315', '4.317': '4.316', '4.318': '4.317', '4.319': '4.318', '4.320': '4.319', '4.321': '4.320', '4.322': '4.321', '4.323': '4.322', '4.324': '4.323', '4.325': '4.324', '4.326': '4.325', '4.327': '4.326', '4.328': '4.327', '4.329': '4.328', '4.330': '4.329', '4.331': '4.330', '4.332': '4.331', '4.333': '4.332', '4.334': '4.333', '4.335': '4.334', '4.336': '4.335', '4.337': '4.336', '4.338': '4.337', '4.339': '4.338', '4.340': '4.339', '4.341': '4.340', '4.342': '4.341', '4.343': '4.342', '4.344': '4.343', '4.345': '4.344', '4.346': '4.345', '4.347': '4.346', '4.348': '4.347', '4.349': '4.348', '4.350': '4.349', '4.351': '4.350', '4.352': '4.351', '4.353': '4.352', '4.354': '4.353', '4.355': '4.354', '4.356': '4.355', '4.357': '4.356', '4.358': '4.357', '4.359': '4.358', '4.360': '4.359', '4.361': '4.360', '4.659': '4.361', '4.660': '4.659', '4.661': '4.660', '4.662': '4.661', '4.663': '4.662', '4.664': '4.663', '4.665': '4.664', '4.666': '4.665', '4.667': '4.666', '4.668': '4.667', '4.669': '4.668', '4.670': '4.669', '4.671': '4.670', '4.672': '4.671', '4.673': '4.672', '4.674': '4.673', '4.675': '4.674', '4.676': '4.675', '4.677': '4.676', '4.678': '4.677', '4.679': '4.678', '4.680': '4.679', '4.681': '4.680', '4.682': '4.681', '4.683': '4.682', '4.684': '4.683', '4.685': '4.684', '4.686': '4.685', '4.687': '4.686', '4.688': '4.687', '4.689': '4.688', '4.690': '4.689', '4.691': '4.690', '4.692': '4.691', '4.693': '4.692', '4.694': '4.693', '4.695': '4.694', '4.696': '4.695', '4.697': '4.696', '4.698': '4.697', '4.699': '4.698', '4.700': '4.699', '4.701': '4.700', '4.702': '4.701', '4.703': '4.702', '4.704': '4.703', '4.705': '4.704', '6.295': '4.705', '6.296': '6.295', '6.297': '6.296', '6.298': '6.297', '6.299': '6.298', '6.300': '6.299', '6.301': '6.300', '6.302': '6.301', '6.303': '6.302', '6.304': '6.303', '6.305': '6.304', '6.306': '6.305', '6.307': '6.306', '6.308': '6.307', '6.309': '6.308', '6.310': '6.309', '6.311': '6.310', '6.312': '6.311', '6.313': '6.312', '6.314': '6.313', '6.315': '6.314', '6.316': '6.315', '6.317': '6.316', '6.318': '6.317', '6.319': '6.318', '6.320': '6.319', '6.321': '6.320', '6.322': '6.321', '6.323': '6.322', '6.324': '6.323', '6.325': '6.324', '6.326': '6.325', '6.327': '6.326', '6.328': '6.327', '6.329': '6.328', '6.330': '6.329', '6.331': '6.330', '6.332': '6.331', '6.384': '6.332', '6.385': '6.384', '6.386': '6.385', '6.387': '6.386', '6.388': '6.387', '6.389': '6.388', '6.390': '6.389', '6.391': '6.390', '6.392': '6.391', '6.393': '6.392', '6.394': '6.393', '6.395': '6.394', '6.396': '6.395', '6.397': '6.396', '6.398': '6.397', '6.399': '6.398', '6.400': '6.399', '6.401': '6.400', '6.402': '6.401', '6.403': '6.402', '6.404': '6.403', '6.405': '6.404', '6.406': '6.405', '6.407': '6.406', '6.408': '6.407', '6.409': '6.408', '6.410': '6.409', '6.411': '6.410', '6.412': '6.411', '6.413': '6.412', '6.414': '6.413', '6.415': '6.414', '6.416': '6.415', '6.417': '6.416', '6.418': '6.417', '6.419': '6.418', '6.420': '6.419', '6.421': '6.420', '6.422': '6.421', '6.423': '6.422', '6.424': '6.423', '6.425': '6.424', '6.450': '6.425', '6.451': '6.450', '6.452': '6.451', '6.453': '6.452', '6.454': '6.453', '6.455': '6.454', '6.456': '6.455', '6.457': '6.456', '6.458': '6.457', '6.459': '6.458', '6.460': '6.459', '6.461': '6.460', '6.462': '6.461', '6.463': '6.462', '6.464': '6.463', '6.465': '6.464', '6.466': '6.465', '6.467': '6.466', '6.468': '6.467', '6.469': '6.468', '6.470': '6.469', '6.471': '6.470', '6.472': '6.471', '6.473': '6.472', '6.474': '6.473', '6.475': '6.474', '6.476': '6.475', '6.477': '6.476', '6.847': '6.477', '6.848': '6.847', '6.849': '6.848', '6.850': '6.849', '6.851': '6.850', '6.852': '6.851', '6.853': '6.852', '6.854': '6.853', '6.855': '6.854', '6.856': '6.855', '6.857': '6.856', '6.858': '6.857', '6.859': '6.858', '6.860': '6.859', '6.861': '6.860', '6.862': '6.861', '6.863': '6.862', '6.864': '6.863', '6.865': '6.864', '6.866': '6.865', '6.867': '6.866', '6.868': '6.867', '6.869': '6.868', '6.870': '6.869', '6.871': '6.870', '6.872': '6.871', '6.873': '6.872', '6.874': '6.873', '6.875': '6.874', '6.876': '6.875', '6.877': '6.876', '6.878': '6.877', '6.879': '6.878', '6.880': '6.879', '6.881': '6.880', '6.882': '6.881', '6.883': '6.882', '6.884': '6.883', '6.885': '6.884', '6.886': '6.885', '6.887': '6.886', '6.888': '6.887', '6.889': '6.888', '6.890': '6.889', '6.891': '6.890', '6.892': '6.891', '6.893': '6.892', '6.894': '6.893', '6.895': '6.894', '6.896': '6.895', '6.897': '6.896', '6.898': '6.897', '6.899': '6.898', 'end': '6.899', 'start': 'start'}
title = "Vergil, Aeneid (AP Selections)"
section_level =  2
language = "Latin"
book = text.Text(title, section_words, the_text, section_list, section_level, language, True, False)