"""Load demo data: >=10 rows per table (lab requirement)."""
import logging
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from insurance import models

log = logging.getLogger("insurance")
N = 10


def _phone_unique(seq: int) -> str:
    n = (1_000_000 + seq * 7919) % 10_000_000
    s = f"{n:07d}"
    return f"+375 (29) {s[:3]}-{s[3:5]}-{s[5:7]}"


def _adult_birth(years: int = 30) -> date:
    return date.today().replace(year=date.today().year - years)


def clear_demo_data() -> None:
    models.Review.objects.all().delete()
    models.PromoCode.objects.all().delete()
    models.Vacancy.objects.all().delete()
    models.ContactPerson.objects.all().delete()
    models.FAQEntry.objects.all().delete()
    models.NewsArticle.objects.all().delete()
    models.CompanyRequisite.objects.all().delete()
    models.CompanyProfile.objects.all().delete()
    models.Contract.objects.all().delete()
    models.InsuredObject.objects.all().delete()
    models.ClientIdentity.objects.all().delete()
    models.Client.objects.all().delete()
    models.Agent.objects.all().delete()
    models.Branch.objects.all().delete()
    models.InsuranceType.objects.all().delete()


def seed() -> None:
    cities = ["Минск", "Гродно", "Брест", "Гомель", "Витебск", "Могилёв", "Бобруйск", "Барановичи", "Пинск", "Орша"]
    branches = [
        models.Branch(
            name=f"Филиал {cities[i]}",
            address=f"ул. Центральная, {10 + i}",
            city=cities[i],
            phone=_phone_unique(i + 1),
        )
        for i in range(N)
    ]
    models.Branch.objects.bulk_create(branches)
    branches = list(models.Branch.objects.order_by("id"))

    types_data = [
        ("Авто от угона", Decimal("0.028000"), Decimal("12.00")),
        ("Имущество граждан", Decimal("0.018000"), Decimal("10.00")),
        ("ДМС", Decimal("0.042000"), Decimal("15.00")),
        ("Жизнь", Decimal("0.012000"), Decimal("8.00")),
        ("КАСКО", Decimal("0.055000"), Decimal("14.00")),
        ("Ответственность ТС", Decimal("0.022000"), Decimal("11.00")),
        ("Несчастный случай", Decimal("0.025000"), Decimal("9.00")),
        ("Путешествия", Decimal("0.015000"), Decimal("7.00")),
        ("Грузоперевозки", Decimal("0.020000"), Decimal("10.50")),
        ("Сельхоз риски", Decimal("0.019000"), Decimal("8.50")),
    ]
    insurance_types = [
        models.InsuranceType(name=name, tariff_rate=tr, agent_commission_percent=cp)
        for name, tr, cp in types_data
    ]
    models.InsuranceType.objects.bulk_create(insurance_types)
    insurance_types = list(models.InsuranceType.objects.order_by("id"))

    agents = []
    for i in range(N):
        br = branches[i % len(branches)]
        agents.append(
            models.Agent(
                last_name=f"Агентов{i + 1}",
                first_name=f"Имя{i + 1}",
                patronymic="Петрович",
                phone=_phone_unique(20 + i),
                birth_date=_adult_birth(25 + (i % 10)),
                branch=br,
            )
        )
    models.Agent.objects.bulk_create(agents)
    agents_by_branch = {}
    for a in models.Agent.objects.select_related("branch"):
        agents_by_branch.setdefault(a.branch_id, []).append(a)

    clients = [
        models.Client(
            full_name=f"Клиент Демо {i + 1}",
            phone=_phone_unique(100 + i),
            email=f"client{i + 1}@example.invalid",
            birth_date=_adult_birth(22 + (i % 8)),
            address=f"г. {cities[i % len(cities)]}, ул. Примерная, д. {10 + i}",
        )
        for i in range(N)
    ]
    models.Client.objects.bulk_create(clients)
    clients = list(models.Client.objects.order_by("id"))

    for i, c in enumerate(clients):
        models.ClientIdentity.objects.create(
            client=c,
            document_id=f"MP{7000000 + i}",
        )

    kinds = [c[0] for c in models.InsuredObject.ObjectKind.choices]
    objects_list = [
        models.InsuredObject(
            object_type=kinds[i % len(kinds)],
            description=f"Объект страхования №{i + 1}",
            value=Decimal(5000 + i * 2500),
        )
        for i in range(N)
    ]
    models.InsuredObject.objects.bulk_create(objects_list)
    objects_list = list(models.InsuredObject.objects.order_by("id"))

    base_signed = date(2024, 1, 10)
    for i in range(N):
        br = branches[i % len(branches)]
        branch_agents = agents_by_branch.get(br.id, [])
        ag = branch_agents[0] if branch_agents else list(agents_by_branch.values())[0][0]
        signed = base_signed + timedelta(days=20 * i)
        contract = models.Contract(
            signed_date=signed,
            end_date=signed + timedelta(days=365),
            insurance_amount=Decimal(8000 + i * 4500),
            branch=br,
            agent=ag,
            client=clients[i],
            insurance_type=insurance_types[i % len(insurance_types)],
        )
        contract.save()
        contract.insured_objects.add(objects_list[i % len(objects_list)])

    profile = models.CompanyProfile.objects.create(
        title="О компании (демо)",
        about_text="Страховая компания демонстрационного стенда.",
    )
    for i in range(N):
        models.CompanyRequisite.objects.create(
            profile=profile,
            label=f"Реквизит {i + 1}",
            value=f"Значение реквизита №{i + 1}",
            sort_order=i,
        )

    for n in range(N):
        title = f"Новость компании №{n + 1}"
        models.NewsArticle.objects.create(
            title=title,
            slug=slugify(f"news-{n + 1}")[:200],
            summary=f"Краткое описание новости №{n + 1}.",
            image_url=f"insurance/images/news_{(n % 3) + 1}.svg",
            body="Полный текст новости (демо).",
            is_published=True,
            published_at=timezone.now() - timedelta(days=n),
        )

    for i in range(N):
        models.FAQEntry.objects.create(
            question=f"Термин / вопрос №{i + 1}?",
            answer=f"Определение и пояснение для пункта словаря №{i + 1}.",
        )

    for i in range(N):
        models.ContactPerson.objects.create(
            full_name=f"Сотрудник контактов {i + 1}",
            role_title="Специалист" if i % 2 else "Руководитель",
            photo_url="insurance/images/contact.svg",
            phone=_phone_unique(300 + i),
            email=f"contact{i + 1}@example.invalid",
            bio="Биография для страницы контактов.",
            birth_date=_adult_birth(35 + (i % 5)),
            branch=branches[i % len(branches)],
        )

    for i in range(N):
        models.Vacancy.objects.create(
            title=f"Вакансия: страховой агент ({i + 1})",
            description="Консультирование, оформление договоров.",
            is_active=i < 8,
        )

    for i in range(N):
        models.Review.objects.create(
            guest_name=f"Гость {i + 1}",
            rating=(i % 5) + 1,
            text=f"Отзыв демо №{i + 1}: понравился сервис, рекомендую коллегам.",
        )

    today = date.today()
    for i in range(N):
        vf = today - timedelta(days=30 + i * 10)
        vt = today + timedelta(days=60 + i * 5)
        models.PromoCode.objects.create(
            code=f"PROMO{i + 1:02d}",
            discount_percent=Decimal(5 + (i % 10)),
            valid_from=vf,
            valid_until=vt,
            is_active=i < 7,
        )

    for group_name in ("client", "employee"):
        Group.objects.get_or_create(name=group_name)


class Command(BaseCommand):
    help = f"Create demo records ({N}+ per table). --force to replace."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        if options["clear"]:
            with transaction.atomic():
                clear_demo_data()
            self.stdout.write(self.style.SUCCESS("Cleared insurance app data."))
            return

        if models.Contract.objects.exists() and not options["force"]:
            self.stdout.write(
                self.style.WARNING("Data exists. Use --force to re-seed.")
            )
            return

        with transaction.atomic():
            if options["force"]:
                clear_demo_data()
            seed()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded: branches={models.Branch.objects.count()}, "
                f"contracts={models.Contract.objects.count()}, "
                f"news={models.NewsArticle.objects.count()}"
            )
        )
