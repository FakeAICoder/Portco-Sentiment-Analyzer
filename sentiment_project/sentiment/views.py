from django.http import JsonResponse
from django.views.decorators.http import require_GET
from . import aggregator
import os


@require_GET
def aggregate(request):
    feed_url = request.GET.get("feed_url")
    openai_key = os.getenv("OPENAI_API_KEY")
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    if not feed_url:
        return JsonResponse({"error": "feed_url parameter required"}, status=400)

    try:
        data = aggregator.aggregate_feed(feed_url, openai_key, bearer)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)

    return JsonResponse({"results": data})
