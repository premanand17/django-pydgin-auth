''' Test for elastic model factory '''
from django.test import TestCase, override_settings

from elastic.tests.settings_idx import OVERRIDE_SETTINGS
from pydgin_auth.elastic_model_factory import ElasticPermissionModelFactory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group


@override_settings(ELASTIC=OVERRIDE_SETTINGS)
def setUpModule():
    pass


@override_settings(ELASTIC=OVERRIDE_SETTINGS)
def tearDownModule():
    pass


class ElasticModelFactoryTest(TestCase):

    def setUp(self):
        # create elastic models
        ElasticPermissionModelFactory.create_dynamic_models()
        # create the default group READ
        Group.objects.get_or_create(name='READ')

    def tearDown(self):
        pass

    def test_elastic_models(self):
        # check model names are created correctly
        all_models, all_types = ElasticPermissionModelFactory.get_elastic_model_names(as_list=True)

        self.assertTrue('disease_idx' in all_models, "disease_idx exists ")
        self.assertTrue('gene_idx' in all_models, "gene_idx exists ")
        self.assertTrue('marker_idx' in all_models, "marker_idx exists ")
        self.assertTrue('marker-marker_idx_type' in all_types, "marker-marker_idx_type exists ")
        self.assertTrue('marker-rs_merge_idx_type' in all_types, "marker-rs_merge_idx_type exists ")

        for model in all_models:
            # check content types are created correctly...
            # created should be false as the content type is already created in the setup
            content_type, created = ContentType.objects.get_or_create(
                model=model, app_label="elastic",
            )
            self.assertEqual(model, content_type.name, "Model and content_type are equal : " + str(content_type))
            self.assertFalse(created, "Model already created and exists " + str(content_type))
