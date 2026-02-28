from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Plan, Testimonial, ContactSubmission, ContactInfo, SiteConfig


def _common_context():
    site = SiteConfig.load()
    return {
        "contact_info": ContactInfo.load(),
        "site": site,
    }


def index(request):
    if request.method == "POST" and "contact_submit" in request.POST:
        return _handle_contact(request)

    ctx = _common_context()
    site = ctx["site"]
    plans = list(Plan.objects.all())

    # Resolve CTA URL for each plan
    url_map = {"register": site.register_url, "billing": site.billing_url, "login": site.login_url}
    for plan in plans:
        plan.cta_url = url_map.get(plan.cta_url_type, site.register_url)
    ctx["plans"] = plans
    ctx["max_annual_discount"] = max(
        (p.annual_discount_percent for p in plans), default=0
    )
    ctx["testimonials"] = Testimonial.objects.filter(is_active=True)
    return render(request, "main/index.html", ctx)


def privacy(request):
    return render(request, "main/privacy.html", _common_context())


def terms(request):
    return render(request, "main/terms.html", _common_context())


def data_policy(request):
    return render(request, "main/data_policy.html", _common_context())


def _handle_contact(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    if not all([name, email, subject, message]):
        messages.error(request, "Please fill in all fields.")
        return redirect("main:index")

    ContactSubmission.objects.create(
        name=name, email=email, subject=subject, message=message,
    )
    messages.success(request, "Message sent! We'll get back to you shortly.")
    return redirect("main:index")
