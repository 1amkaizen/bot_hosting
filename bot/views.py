import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .handlers import handle_message 
logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Data masuk: {data}")

            handle_message(data)

        except Exception as e:
            logger.error(f"Error di webhook: {e}")
            return JsonResponse({"ok": False, "error": str(e)}, status=200)

    return JsonResponse({"ok": True})

