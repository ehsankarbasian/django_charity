from django.core.management.base import BaseCommand, CommandError
from App1.Components.init_test_db import *


def init_default_db():
    init_db_user()
    print("Initialized: users")
    init_db_profile()
    print("Initialized: userProfiles")
    init_db_transaction()
    print("Initialized: Transactions")
    init_db_storeManagement()
    print("Initialized: StoreElements(category, subcategory, product)")
    init_db_donateIn()
    print("Initialized: donatesIn")
    init_db_event()
    print("Initialized: events")


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("Processing ...")
            print("Please wait")
            print("")
            init_default_db()
            print("")
            print("Done !!!")
        except Exception:
            raise CommandError("An error occurred")
