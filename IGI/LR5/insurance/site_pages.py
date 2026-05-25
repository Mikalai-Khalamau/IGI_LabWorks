"""Public site pages (lab stage 5)."""
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.list import ListView

from . import models
from .forms import ReviewForm
from .mixins import ClientGroupMixin

User = get_user_model()


class SiteHomeView(TemplateView):
    template_name = "insurance/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["latest_news"] = (
            models.NewsArticle.objects.filter(is_published=True)
            .order_by("-published_at")
            .first()
        )
        return ctx


class AboutView(TemplateView):
    template_name = "insurance/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["company"] = (
            models.CompanyProfile.objects.prefetch_related("requisites")
            .order_by("id")
            .first()
        )
        return ctx


class NewsListView(ListView):
    model = models.NewsArticle
    template_name = "insurance/news_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return models.NewsArticle.objects.filter(is_published=True).order_by(
            "-published_at"
        )


class NewsDetailView(DetailView):
    model = models.NewsArticle
    template_name = "insurance/news_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return models.NewsArticle.objects.filter(is_published=True)


class FAQListView(ListView):
    model = models.FAQEntry
    template_name = "insurance/faq_list.html"
    context_object_name = "faq_entries"
    paginate_by = 20

    def get_queryset(self):
        return models.FAQEntry.objects.order_by("-created_at")


class ContactListView(ListView):
    model = models.ContactPerson
    template_name = "insurance/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 12

    def get_queryset(self):
        return models.ContactPerson.objects.select_related("branch").order_by("full_name")


class PrivacyView(TemplateView):
    template_name = "insurance/privacy.html"


class VacancyListView(ListView):
    model = models.Vacancy
    template_name = "insurance/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 15

    def get_queryset(self):
        return models.Vacancy.objects.filter(is_active=True).order_by("-created_at")


class ReviewListView(ListView):
    model = models.Review
    template_name = "insurance/review_list.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        return models.Review.objects.select_related("user").order_by("-created_at")


class ReviewCreateView(LoginRequiredMixin, ClientGroupMixin, SuccessMessageMixin, CreateView):
    model = models.Review
    form_class = ReviewForm
    template_name = "insurance/review_form.html"
    success_url = reverse_lazy("insurance:review-list")
    success_message = "Review submitted."

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.guest_name = ""
        return super().form_valid(form)


class PromoListView(TemplateView):
    template_name = "insurance/promo_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        active_q = Q(is_active=True) & Q(valid_from__lte=today) & Q(valid_until__gte=today)
        ctx["active_promos"] = (
            models.PromoCode.objects.filter(active_q).order_by("-valid_until")
        )
        ctx["archived_promos"] = (
            models.PromoCode.objects.exclude(active_q).order_by("-valid_until")
        )
        return ctx


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "insurance/register.html"
    success_url = reverse_lazy("login")
    success_message = "Account created. You can sign in now."

    def form_valid(self, form):
        from django.contrib.auth.models import Group

        response = super().form_valid(form)
        group, _ = Group.objects.get_or_create(name="client")
        self.object.groups.add(group)
        return response
