from django.core.management.base import BaseCommand
from crud_operations.models import Employee, Position
from crud_operations.forms import PositionForm
import json

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
          
        for i in ['Junior2','Senior2']:
            # model = Position(title = i)
            # model.save()
            item = {}

            item['title'] = i
            try:
                form = PositionForm(item)
                form.save()
            except Exception as e:
                print(item)
                print('------------------------')
                print(e)