from django.test import TestCase
from django.core.management import call_command
from elastic.tests.settings_idx import IDX
from elastic.elastic_settings import ElasticSettings

from elastic.search import Search, ElasticQuery
from elastic.query import Query, TermsFilter, BoolQuery
import requests
from django.contrib.auth.models import User, Group
from pydgin_auth.permissions import get_user_groups
from django.test.client import Client, RequestFactory
# Get an instance of a logger
import logging
import json
logger = logging.getLogger(__name__)


class PydginAuthElasticTestCase(TestCase):

    multi_db = True

    def setUp(self):
        ''' Run the index loading script to create test indices and
        create test repository '''

        region_key = 'PRIVATE_REGIONS_GFF'
        if region_key in IDX.keys():
            idx_kwargs = IDX[region_key]
            self.index_name = idx_kwargs['indexName']
            print("Index name ============" + str(self.index_name))
            call_command('index_search', **idx_kwargs)

        '''Create test user and test client'''
        # Every test needs a client.
        self.client = Client()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.default_group = Group.objects.create(name='READ')

        self.user = User.objects.create_user(
            username='test_user', email='test@test.com', password='test_pass')
        self.user.groups.add(self.default_group)

    def tearDown(self):
        ''' Remove loaded test indices and test repository. '''

        key = 'PRIVATE_REGIONS_GFF'
        if key in IDX.keys():
            print(ElasticSettings.url() + '/' + IDX[key]['indexName'])
            requests.delete(ElasticSettings.url() + '/' + IDX[key]['indexName'])

    def test_region_idx_loader(self):
        ''' Test loader has created and populated indices.  '''

        key = 'PRIVATE_REGIONS_GFF'

        if key in IDX.keys():
            idx = IDX[key]['indexName']
            Search.index_refresh(idx)
            self.assertTrue(Search.index_exists(idx=idx), 'Index exists: '+idx)
            ndocs = Search(idx=idx).get_count()['count']
            self.assertTrue(ndocs > 0, "Elastic count documents in " + idx + ": " + str(ndocs))

        # Query the index for private regions

    def test_elastic_group_name(self):
        '''
        gff row:
        chr4    immunobase      region  122061159       122684373       .       .       .
        Name=4q27;region_id=803;region_group=["DIL"]
        idx doc:
         "_source":{"attr": {"region_id": "803", "group_name": "[\"DIL\"]", "Name": "4q27"},
         "seqid": "chr4", "source": "immunobase", "type": "region",
         "score": ".", "strand": ".", "phase": ".", "start": 122061159, "end": 122684373}
        idx_query:
        Private(in given group) OR Public
        -d '{"query":{"filtered":{"filter":{"bool": {
                                            "should": [
                                                        {"terms": {"group_name":["dil"]}},
                                                        { "missing": { "field": "group_name"   }}
                                                      ]
                                                    }}}}}'
        Private(in given group):
        -d '{"query":{"filtered":{"filter":{"terms":{"group_name":["dil"]}}}}}'
        Public:
        -d {'query': {'filtered': {'filter': {'missing': {'field': 'group_name'}},
-                         'query': {'term': {'match_all': '{}'}}}}}
        '''
        # get the groups for the given user
        response = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test_pass'})
        self.assertTrue(response.status_code, "200")

        logged_in_user = User.objects.get(id=self.client.session['_auth_user_id'])
        if logged_in_user and logged_in_user.is_authenticated():
            user_groups = get_user_groups(logged_in_user)
            self.assertTrue('READ' in user_groups, "user present in READ group")
            # make sure the user is not yet in DIL group
            self.assertFalse('DIL' in user_groups, "user not present in DIL group")

        group_names = get_user_groups(logged_in_user)
        if 'READ' in group_names : group_names.remove('READ')  # @IgnorePep8
        group_names = [x.lower() for x in group_names]
        self.assertTrue(len(group_names) == 0, "No group present")

        # Match all query
        # as there is not group we do a match all
        query = ElasticQuery(Query.match_all())
        expected_query_string = {"query": {"match_all": {}}}
        self.assertJSONEqual(json.dumps(query.query), json.dumps(expected_query_string), "Query string matched")

        Search.index_refresh(self.index_name)
        elastic = Search(query, idx=self.index_name)
        docs = elastic.search().docs
        self.assertTrue(len(docs) == 12, "Elastic string query retrieved all public regions")

        # Filtered query for group names
        # add the user to DIL group and get the query string
        self.dil_group = Group.objects.create(name='DIL')
        logged_in_user.groups.add(self.dil_group)
        group_names = get_user_groups(logged_in_user)
        if 'READ' in group_names : group_names.remove('READ')  # @IgnorePep8
        group_names = [x.lower() for x in group_names]
        self.assertTrue(len(group_names) > 0, "More than 1 group present")
        self.assertTrue("dil" in group_names, "DIL group present")

        # retrieves all docs with missing file group_name - 11 docs
        terms_filter = TermsFilter.get_missing_terms_filter("field", "group_name")
        query = ElasticQuery.filtered(Query.match_all(), terms_filter)
        elastic = Search(query, idx=self.index_name)
        docs = elastic.search().docs
        self.assertTrue(len(docs) == 11, "Elastic string query retrieved all public regions")

        # build filtered boolean query to bring all public docs + private docs 11+1 = 12 docs
        query_bool = BoolQuery()
        query_bool.should(Query.missing_terms("field", "group_name")) \
                  .should(Query.terms("group_name", group_names).query_wrap())

        query = ElasticQuery.filtered_bool(Query.match_all(), query_bool)
        elastic = Search(query, idx=self.index_name)
        docs = elastic.search().docs
        self.assertTrue(len(docs) == 12, "Elastic string query retrieved both public + private regions")

        terms_filter = TermsFilter.get_terms_filter("group_name", group_names)
        query = ElasticQuery.filtered(Query.match_all(), terms_filter)
        elastic = Search(query, idx=self.index_name)
        docs = elastic.search().docs
        self.assertTrue(len(docs) == 1, "Elastic string query retrieved one private regions")
        self.assertEqual(docs[0].attr['Name'], "4q27", "type matched region")
        self.assertEqual(docs[0].attr['region_id'], "803", "type matched region")
        self.assertEqual(docs[0].attr['group_name'], "[\"DIL\"]", "type matched region")
