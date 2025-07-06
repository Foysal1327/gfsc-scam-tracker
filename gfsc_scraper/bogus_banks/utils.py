from .models import ScrapedItem
from django.core.mail import send_mail
from django.conf import settings

def detect_changes(fetched_items):
    current = {item.name: item for item in ScrapedItem.objects.all()}
    fetched_names = set()
    new = []
    removed = []
    
    for entry in fetched_items:
        name = entry['name']
        fetched_names.add(name)
        existing = current.get(name)

        if not existing:
            new.append(entry)
        else:
            # Update existing if content differs
            changed = False
            if existing.domains != entry['domains'] or existing.notes != entry['notes']:
                existing.domains = entry['domains']
                existing.notes = entry['notes']
                existing.save()
                changed = True

    removed_names = set(current.keys()) - fetched_names
    removed = [current[name] for name in removed_names]

    return new, removed

def send_change_notification(new_items, removed_items):
    if not new_items and not removed_items:
        return

    subject = "GFSC Scraper: Changes Detected"
    lines = []
    if new_items:
        lines.append(f"New items ({len(new_items)}):")
        for item in new_items:
            lines.append(f"- {item['name']}")
    if removed_items:
        lines.append(f"\nRemoved items ({len(removed_items)}):")
        for item in removed_items:
            lines.append(f"- {item['name']}")
    message = "\n".join(lines)
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        getattr(settings, 'NOTIFY_EMAILS', []),
        fail_silently=False,
    )