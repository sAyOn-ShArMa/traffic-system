from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import Vehicle, Accident, Violation, TrafficSignal, Operator
import json


def dashboard_stats(request):
    total_vehicles = Vehicle.objects.count()
    active_accidents = Accident.objects.filter(status="Pending").count()
    total_accidents = Accident.objects.count()
    total_violations = Violation.objects.count()
    speeds = Vehicle.objects.values_list('speed', flat=True)
    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    overspeeding = Vehicle.objects.filter(speed__gt=80).count()
    severe_accidents = Accident.objects.filter(severity__in=['Severe', 'Fatal'], status='Pending').count()

    return JsonResponse({
        "total_vehicles": total_vehicles,
        "active_accidents": active_accidents,
        "total_accidents": total_accidents,
        "total_violations": total_violations,
        "avg_speed": round(avg_speed, 1),
        "overspeeding": overspeeding,
        "severe_accidents": severe_accidents,
    })


def vehicles(request):
    data = {}
    for v in Vehicle.objects.all():
        data[v.vehicle_id] = {
            "lat": v.lat,
            "lng": v.lng,
            "speed": v.speed,
            "heading": v.heading,
        }
    return JsonResponse(data)


def accidents(request):
    data = []
    for a in Accident.objects.all():
        data.append({
            "id": a.id,
            "vehicle": a.vehicle,
            "lat": a.lat,
            "lng": a.lng,
            "road_name": a.road_name,
            "severity": a.severity,
            "description": a.description,
            "injuries": a.injuries,
            "time": a.time.strftime("%H:%M:%S"),
            "date": a.time.strftime("%Y-%m-%d"),
            "status": a.status,
        })
    return JsonResponse(data, safe=False)


def violations(request):
    data = []
    for v in Violation.objects.all():
        data.append({
            "vehicle": v.vehicle,
            "lat": v.lat,
            "lng": v.lng,
            "speed": v.speed,
            "lane": v.lane,
            "violation_type": v.violation_type,
            "video": v.video_clip,
            "fine": v.fine_amount,
            "time": v.time.strftime("%H:%M:%S"),
        })
    return JsonResponse(data, safe=False)


def congestion(request):
    data = []
    for v in Vehicle.objects.filter(speed__lt=20):
        data.append([v.lat, v.lng, 1])
    return JsonResponse(data, safe=False)


def signals(request):
    data = []
    for s in TrafficSignal.objects.all():
        data.append({
            "id": s.id,
            "name": s.name,
            "lat": s.lat,
            "lng": s.lng,
            "state": s.state,
            "cycle_time": s.cycle_time,
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def dispatch(request):
    if request.method == "POST":
        body = json.loads(request.body)
        accident_id = body.get("accident_id")
        unit = body.get("unit")
        try:
            a = Accident.objects.get(id=accident_id)
            # Append new unit to existing dispatched units
            if a.status.startswith("Dispatched"):
                existing = a.status.replace("Dispatched (", "").rstrip(")")
                units = [u.strip() for u in existing.split(",")]
                if unit not in units:
                    units.append(unit)
                a.status = f"Dispatched ({', '.join(units)})"
            else:
                a.status = f"Dispatched ({unit})"
            a.save()
            return JsonResponse({"success": True, "status": a.status})
        except Accident.DoesNotExist:
            return JsonResponse({"success": False, "message": "Accident not found"})
    return JsonResponse({"success": False, "message": "POST required"})


@csrf_exempt
def resolve_accident(request):
    if request.method == "POST":
        body = json.loads(request.body)
        accident_id = body.get("accident_id")
        try:
            a = Accident.objects.get(id=accident_id)
            a.status = "Resolved"
            a.resolved_at = timezone.now()
            a.save()
            return JsonResponse({"success": True})
        except Accident.DoesNotExist:
            return JsonResponse({"success": False, "message": "Accident not found"})
    return JsonResponse({"success": False, "message": "POST required"})


@csrf_exempt
def update_vehicle(request):
    if request.method == "POST":
        body = json.loads(request.body)
        vid = body.get("vehicle_id")
        v, _ = Vehicle.objects.get_or_create(vehicle_id=vid)
        v.lat = body.get("lat", v.lat)
        v.lng = body.get("lng", v.lng)
        v.speed = body.get("speed", v.speed)
        v.heading = body.get("heading", v.heading)
        v.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "POST required"})


def operator_login(request):
    if request.session.get('operator_id'):
        return redirect('command_center')

    error = None
    reg_success = None
    if request.method == "POST":
        op_id = request.POST.get('operator_id', '').strip()
        password = request.POST.get('password', '').strip()
        try:
            operator = Operator.objects.get(operator_id=op_id, is_active=True)
            if check_password(password, operator.password):
                request.session['operator_id'] = operator.operator_id
                request.session['operator_name'] = operator.name
                request.session['operator_role'] = operator.role
                operator.last_login = timezone.now()
                operator.save()
                return redirect('command_center')
            else:
                error = "Invalid password. Please try again."
        except Operator.DoesNotExist:
            error = "Operator ID not found."

    if request.GET.get('registered'):
        reg_success = "Registration successful! You can now log in."

    return render(request, 'login.html', {
        'error': error,
        'reg_success': reg_success,
        'active_tab': 'login',
    })


@csrf_exempt
def operator_register(request):
    if request.session.get('operator_id'):
        return redirect('command_center')

    error = None
    if request.method == "POST":
        name = request.POST.get('reg_name', '').strip()
        op_id = request.POST.get('reg_operator_id', '').strip()
        password = request.POST.get('reg_password', '').strip()
        confirm = request.POST.get('reg_confirm_password', '').strip()
        role = request.POST.get('reg_role', 'Operator').strip()

        if not name or not op_id or not password:
            error = "All fields are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif Operator.objects.filter(operator_id=op_id).exists():
            error = "Operator ID already exists."
        else:
            Operator.objects.create(
                operator_id=op_id,
                name=name,
                password=make_password(password),
                role=role,
            )
            return redirect('/login/?registered=1')

    return render(request, 'login.html', {
        'reg_error': error,
        'active_tab': 'register',
    })


def operator_logout(request):
    request.session.flush()
    return redirect('login')


def command_center(request):
    if not request.session.get('operator_id'):
        return redirect('login')
    return render(request, 'map.html', {
        'operator_name': request.session.get('operator_name', ''),
        'operator_role': request.session.get('operator_role', ''),
        'operator_id': request.session.get('operator_id', ''),
    })
