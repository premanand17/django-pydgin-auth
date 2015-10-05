

OVERRIDE_SETTINGS_CHICP = \
    {'default': {
        'ELASTIC_URL': 'http://dev-elastic1:9200/',
        'IDX': {
            'CP_STATS_UD': {
                'name': 'cp:hg19_userdata_bed',
                'label': 'User Data',
                'idx_type': {},
                'auth_public': True,
                },
            'CP_STATS_IC': {
                'name': 'cp:hg19_immunochip_bed',
                'label': 'ImmunoChip',
                'idx_type': {
                    'ic-atd_cooper': {'label': "ATD - Cooper et al.", 'type': 'atd_cooper', 'auth_public': True},
                    'ic-cel_trynka': {'label': "CEL - Trynka et al.", 'type': 'cel_trynka', 'auth_public': True},
                    'ic-jia_hinks_uk': {'label': "JIA - Hinks et al. UK", 'type': 'jia_hinks_uk'},
                    'ic-ms_imsgc': {'label': "MS - IMSGC et al.", 'type': 'ms_imsgc'},
                    'ic-nar_faraco': {'label': "NAR - Faraco et al.", 'type': 'nar_faraco'},
                    'ic-pbc_liu': {'label': "PBC - Liu et al.", 'type': 'pbc_liu', 'auth_public': True},
                    'ic-ra_eyre': {'label': "RA - Eyre et al.", 'type': 'ra_eyre', 'auth_public': True},
                    'ic-t1d_onengut': {'label': 'T1D - Onengut et al.', 'type': 't1d_onengut', 'auth_public': True},
                },
                'auth_public': True,
            },
            'CP_STATS_GWAS': {
                'name': 'cp:hg19_gwas_bed',
                'label': 'GWAS Statistic',
                'idx_type': {
                    'gwas-dubois': {'label': 'CEL - Dubois et al.', 'type': 'cel_dubois','auth_public': True},
                    'gwas-franke': {'label': 'CRO - Franke et al.', 'type': 'cro_franke','auth_public': True},
                    'gwas-imsgc': {'label': 'MS - IMSGC et al.', 'type': 'ms_imsgc','auth_public': True},
                    'gwas-okada': {'label': 'RA - Okada et al.', 'type': 'ra_okada'},
                    'gwas-stahl': {'label': 'RA - Stahl et al.', 'type': 'ra_stahl'},
                    'gwas-barrett': {'label': 'T1D - Barrett et al.', 'type': 't1d_barrett'},
                    'gwas-cooper': {'label': 'T1D - Cooper et al.', 'type': 't1d_cooper','auth_public': True},
                    'gwas-anderson': {'label': 'UC - Anderson et al.', 'type': 'uc_anderson'},
                },
            'auth_public': True,
            },
            'TARGET_CHICAGO': {'name': 'cp:hg19_chicago_targets', 'label': 'CHICAGO',
                               'auth_public': True, },
            'TARGET_MIFSUD': {'name': 'cp:hg19_mifsud_gt_pm', 'label': 'Mifsud et al.', },
            'TARGET_MARTIN': {'name': 'cp:hg19_martin_pm', 'label': 'Martin et al.',
                              'auth_public': True, },
        },
        'TEST': 'auto_tests',
        'REPOSITORY': 'my_backup',
    }
    }


OVERRIDE_SETTINGS_PYDGIN = \
    {'default': {
        'ELASTIC_URL': 'http://dev-elastic1:9200/',
        'IDX': {
            'GENE': {
                'name': 'genes_hg38_v0.0.2',
                'idx_type': {
                    'GENE': {'type': 'gene', 'search': True, 'auth_public': True},
                    'PATHWAY': {'type': 'pathway_genesets', 'search': True},
                    'INTERACTIONS': {'type': 'interactions'}
                },
                'label': 'gene related indices',
                'suggester': True,
                'auth_public': True
            },
            'PUBLICATION': {
                'name': 'publications_v0.0.4',
                'idx_type': {
                    'PUBLICATION': {'type': 'publication', 'search': True}
                },
                'suggester': True,
                'auth_public': True
            },
            'MARKER': {
                'name': 'dbsnp144',
                'idx_type': {
                    'MARKER': {'type': 'marker', 'description': 'dbsnp', 'search': True, 'auth_public': True},
                    'HISTORY': {'type': 'rs_merge', 'description': 'snp merge history',
                                'search': True, 'auth_public': True},
                    'IC': {'type': 'immunochip', 'search': True}
                },
                'suggester': True,
                'auth_public': True
            },
            'DISEASE': {
                'name': 'disease',
                'idx_type': {
                    'DISEASE': {'type': 'disease', 'search': True}
                },
                'suggester': True,
            },
        },
        'TEST': 'auto_tests',
        'REPOSITORY': 'my_backup',
        'TEST_REPO_DIR': '/ipswich/data/pydgin/elastic/repos/test_snapshot/',
    }
    }
