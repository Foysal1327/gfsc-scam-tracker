from django.core.management.base import BaseCommand
from bogus_banks.scraper import fetch_items
from bogus_banks.utils import *
from bogus_banks.models import ScrapedItem

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = fetch_items()
        new_items, removed_items = detect_changes(data)

        for item in new_items:
            ScrapedItem.objects.create(**item)
        
        if new_items or removed_items:
            # Send notification if there are changes
            send_change_notification(new_items, removed_items)

        self.stdout.write(self.style.SUCCESS(
            f"Scraping done. New: {len(new_items)}, Removed: {len(removed_items)}"))