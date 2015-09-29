from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.test.client import RequestFactory, Client
import logging
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from pydgin_auth.admin import ElasticPermissionModelFactory
from pydgin_auth.permissions import get_authenticated_idx_and_idx_types, get_elastic_model_names


logger = logging.getLogger(__name__)


class PydginAuthTestCase(TestCase):

    multi_db = True

    def setUp(self):
        '''Method called to prepare the test , is called immediately before calling the test method.
        Create test_user and add it to READ group'''
        # Every test needs a client.
        self.client = Client()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.group, created = Group.objects.get_or_create(name='READ')  # @UnusedVariable
        self.user = User.objects.create_user(
            username='test_user', email='test@test.com', password='test_pass')
        self.user.groups.add(self.group)
        ElasticPermissionModelFactory.create_dynamic_models()

    def test_get_elastic_model_names(self):
        idx_keys = ['GENE', 'PUBLICATION', 'MARKER', 'DISEASE']
        idx_type_keys = ['GENE.GENE', 'GENE.PATHWAY', 'GENE.INTERACTIONS', 'PUBLICATION.PUBLICATION', 'MARKER.MARKER',
                         'MARKER.HISTORY', 'MARKER.IC', 'DISEASE.DISEASE']

        model_names = get_elastic_model_names(idx_keys, idx_type_keys)

        self.assertIn('IDX', model_names, 'IDX in dict')
        idx = model_names['IDX']

        self.assertIn('IDX_TYPE', model_names, 'IDX_TYPE in dict')
        idx_type = model_names['IDX_TYPE']

        self.assertEqual(idx['MARKER'], 'marker_idx')
        self.assertEqual(idx['GENE'], 'gene_idx')
        self.assertEqual(idx['PUBLICATION'], 'publication_idx')
        self.assertEqual(idx['DISEASE'], 'disease_idx')

        self.assertIn('marker-marker_idx_type', idx_type['MARKER.MARKER'])
        self.assertIn('marker-rs_merge_idx_type', idx_type['MARKER.HISTORY'])
        self.assertIn('marker-immunochip_idx_type', idx_type['MARKER.IC'])

        self.assertIn('gene-gene_idx_type', idx_type['GENE.GENE'])
        self.assertIn('gene-pathway_genesets_idx_type', idx_type['GENE.PATHWAY'])
        self.assertIn('gene-interactions_idx_type', idx_type['GENE.INTERACTIONS'])

        self.assertIn('publication-publication_idx_type', idx_type['PUBLICATION.PUBLICATION'])

        self.assertIn('disease-disease_idx_type', idx_type['DISEASE.DISEASE'])

    def test_get_authenticated_idx_and_idx_types(self):
        idx_keys = ['GENE', 'PUBLICATION', 'MARKER', 'DISEASE']
        idx_type_keys = ['GENE.GENE', 'GENE.PATHWAY', 'GENE.INTERACTIONS', 'PUBLICATION.PUBLICATION', 'MARKER.MARKER',
                         'MARKER.HISTORY', 'MARKER.IC', 'DISEASE.DISEASE']

        # We have not set the permissions yet, so we expect to get back everything
        (idx_keys_auth, idx_type_keys_auth) = get_authenticated_idx_and_idx_types(self.user, idx_keys, idx_type_keys)

        self.assertIn('MARKER', idx_keys_auth)
        self.assertIn('GENE', idx_keys_auth)
        self.assertIn('PUBLICATION', idx_keys_auth)
        self.assertIn('DISEASE', idx_keys_auth)

        self.assertIn('GENE.GENE', idx_type_keys_auth)
        self.assertIn('GENE.PATHWAY', idx_type_keys_auth)
        self.assertIn('GENE.INTERACTIONS', idx_type_keys_auth)

        self.assertIn('PUBLICATION.PUBLICATION', idx_type_keys_auth)

        self.assertIn('MARKER.MARKER', idx_type_keys_auth)
        self.assertIn('MARKER.MARKER', idx_type_keys_auth)
        self.assertIn('MARKER.MARKER', idx_type_keys_auth)

        self.assertIn('DISEASE.DISEASE', idx_type_keys_auth)

        # Create test_dil user and assign the user to DIL group
        dil_group, created = Group.objects.get_or_create(name='DIL')
        self.assertTrue(created)
        dil_user = User.objects.create_user(
            username='test_dil', email='test_dil@test.com', password='test123')
        dil_user.groups.add(dil_group)
        self.assertTrue(dil_user.groups.filter(name='DIL').exists())

        all_groups_of_dil_user = dil_user.groups.values_list('name', flat=True)
        self.assertTrue("DIL" in all_groups_of_dil_user, "Found DIL in groups")
        self.assertTrue("READ" in all_groups_of_dil_user, "Found READ in groups")

        # create the content type
        test_model = 'disease_idx'

        # create permissions on models and retest again to check if the idx could be seen
        content_type, created = ContentType.objects.get_or_create(  # @UnusedVariable
            model=test_model, app_label=ElasticPermissionModelFactory.PERMISSION_MODEL_APP_NAME,
        )

        # create permission and assign ...Generally we create via admin interface
        can_read_permission, create = Permission.objects.get_or_create(  # @UnusedVariable
            codename='can_read_disease_idx',
            name='Can Read disease Idx',
            content_type=content_type)

        # check if you can see the index
        (idx_keys_auth, idx_type_keys_auth) = get_authenticated_idx_and_idx_types(self.user, idx_keys, idx_type_keys)

        self.assertNotIn('DISEASE', idx_keys_auth)
        self.assertNotIn('DISEASE.DISEASE', idx_type_keys_auth)

        # now grant access to test_dil and check if the user can see the index
        # Add the permission to dil_group
        dil_group.permissions.add(can_read_permission)
        dil_user = get_object_or_404(User, pk=dil_user.id)
        available_group_perms = dil_user.get_group_permissions()
        self.assertTrue('elastic.can_read_disease_idx' in available_group_perms,
                        "dil_user has perm 'elastic.can_read_disease_idx' ")

        # check if you can see the index
        (idx_keys_auth, idx_type_keys_auth) = get_authenticated_idx_and_idx_types(dil_user, idx_keys, idx_type_keys)
        self.assertIn('DISEASE', idx_keys_auth, 'dil_user can see the disease_idx')

        # test type now

        # create the content type
        test_model_type = 'marker-rs_merge_idx_type'

        # create permissions on models and retest again to check if the idx could be seen
        content_type, created = ContentType.objects.get_or_create(  # @UnusedVariable
            model=test_model_type, app_label=ElasticPermissionModelFactory.PERMISSION_MODEL_APP_NAME,
        )

        # create permission and assign ...Generally we create via admin interface
        can_read_permission, create = Permission.objects.get_or_create(  # @UnusedVariable
            codename='can_read_marker-rs_merge',
            name='Can Read marker rs merge Idx type',
            content_type=content_type)

        # check if you can see the index type
        (idx_keys_auth, idx_type_keys_auth) = get_authenticated_idx_and_idx_types(dil_user, idx_keys, idx_type_keys)
        self.assertNotIn('MARKER.HISTORY', idx_keys_auth)

        # now grant access to test_dil and check if the user can see the index
        # Add the permission to dil_group
        dil_group.permissions.add(can_read_permission)
        dil_user = get_object_or_404(User, pk=dil_user.id)
        available_group_perms = dil_user.get_group_permissions()
        self.assertTrue('elastic.can_read_marker-rs_merge' in available_group_perms,
                        "dil_user has perm 'elastic.can_read_marker-rs_merge' ")

        # check if you can see the index type
        (idx_keys_auth, idx_type_keys_auth) = get_authenticated_idx_and_idx_types(dil_user, idx_keys, idx_type_keys)
        self.assertIn('MARKER.HISTORY', idx_type_keys_auth)


#     def test_routers(self):
#         '''Test if the routers are available to route to different databases'''
#         logger.debug('running test_routers')
#         self.original_routers = router.routers
#
#         routers = []
#         for router_ in self.original_routers:
#             routers.append(router_.__class__.__name__)
#
#         self.assertTrue('AuthRouter' in routers, "Found AuthRouter in routers")
#         self.assertTrue('DefaultRouter' in routers, "Found DefaultRouter in routers")

    def test_login(self):
        '''Test login. First try to login with invalid credentials, and try again with right credentials again'''
        logger.debug('running test_login')
        response = self.client.get('/accounts/login/', follow=True)
        # check if redirected to login
        self.assertTemplateUsed(response, 'registration/login.html')

        response = self.client.post('/accounts/login/', {'username': 'test_invalid', 'password': 'test_pass'})
        self.assertTrue(response.status_code, "200")
        response_string = response.content.decode('utf-8')
        self.assertTrue("The username and password provided is not valid/recognised" in response_string)

        response = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test_pass'})
        self.assertTrue(response.status_code, "200")
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(User.objects.get(id=self.client.session['_auth_user_id']).username, 'test_user')

    def test_register_user(self):
        '''Test registration. First try to login with out agreeing to terms and
        try to register again with is_terms_agreed set'''
        logger.debug('running test_register_user')
        response = self.client.get('/accounts/register/', follow=True)
        # check if redirected to registration page
        self.assertTemplateUsed(response, 'registration/registration_form.html')
        self.client.post('/accounts/register/',
                         {'username': 'new_user', 'email': 'newuser@new.com',
                          'password1': 'newtest', 'password2': 'newtest'})
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        user_present = False
        for user in users:
            if user.username == 'new_user':
                user_present = True
                break

        self.assertFalse(user_present, "new_user not in Users before is_terms_agreed")

        self.client.post('/accounts/register/',
                         {'username': 'new_user', 'email': 'newuser@new.com',
                          'password1': 'newtest', 'password2': 'newtest', 'is_terms_agreed': '1'})
        self.assertEqual(response.status_code, 200)
        users = User.objects.all()
        for user in users:
            if user.username == 'new_user':
                user_present = True
                break

        self.assertTrue(user_present, "new_user in Users list after is_terms_agreed")

    def test_create_groups(self):
        '''Test if we get back the READ group without creating it (created is false)
        and other groups should get created (created is True)'''
        read_group, created = Group.objects.get_or_create(name='READ')
        self.assertEqual(read_group.name, "READ")
        self.assertEqual(created, False)

        dil_group, created = Group.objects.get_or_create(name='DIL')
        self.assertEqual(dil_group.name, "DIL")
        self.assertTrue(created)

        curator_group, created = Group.objects.get_or_create(name='CURATOR')
        self.assertEqual(curator_group.name, "CURATOR")
        self.assertTrue(created)

        pydgin_admin_group, created = Group.objects.get_or_create(name='ADMIN')
        self.assertEqual(pydgin_admin_group.name, "ADMIN")
        self.assertTrue(created)
