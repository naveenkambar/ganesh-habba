import json
from decimal import Decimal, InvalidOperation

from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import SiteSettings, ScheduleItem, Collection, Expenditure


def get_settings():
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return obj


def parse_body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def check_password(data, settings_obj):
    return data.get("password", "") == settings_obj.password


# ---------- Frontend ----------

def index(request):
    return render(request, "index.html")


# ---------- API: read everything ----------

def api_data(request):
    s = get_settings()

    schedule = [
        {"id": str(x.id), "day": x.day, "time": x.time, "event": x.event}
        for x in ScheduleItem.objects.all()
    ]
    collections = [
        {"id": str(x.id), "name": x.name, "amount": float(x.amount),
         "receipt": x.receipt, "mode": x.mode, "date": x.date}
        for x in Collection.objects.all()
    ]
    expenditures = [
        {"id": str(x.id), "item": x.item, "amount": float(x.amount),
         "category": x.category, "date": x.date, "note": x.note}
        for x in Expenditure.objects.all()
    ]

    return JsonResponse({
        "settings": {
            "festivalName": s.festival_name,
            "streetName": s.street_name,
            "dateRange": s.date_range,
            "upiName": s.upi_name,
            "upiId": s.upi_id,
        },
        "schedule": schedule,
        "collections": collections,
        "expenditures": expenditures,
    })


# ---------- API: auth ----------

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    data = parse_body(request)
    s = get_settings()
    return JsonResponse({"ok": check_password(data, s)})


@csrf_exempt
@require_http_methods(["POST"])
def api_change_password(request):
    data = parse_body(request)
    s = get_settings()
    if data.get("current", "") != s.password:
        return JsonResponse({"error": "Current password is incorrect."}, status=403)
    new = (data.get("new") or "").strip()
    if len(new) < 4:
        return JsonResponse({"error": "New password must be at least 4 characters."}, status=400)
    s.password = new
    s.save()
    return JsonResponse({"ok": True})


# ---------- API: settings (title, UPI) ----------

@csrf_exempt
@require_http_methods(["POST"])
def api_update_settings(request):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)

    field_map = {
        "festivalName": "festival_name",
        "streetName": "street_name",
        "dateRange": "date_range",
        "upiName": "upi_name",
        "upiId": "upi_id",
    }
    changed = False
    for key, field in field_map.items():
        if key in data and data[key] is not None:
            setattr(s, field, data[key])
            changed = True
    if changed:
        s.save()
    return JsonResponse({"ok": True})


# ---------- API: schedule ----------

@csrf_exempt
@require_http_methods(["POST"])
def api_schedule_create(request):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    day = (data.get("day") or "").strip()
    time_ = (data.get("time") or "").strip()
    event = (data.get("event") or "").strip()
    if not day or not event:
        return JsonResponse({"error": "Day and event are required."}, status=400)
    obj = ScheduleItem.objects.create(day=day, time=time_, event=event)
    return JsonResponse({"id": str(obj.id), "day": day, "time": time_, "event": event})


@csrf_exempt
@require_http_methods(["DELETE"])
def api_schedule_delete(request, item_id):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    ScheduleItem.objects.filter(pk=item_id).delete()
    return JsonResponse({"ok": True})


# ---------- API: collections (chanda) ----------

@csrf_exempt
@require_http_methods(["POST"])
def api_collections_create(request):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    name = (data.get("name") or "").strip()
    amount = data.get("amount")
    receipt = (data.get("receipt") or "").strip()
    mode = (data.get("mode") or "Cash").strip()
    date = (data.get("date") or "").strip()
    if not name or not amount:
        return JsonResponse({"error": "Name and amount are required."}, status=400)
    if not receipt:
        return JsonResponse({"error": "Receipt No. is required and must be unique."}, status=400)
    try:
        decimal_amount = Decimal(str(amount))
    except InvalidOperation:
        return JsonResponse({"error": "Amount must be a number."}, status=400)
    try:
        obj = Collection.objects.create(name=name, amount=decimal_amount, receipt=receipt, mode=mode, date=date)
    except IntegrityError:
        return JsonResponse(
            {"error": f'Receipt No. "{receipt}" is already used. Each receipt number must be unique.'},
            status=409,
        )
    return JsonResponse({"id": str(obj.id), "name": name, "amount": amount, "receipt": receipt, "mode": mode, "date": date})


@csrf_exempt
@require_http_methods(["DELETE"])
def api_collections_delete(request, item_id):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    Collection.objects.filter(pk=item_id).delete()
    return JsonResponse({"ok": True})


# ---------- API: expenditures ----------

@csrf_exempt
@require_http_methods(["POST"])
def api_expenditures_create(request):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    item = (data.get("item") or "").strip()
    amount = data.get("amount")
    category = (data.get("category") or "Miscellaneous").strip()
    date = (data.get("date") or "").strip()
    note = (data.get("note") or "").strip()
    if not item or not amount:
        return JsonResponse({"error": "Item and amount are required."}, status=400)
    try:
        decimal_amount = Decimal(str(amount))
    except InvalidOperation:
        return JsonResponse({"error": "Amount must be a number."}, status=400)
    obj = Expenditure.objects.create(item=item, amount=decimal_amount, category=category, date=date, note=note)
    return JsonResponse({"id": str(obj.id), "item": item, "amount": amount, "category": category, "date": date, "note": note})


@csrf_exempt
@require_http_methods(["DELETE"])
def api_expenditures_delete(request, item_id):
    data = parse_body(request)
    s = get_settings()
    if not check_password(data, s):
        return JsonResponse({"error": "Not authorized."}, status=403)
    Expenditure.objects.filter(pk=item_id).delete()
    return JsonResponse({"ok": True})
