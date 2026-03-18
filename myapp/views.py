from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def marine_rescue(request):
    return render(request, "marine-rescue.html")

def weather_alert(request):
    alerts = WeatherAlert.objects.filter(status="active")
    return render(request, "weather-alerts.html", {"alerts": alerts})



def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')

        # ================= ADMIN =================
        if user.userType == "admin":
            login(request, user)
            request.session['aid'] = user.id
            return redirect('/admin_home/')

        # ================= FISHERMAN =================
        if user.userType == "fisherman":
            if not Fisherman.objects.filter(loginid=user).exists():
                messages.error(request, "Fisherman profile not found")
                return redirect('/login/')
            login(request, user)
            request.session['fid'] = user.id
            return redirect('/fisherman_home/')

        # ================= RESCUE TEAM =================
        if user.userType == "rescue":

            rescue = RescueTeam.objects.filter(loginid=user).first()

            if not rescue:
                messages.error(request, "Rescue profile not found")
                return redirect('/login/')

            # 🚫 BLOCK LOGIN UNTIL ADMIN APPROVES
            if rescue.status != "active":
                messages.error(
                    request,
                    "Your account is not approved yet. Please wait for admin approval."
                )
                return redirect('/login/')

            login(request, user)
            request.session['rid'] = user.id
            return redirect('/rescue_home/')

        messages.error(request, "Invalid account type")
        return redirect('/login/')

    return render(request, "login.html")


def fisherman_register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        boat_number = request.POST.get("boat_number")
        address = request.POST.get("address")

        if not all([username, password, name, phone, boat_number]):
            messages.error(request, "All required fields must be filled")
            return redirect('/fisherman_register/')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/fisherman_register/')

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="fisherman",
            viewPass=password
        )

        Fisherman.objects.create(
            loginid=login_obj,
            name=name,
            phone=phone,
            boat_number=boat_number,
            address=address
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('/login/')

    return render(request, "register.html")


def rescue_register(request):

    ports = Port.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        port_id = request.POST.get("port")
        profile_pic = request.FILES.get("profile_pic")

        if not all([username, password, name, phone, email, port_id]):
            messages.error(request, "All required fields must be filled")
            return redirect('/rescue_register/')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/rescue_register/')

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="rescue",
            viewPass=password
        )

        RescueTeam.objects.create(
            loginid=login_obj,
            name=name,
            phone=phone,
            email=email,
            port_id=port_id,
            profile_pic=profile_pic,
            status="inactive"   # admin approval needed
        )

        messages.success(
            request,
            "Rescue team registered successfully. Await admin approval."
        )
        return redirect('/login/')

    return render(request, "rescue_register.html", {
        "ports": ports
    })



def admin_home(request):
    if 'aid' not in request.session:
        return redirect('/login/')
    return render(request, "ADMIN/index.html")

def admin_pending_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    rescues = RescueTeam.objects.filter(status='inactive')

    return render(request, "ADMIN/pending_rescue.html", {
        "rescues": rescues
    })


def admin_view_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    rescue_list = RescueTeam.objects.select_related(
        'loginid', 'port'
    ).order_by('-id')

    return render(request, "ADMIN/view_rescue.html", {
        "rescue_list": rescue_list
    })

def admin_approve_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        rid = request.POST.get("rid")

        rescue = RescueTeam.objects.filter(id=rid).first()
        if rescue:
            rescue.status = "active"
            rescue.save()
            messages.success(
                request,
                f"{rescue.name} approved successfully."
            )

    return redirect('/admin_view_rescue/')


def admin_block_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        rid = request.POST.get("rid")

        rescue = RescueTeam.objects.filter(id=rid).first()
        if rescue:
            rescue.status = "inactive"
            rescue.save()
            messages.warning(
                request,
                f"{rescue.name} blocked successfully."
            )

    return redirect('/admin_view_rescue/')



def admin_block_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        rid = request.POST.get("rid")

        rescue = RescueTeam.objects.filter(id=rid).first()
        if rescue:
            rescue.status = "inactive"
            rescue.save()
            messages.warning(
                request,
                f"{rescue.name} blocked successfully."
            )

    return redirect('/admin_view_rescue/')


def admin_reject_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        rid = request.POST.get("rid")

        rescue = RescueTeam.objects.filter(id=rid).first()
        if rescue:
            rescue.status = "inactive"
            rescue.save()
            messages.error(
                request,
                f"{rescue.name} rejected."
            )

    return redirect('/admin_view_rescue/')





def admin_delete_rescue(request, rid):
    if 'aid' not in request.session:
        return redirect('/login/')

    rescue = RescueTeam.objects.filter(id=rid).first()
    if rescue:
        rescue.delete()
        messages.error(
            request,
            "Rescue team deleted permanently."
        )

    return redirect('/admin_view_rescue/')


def admin_view_fishermen(request):
    # Admin session check
    if 'aid' not in request.session:
        return redirect('/login/')

    # Fetch fishermen details
    users = Fisherman.objects.select_related('loginid').all()

    return render(
        request,
        "ADMIN/view_users.html",
        {
            "users": users
        }
    )
# Admin - Add Weather Alert
def admin_add_weather_alert(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    ports = Port.objects.all()
    admins = Login.objects.filter(id=request.session['aid']).first()

    if request.method == "POST":
        port_id = request.POST.get("port")
        title = request.POST.get("title")
        description = request.POST.get("description")
        alert_level = request.POST.get("alert_level")
        status = request.POST.get("status", "active")

        # Validation
        if not port_id or not title or not description or not alert_level:
            messages.error(request, "All fields except status are required.")
            return redirect('/admin_add_weather_alert/')

        port = Port.objects.filter(id=port_id).first()
        if not port:
            messages.error(request, "Selected port does not exist.")
            return redirect('/admin_add_weather_alert/')

        WeatherAlert.objects.create(
            port=port,
            title=title,
            description=description,
            alert_level=alert_level,
            status=status,
            created_by=admins,
        )

        messages.success(request, f"Weather alert '{title}' added successfully.")
        return redirect('/admin_add_weather_alert/')

    return render(request, "ADMIN/admin_add_weather.html", {"ports": ports})

# Admin - Edit Weather Alert
def admin_edit_weather_alert(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    alert_id = request.GET.get('id')
    alert = WeatherAlert.objects.filter(id=alert_id).first()
    if not alert:
        messages.error(request, "Weather alert not found.")
        return redirect('/admin_view_weather/')

    ports = Port.objects.all()

    if request.method == "POST":
        port_id = request.POST.get("port")
        title = request.POST.get("title")
        description = request.POST.get("description")
        alert_level = request.POST.get("alert_level")
        status = request.POST.get("status", "active")

        if not port_id or not title or not description or not alert_level:
            messages.error(request, "All fields except status are required.")
            return redirect(f'/admin_edit_weather_alert/?id={alert.id}')

        port = Port.objects.filter(id=port_id).first()
        if not port:
            messages.error(request, "Selected port does not exist.")
            return redirect(f'/admin_edit_weather_alert/?id={alert.id}')

        alert.port = port
        alert.title = title
        alert.description = description
        alert.alert_level = alert_level
        alert.status = status
        alert.save()

        messages.success(request, f"Weather alert '{title}' updated successfully.")
        return redirect('/admin_view_weather/')

    return render(request, "ADMIN/admin_edit_weather.html", {
        "alert": alert,
        "ports": ports
    })

# Admin - Delete Weather Alert
def admin_delete_weather_alert(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    alert_id = request.GET.get('id')
    alert = WeatherAlert.objects.filter(id=alert_id).first()
    if not alert:
        messages.error(request, "Weather alert not found.")
        return redirect('/admin_view_weather/')

    alert.delete()
    messages.success(request, "Weather alert deleted successfully.")
    return redirect('/admin_view_weather/')

def admin_view_weather(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    weather_alerts = WeatherAlert.objects.select_related('port').order_by('-created_at')

    return render(request, 'ADMIN/admin_view_weather.html', {
        'weather_alerts': weather_alerts
    })

def admin_view_port(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    ports = Port.objects.all().order_by('name')
    return render(request, "ADMIN/view_port.html", {
        "ports": ports
    })


def admin_add_port(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Port name is required")
            return redirect('/admin_add_port/')

        Port.objects.create(
            name=name,
            description=description
        )

        messages.success(request, f"Port '{name}' added successfully")
        return redirect('/admin_view_ports/')   # go back to list

    # ✅ VERY IMPORTANT (GET request)
    return render(request, "ADMIN/admin_add_port.html")



# Delete
def admin_delete_port(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    port_id = request.GET.get('id')
    port = Port.objects.filter(id=port_id).first()

    if not port:
        messages.error(request, "Port not found")
    else:
        port.delete()
        messages.success(request, "Port deleted successfully")

    return redirect('/admin_view_ports/')

# Edit
def admin_edit_port(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    port_id = request.GET.get('id')
    port = Port.objects.filter(id=port_id).first()

    if not port:
        messages.error(request, "Port not found")
        return redirect('/admin_view_ports/')

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            messages.error(request, "Name is required")
            return redirect(f'/admin_edit_port/?id={port.id}')

        if Port.objects.filter(name__iexact=name).exclude(id=port.id).exists():
            messages.error(request, "Port name already exists")
            return redirect(f'/admin_edit_port/?id={port.id}')

        port.name = name
        port.description = description
        port.save()

        messages.success(request, "Port updated successfully")
        return redirect('/admin_view_ports/')

    return render(request, "ADMIN/edit_port.html", {
        "port": port
    })



def admin_view_sos_rescue(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    sos_list = SOS.objects.select_related(
        'fisherman',
        'fisherman__loginid'
    ).order_by('-created_at')

    rescue_actions = RescueAction.objects.select_related(
        'sos',
        'sos__fisherman',
        'rescue_team',
        'rescue_team__port'
    ).order_by('-action_date')

    return render(request, 'ADMIN/admin_view_sos_rescue.html', {
        'sos_list': sos_list,
        'rescue_actions': rescue_actions
    })


def admin_view_sos(request):
    if 'aid' not in request.session:
        return redirect('/login/')

    sos_list = SOS.objects.select_related(
        'fisherman'
    ).order_by('-created_at')

    return render(request, "ADMIN/view_sos.html", {
        "sos_list": sos_list
    })


def fisherman_home(request):
    if 'fid' not in request.session:
        return redirect('/login/')
    return render(request, "USER/index.html")

def fisherman_view_weather(request):
    if 'fid' not in request.session:
        return redirect('/login/')

    alerts = WeatherAlert.objects.filter(status="active").order_by('-created_at')
    return render(request, "USER/view_weather.html", {
        "alerts": alerts
    })
def send_sos(request):
    if 'fid' not in request.session:
        return redirect('/login/')

    fisherman = Fisherman.objects.filter(
        loginid_id=request.session['fid']
    ).first()

    if not fisherman:
        return redirect('/login/')

    if request.method == "POST":
        emergency_type = request.POST.get("emergency_type")
        location = request.POST.get("location")
        message = request.POST.get("message")

        SOS.objects.create(
            fisherman=fisherman,
            emergency_type=emergency_type,
            location_details=location,
            message=message
        )

        messages.success(request, "SOS sent successfully")
        return redirect('/fisherman_home/')

    return render(request, "USER/send_sos.html")

def fisherman_sos_history(request):
    if 'fid' not in request.session:
        return redirect('/login/')

    fisherman = Fisherman.objects.filter(loginid_id=request.session['fid']).first()
    if not fisherman:
        return redirect('/login/')

    sos_list = SOS.objects.filter(fisherman=fisherman).order_by('-created_at')
    return render(request, "USER/sos_history.html", {
        "sos_list": sos_list
    })



def rescue_home(request):
    if 'rid' not in request.session:
        return redirect('/login/')
    return render(request, "RESCUE/index.html")

def rescue_view_sos(request):
    if 'rid' not in request.session:
        return redirect('/login/')

    sos_list = SOS.objects.filter(
        status__in=["pending", "dispatched"]
    ).order_by('-created_at')

    sos_id = request.GET.get("sos_id")
    selected_sos = None
    actions = None

    if sos_id:
        selected_sos = SOS.objects.filter(id=sos_id).first()
        if selected_sos:
            actions = RescueAction.objects.filter(
                sos=selected_sos
            ).order_by('-action_date')

    return render(request, "RESCUE/sos_dashboard.html", {
        "sos_list": sos_list,
        "selected_sos": selected_sos,
        "actions": actions
    })


def rescue_take_action(request):
    if 'rid' not in request.session:
        return redirect('/login/')

    sos_id = request.POST.get("sos_id")
    sos = SOS.objects.filter(id=sos_id).first()

    rescue_team = RescueTeam.objects.filter(
        loginid_id=request.session['rid']
    ).first()

    if request.method == "POST":
        RescueAction.objects.create(
            sos=sos,
            rescue_team=rescue_team,
            action_note=request.POST.get("action_note"),
            status_updated_to=request.POST.get("status")
        )

        sos.status = request.POST.get("status")
        sos.save()

    return redirect(f"/rescue_view_sos/?sos_id={sos.id}")

def rescue_history(request):
    if 'rid' not in request.session:
        return redirect('/login/')

    rescue_team = RescueTeam.objects.filter(
        loginid_id=request.session['rid']
    ).first()

    if not rescue_team:
        return redirect('/login/')

    # Get SOS IDs handled by this rescue team
    sos_ids = RescueAction.objects.filter(
        rescue_team=rescue_team
    ).values_list('sos_id', flat=True).distinct()

    sos_list = SOS.objects.select_related(
        'fisherman'
    ).filter(
        id__in=sos_ids
    ).order_by('-created_at')

    return render(request, "RESCUE/rescue_history.html", {
        "sos_list": sos_list
    })


def rescue_history_detail(request):
    if 'rid' not in request.session:
        return redirect('/login/')

    sos_id = request.GET.get("sos_id")

    sos = SOS.objects.select_related(
        'fisherman'
    ).filter(id=sos_id).first()

    if not sos:
        messages.error(request, "SOS not found")
        return redirect('/rescue_history/')

    actions = RescueAction.objects.select_related(
        'rescue_team'
    ).filter(
        sos=sos
    ).order_by('-action_date')

    return render(request, "RESCUE/rescue_history_detail.html", {
        "sos": sos,
        "actions": actions
    })
