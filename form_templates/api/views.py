from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from tinydb import Query, TinyDB

from api.utils import format_dates, get_field_type


@require_POST
@csrf_exempt
def get_form(request: HttpRequest) -> JsonResponse:
    """Функция для получения шаблона формы."""
    db = TinyDB(settings.DATA_STORAGE_LOCATION)
    query = Query()
    query_parameters = request.GET
    if query_parameters.get('name'):
        return JsonResponse(
            {'name': "you can't search by name field"},
            status=HTTPStatus.BAD_REQUEST,
        )
    formatted_parameters = format_dates(query_parameters)
    found_records = db.search(query.fragment(formatted_parameters))
    if found_records:
        response = []
        for record in found_records:
            response.append({'name': record['name']})
        return JsonResponse(response, safe=False)
    fields_types = {}
    for field_name, value in formatted_parameters.items():
        fields_types[field_name] = get_field_type(
            value,
        )  # type:ignore[arg-type]
    return JsonResponse(fields_types)
