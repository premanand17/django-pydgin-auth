''' Used to define Elastic mapping and index data. '''
from django.core.management.base import BaseCommand
from optparse import make_option
import logging
from django.contrib.contenttypes.models import ContentType

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    ''' Elastic index model management tool.
    Note: Extend it to delete the index type from elastic server as well.
    '''
    help = "Use it to remove stale Elastic index types - models\n\n" \
           "Options:\n" \
           " --applabel [app name] " \

    option_list = BaseCommand.option_list + (
        make_option('--applabel',
                    dest='applabel',
                    help='applabel to do the cleanup'),
        )

    def handle(self, *args, **options):
        ''' Handle the user options to remove stale contenttypes -'''
        if options['applabel']:
            self.delete_stale_contenttypes(self, *args, **options)
        else:
            print(help)

    def delete_stale_contenttypes(self, *args, **options):
        print('delete_stale_contenttypes called')
        ContentType.objects.clear_cache()

        # find out the models to be deleted here, by setting some criteria (time limit)
        # Assuming that you have the model to be delete
        # models2go = ['cp_stats_ud-ud-tmpvsl4_inn_idx_type']
        models2go = self.get_models_to_delete()
        # models2go = ['disease_idx'] # pydgin

        for ct in ContentType.objects.filter(app_label=options['applabel']):
            print(ct.name)
            if str(ct.name) in models2go:
                print('Matched, finding permissions for %s  %s' % (str(ct.name), str(ct.id)))
                print("deleting %s" % ct)
                ct.delete()

    def get_models_to_delete(self):
        '''Get models to delete'''
        models2go = ['cp_stats_ud-ud-tmpvsl4_inn_idx_type']
        return models2go
