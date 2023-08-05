from django.apps import apps
from django.core.management.base import BaseCommand
from django_postgres_model_constraints.utils import get_add_foreign_key_constraint_statements


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('model', nargs='+', help='model')

    def handle(self, *args, **options):
        for arg in options['model']:
            app_label = arg.split('.')[0]
            model_name = arg.split('.')[1]
            model = apps.get_model(app_label=app_label, model_name=model_name)
            statements = get_add_foreign_key_constraint_statements(model)
            if statements:
                print("\n\n".join(statements))
