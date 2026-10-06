# leads/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import LeadForm
from .models import Lead, LeadActivity


@login_required
def dashboard(request):
    context = {
        "total": Lead.objects.count(),
        "new": Lead.objects.filter(status=Lead.Status.NEW).count(),
        "contacted": Lead.objects.filter(status=Lead.Status.CONTACTED).count(),
        "qualified": Lead.objects.filter(status=Lead.Status.QUALIFIED).count(),
        "won": Lead.objects.filter(status=Lead.Status.WON).count(),
        "lost": Lead.objects.filter(status=Lead.Status.LOST).count(),
        "recent_leads": Lead.objects.select_related("assigned_to")[:5],
    }

    return render(
        request,
        "leads/dashboard.html",
        context,
    )


@login_required
def lead_list(request):
    leads = Lead.objects.select_related("assigned_to")

    search = request.GET.get(
        "search",
        "",
    ).strip()

    status_filter = request.GET.get(
        "status",
        "",
    )

    source_filter = request.GET.get(
        "source",
        "",
    )

    ordering = request.GET.get(
        "ordering",
        "-created_at",
    )

    allowed_ordering = {
        "name",
        "-name",
        "created_at",
        "-created_at",
        "status",
        "-status",
    }

    if ordering not in allowed_ordering:
        ordering = "-created_at"

    if search:
        leads = leads.filter(
            Q(name__icontains=search)
            | Q(phone__icontains=search)
            | Q(email__icontains=search)
        )

    if status_filter:
        leads = leads.filter(status=status_filter)

    if source_filter:
        leads = leads.filter(source=source_filter)

    leads = leads.order_by(ordering)

    paginator = __import__(
        "django.core.paginator",
        fromlist=["Paginator"],
    ).Paginator(
        leads,
        10,
    )

    page_number = request.GET.get(
        "page",
        1,
    )

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "leads/lead_list.html",
        {
            "page_obj": page_obj,
            "search": search,
            "status_filter": status_filter,
            "source_filter": source_filter,
            "ordering": ordering,
            "statuses": Lead.Status.choices,
            "sources": Lead.Source.choices,
        },
    )


@login_required
def lead_create(request):

    if request.method == "POST":
        form = LeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)

            lead.assigned_to = request.user
            lead.save()

            LeadActivity.objects.create(
                lead=lead,
                user=request.user,
                action="created",
                description="Lead created",
            )

            messages.success(
                request,
                "Lead created successfully.",
            )

            return redirect(
                "lead-detail",
                pk=lead.pk,
            )

    else:
        form = LeadForm()

    return render(
        request,
        "leads/lead_form.html",
        {
            "form": form,
            "title": "Create Lead",
        },
    )


@login_required
def lead_detail(request, pk):

    lead = get_object_or_404(
        Lead.objects.select_related("assigned_to"),
        pk=pk,
    )

    activities = lead.activities.select_related("user")  # type: ignore

    return render(
        request,
        "leads/lead_detail.html",
        {
            "lead": lead,
            "activities": activities,
        },
    )


@login_required
def lead_edit(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    old_status = lead.status

    if request.method == "POST":
        form = LeadForm(
            request.POST,
            instance=lead,
        )

        if form.is_valid():
            lead = form.save()

            if old_status != lead.status:
                LeadActivity.objects.create(
                    lead=lead,
                    user=request.user,
                    action="status_changed",
                    description=(f"Status changed from {old_status} to {lead.status}"),
                )
            else:
                LeadActivity.objects.create(
                    lead=lead,
                    user=request.user,
                    action="updated",
                    description="Lead updated",
                )

            messages.success(
                request,
                "Lead updated successfully.",
            )

            return redirect(
                "lead-detail",
                pk=lead.pk,
            )

    else:
        form = LeadForm(instance=lead)

    return render(
        request,
        "leads/lead_form.html",
        {
            "form": form,
            "lead": lead,
            "title": "Edit Lead",
        },
    )


@login_required
def lead_delete(request, pk):

    lead = get_object_or_404(
        Lead,
        pk=pk,
    )

    if request.method == "POST":
        lead.delete()

        messages.success(
            request,
            "Lead deleted successfully.",
        )

        return redirect("lead-list")

    return render(
        request,
        "leads/lead_delete.html",
        {
            "lead": lead,
        },
    )
