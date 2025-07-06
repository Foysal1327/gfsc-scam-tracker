from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ScrapedItem
from .scraper import fetch_items
from .utils import*
from django.core.paginator import Paginator

@login_required
def item_list(request):
    # items = ScrapedItem.objects.all().order_by('-updated_at')
    # return render(request, 'bogus_banks/item_list.html', {
    #     'items': items,
    #     'new_items': [],
    #     'removed_items': []
    # })
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    items = ScrapedItem.objects.all().order_by('-updated_at')
    paginator = Paginator(items, per_page)
    page_obj = paginator.get_page(page_number)
    per_page_choices = [10, 20, 50, 100]
    return render(request, 'bogus_banks/item_list.html', {
        'page_obj': page_obj,
        'items': page_obj.object_list,
        'per_page': per_page,
        'per_page_choices': per_page_choices,
        'new_items': [],
        'removed_items': []
    })

@login_required
def filter_items(request):
    q = request.GET.get('q', '')
    items = ScrapedItem.objects.filter(name__icontains=q).order_by('-updated_at')
    return render(request, 'bogus_banks/partials/item_list.html', {'items': items})

@login_required
def refresh_items(request):
    data = fetch_items()
    new_items, removed_items = detect_changes(data)

    # Insert new items
    for item in new_items:
        ScrapedItem.objects.create(**item)

    if new_items or removed_items:
        send_change_notification(new_items, removed_items)
    # Re-fetch current items
    items = ScrapedItem.objects.all().order_by('-updated_at')

    # Pagination
    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    paginator = Paginator(items, per_page)
    page_obj = paginator.get_page(page_number)
    per_page_choices = [10, 20, 50, 100]

    # If HTMX request, return all tables partial
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'bogus_banks/partials/tables_container.html', {
            'page_obj': page_obj,
            'items': page_obj.object_list,
            'per_page': per_page,
            'per_page_choices': per_page_choices,
            'new_items': new_items,
            'removed_items': removed_items,
        })

    # Otherwise, render the full page (fallback)
    return render(request, 'bogus_banks/item_list.html', {
        'page_obj': page_obj,
        'items': page_obj.object_list,
        'per_page': per_page,
        'per_page_choices': per_page_choices,
        'new_items': new_items,
        'removed_items': removed_items
    })
