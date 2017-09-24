from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from urlshortening.models import Url, get_short_url


@require_POST
def get_short_link(request):
    full_url = request.POST.get('full_url', '')
    if not full_url:
        return JsonResponse({"error": "full_url is empty", "data": ""}, status=400)
    url = get_short_url(full_url)
    return JsonResponse({"error": "", "data": {
        "short_id": url.short_id,
        "short_url_path": settings.SHORT_URL_PATH
    }})


@require_GET
def get_full_link(request, short_id):
    try:
        url = Url.objects.get(pk=short_id)
        if url.is_expired:
            return JsonResponse({"error": "Link is expired", "data": ""}, status=404)
        return JsonResponse({"error": "", "data": {"full_url": url.url}})
    except Url.DoesNotExist:
        return JsonResponse({"error": "Url doesn\'t exist", "data": ""}, status=404)
