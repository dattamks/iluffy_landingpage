from django.db import models


class Plan(models.Model):
    """Pricing plan shown on the landing page."""

    name = models.CharField(max_length=50)  # e.g. "Free", "Pro"
    tagline = models.CharField(max_length=200, blank=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    annual_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="Total annual price (shown as per-month equivalent on the card)",
    )
    monthly_original_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Strike-through original monthly price (leave blank if none)",
    )
    annual_original_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Strike-through original annual price (leave blank if none)",
    )
    is_popular = models.BooleanField(default=False)
    cta_label = models.CharField(max_length=60, default="Get Started")
    cta_url_type = models.CharField(
        max_length=20, default="register",
        choices=[("register", "Register"), ("billing", "Billing"), ("login", "Login")],
        help_text="Which app URL this plan's button links to",
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    @property
    def annual_per_month(self):
        if self.annual_price:
            return round(self.annual_price / 12, 2)
        return 0

    @property
    def annual_original_per_month(self):
        if self.annual_original_price:
            return round(self.annual_original_price / 12, 2)
        return None


class PlanFeature(models.Model):
    """Individual feature bullet for a Plan."""

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="features")
    text = models.CharField(max_length=200)
    tooltip = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.plan.name} – {self.text}"


class Testimonial(models.Model):
    """User testimonial displayed on the landing page."""

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150, blank=True)  # e.g. "Software Engineer"
    company = models.CharField(max_length=100, blank=True)
    quote = models.TextField()
    avatar_url = models.URLField(blank=True, help_text="URL to avatar image (optional)")
    rating = models.PositiveSmallIntegerField(default=5, help_text="1-5 star rating")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} – {self.role}"


class ContactSubmission(models.Model):
    """Stores contact-form submissions."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.email} ({self.created_at:%Y-%m-%d})"


class ContactInfo(models.Model):
    """Site-wide contact / social info (singleton-style)."""

    support_email = models.EmailField(default="support@iluffy.com")
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    discord_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"Contact Info ({self.support_email})"

    def save(self, *args, **kwargs):
        # Singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteConfig(models.Model):
    """Configurable app URLs and button labels (singleton-style)."""

    app_base_url = models.URLField(
        default="https://app.iluffy.in",
        help_text="Base URL of the main application (no trailing slash)",
    )
    register_path = models.CharField(max_length=100, default="/register")
    login_path = models.CharField(max_length=100, default="/login")
    billing_path = models.CharField(max_length=100, default="/billing")
    sample_report_url = models.CharField(
        max_length=300, default="#",
        help_text="URL for 'View Sample Report' button (use # as placeholder)",
    )

    # Customisable button labels
    nav_login_label = models.CharField(max_length=60, default="Log in")
    nav_cta_label = models.CharField(max_length=60, default="Analyze Now")
    hero_cta_label = models.CharField(max_length=60, default="Start Analysis")
    hero_secondary_label = models.CharField(max_length=60, default="Sample Report")
    cta_primary_label = models.CharField(max_length=60, default="Get Started Free")
    cta_secondary_label = models.CharField(max_length=60, default="View Pricing")

    class Meta:
        verbose_name = "Site Config"
        verbose_name_plural = "Site Config"

    def __str__(self):
        return f"Site Config ({self.app_base_url})"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def register_url(self):
        return f"{self.app_base_url.rstrip('/')}{self.register_path}"

    @property
    def login_url(self):
        return f"{self.app_base_url.rstrip('/')}{self.login_path}"

    @property
    def billing_url(self):
        return f"{self.app_base_url.rstrip('/')}{self.billing_path}"

