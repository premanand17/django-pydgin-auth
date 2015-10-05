''' Test for elastic model factory '''
from django.test import TestCase, override_settings

from django.contrib.auth.models import Group
from pydgin_auth.tests.settings_idx import OVERRIDE_SETTINGS_CHICP,\
    OVERRIDE_SETTINGS_PYDGIN
from pydgin_auth.elastic_model_factory import ElasticPermissionModelFactory as elastic_factory


def setUp(self):
    # create the default group READ
    Group.objects.get_or_create(name='READ')


class ElasticModelFactoryTest(TestCase):

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_CHICP)
    def test_get_idx_and_idx_type_keys_cp(self):
        '''create idx and idxtype keys for chicp'''
        elastic_factory.create_dynamic_models()
        # usually you can get the IDX dict via ElasticSettings.attrs().get('IDX')
        (idx_keys, idx_type_keys) = elastic_factory.get_idx_and_idx_type_keys(auth_public=False)

        # private idx
        self.assertIn('TARGET_MIFSUD', idx_keys)

        # private idx types
        self.assertIn('CP_STATS_IC.ic-ms_imsgc', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-jia_hinks_uk', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-nar_faraco', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-barrett', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-anderson', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-stahl', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-okada', idx_type_keys)

        # public idx
        (idx_keys, idx_type_keys) = elastic_factory.get_idx_and_idx_type_keys(auth_public=True)

        # private idx
        self.assertIn('CP_STATS_IC', idx_keys)
        self.assertIn('CP_STATS_GWAS', idx_keys)
        self.assertIn('TARGET_MARTIN', idx_keys)
        self.assertIn('CP_STATS_UD', idx_keys)
        self.assertIn('TARGET_CHICAGO', idx_keys)

        # public idx and idx_type
        self.assertIn('CP_STATS_IC.ic-t1d_onengut', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-atd_cooper', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-cel_trynka', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-ra_eyre', idx_type_keys)
        self.assertIn('CP_STATS_IC.ic-pbc_liu', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-cooper', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-dubois', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-franke', idx_type_keys)
        self.assertIn('CP_STATS_GWAS.gwas-imsgc', idx_type_keys)

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_PYDGIN)
    def test_get_idx_and_idx_type_keys_pydgin(self):
        '''create idx and idxtype keys for chicp'''
        elastic_factory.create_dynamic_models()

        # get all private idx and keys
        (idx_keys, idx_type_keys) = elastic_factory.get_idx_and_idx_type_keys(auth_public=False)

        # private idx keys
        self.assertIn('DISEASE', idx_keys)

        # public idx keys
        self.assertNotIn('GENE', idx_keys)
        self.assertNotIn('MARKER', idx_keys)
        self.assertNotIn('PUBLICATION', idx_keys)

        # private idx type keys
        self.assertIn('DISEASE.DISEASE', idx_type_keys)
        self.assertIn('GENE.PATHWAY', idx_type_keys)
        self.assertIn('GENE.INTERACTIONS', idx_type_keys)
        self.assertIn('PUBLICATION.PUBLICATION', idx_type_keys)

        # public idx type keys
        self.assertNotIn('GENE.GENE', idx_type_keys)
        self.assertNotIn('MARKER.MARKER', idx_type_keys)
        self.assertNotIn('MARKER.MARKER', idx_type_keys)
        self.assertNotIn('MARKER.MARKER', idx_type_keys)

        # get all public idx and keys
        (idx_keys, idx_type_keys) = elastic_factory.get_idx_and_idx_type_keys(auth_public=True)

        # private idx key
        self.assertNotIn('DISEASE', idx_keys)

        # public idx key
        self.assertIn('MARKER', idx_keys)
        self.assertIn('PUBLICATION', idx_keys)
        self.assertIn('GENE', idx_keys)

        # private idx type keys
        self.assertNotIn('DISEASE.DISEASE', idx_type_keys)
        self.assertNotIn('GENE.PATHWAY', idx_type_keys)
        self.assertNotIn('GENE.INTERACTIONS', idx_type_keys)
        self.assertNotIn('PUBLICATION.PUBLICATION', idx_type_keys)

        # public idx type keys
        self.assertIn('GENE.GENE', idx_type_keys)
        self.assertIn('MARKER.MARKER', idx_type_keys)
        self.assertIn('MARKER.MARKER', idx_type_keys)
        self.assertIn('MARKER.MARKER', idx_type_keys)

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_PYDGIN)
    def test_get_elastic_model_names_pydgin(self):
        '''check whether the right model names are created for pydgin'''

        # for pydgin, returns only models for private idx and idx_types
        (model_names_idx, model_names_idx_types) = elastic_factory.get_elastic_model_names()
        model_names = model_names_idx + model_names_idx_types

        self.assertIn('DISEASE_IDX', model_names)
        self.assertIn('GENE-PATHWAY_IDX_TYPE', model_names)
        self.assertIn('MARKER-IC_IDX_TYPE', model_names)
        self.assertIn('DISEASE-DISEASE_IDX_TYPE', model_names)

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_CHICP)
    def test_get_elastic_model_names_chicp(self):
        '''check whether the right model names are created for chicp'''
        elastic_factory.create_dynamic_models()
        (idx_keys, idx_type_keys) = elastic_factory.get_idx_and_idx_type_keys(auth_public=False)

        (model_names_idx, model_names_idx_types) = elastic_factory.get_elastic_model_names(
            idx_keys=idx_keys,
            idx_type_keys=idx_type_keys)

        self.assertIn('TARGET_MIFSUD_IDX', model_names_idx)
        self.assertIn('CP_STATS_IC-ic-ms_imsgc_IDX_TYPE', model_names_idx_types)
        self.assertIn('CP_STATS_IC-ic-nar_faraco_IDX_TYPE', model_names_idx_types)
        self.assertIn('CP_STATS_GWAS-gwas-okada_IDX_TYPE', model_names_idx_types)
        self.assertIn('CP_STATS_GWAS-gwas-stahl_IDX_TYPE', model_names_idx_types)

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_PYDGIN)
    def test_elastic_models_pydgin(self):
        '''check whether the right models are created for pydgin'''
        elastic_factory.create_dynamic_models()
        # check model names are created correctly

        expected_models = ['DISEASE_IDX', 'GENE-PATHWAY_IDX_TYPE', 'GENE-INTERACTIONS_IDX_TYPE',
                           'MARKER-IC_IDX_TYPE', 'PUBLICATION-PUBLICATION_IDX_TYPE', 'DISEASE-DISEASE_IDX_TYPE']

        existing_models = elastic_factory.get_db_models(existing=True)

        for model in expected_models:
            self.assertIn(model, existing_models, 'Model exists: ' + model)

    @override_settings(ELASTIC=OVERRIDE_SETTINGS_PYDGIN)
    def test_get_keys_from_model_names(self):

        idx_model_names = ['DISEASE_IDX', 'GENE_IDX']
        idx_type_model_names = ['GENE-INTERACTIONS_IDX_TYPE', 'MARKER-IC_IDX_TYPE', 'PUBLICATION-PUBLICATION_IDX_TYPE']

        (idx_keys, idx_type_keys) = elastic_factory.get_keys_from_model_names(idx_model_names,
                                                                              idx_type_model_names)
        self.assertTrue('DISEASE' in idx_keys, 'Got right idx key : DISEASE')
        self.assertTrue('GENE' in idx_keys, 'Got right idx key : GENE')

        self.assertTrue('GENE.INTERACTIONS' in idx_type_keys, 'Got right idx type key : GENE.INTERACTIONS')
        self.assertTrue('MARKER.IC' in idx_type_keys, 'Got right idx type key : MARKER.IC')
        self.assertTrue('PUBLICATION.PUBLICATION' in idx_type_keys, 'Got right idx type key : PUBLICATION.PUBLICATION')
