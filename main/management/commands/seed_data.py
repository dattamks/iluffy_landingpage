from django.core.management.base import BaseCommand
from main.models import Plan, Testimonial, ContactInfo, SiteConfig


class Command(BaseCommand):
    help = "Seed default plans, testimonials, and contact info"

    def handle(self, *args, **options):
        self._seed_plans()
        self._seed_testimonials()
        self._seed_contact_info()
        self._seed_site_config()
        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))

    def _seed_plans(self):
        if Plan.objects.exists():
            self.stdout.write("Plans already exist — skipping.")
            return

        all_features = [
            "ATS score breakdown",
            "Keyword analysis",
            "Section feedback",
            "AI sentence rewrites",
            "PDF report download",
            "Compare analyses",
            "Priority AI processing",
            "Share reports via link",
            "Smart Job Alerts",
            "AI Resume Generator",
        ]

        free_included = {
            "ATS score breakdown",
            "Keyword analysis",
            "Section feedback",
            "AI sentence rewrites",
            "PDF report download",
            "Compare analyses",
        }

        # ── Free Plan ──────────────────────────────────────────────
        Plan.objects.create(
            name="Free",
            tagline="Get started with AI resume analysis — no credit card needed.",
            credits_per_month=2,
            mrp_monthly=0,
            price_monthly=0,
            mrp_annual=0,
            price_annual=0,
            features=[
                {"name": f, "included": f in free_included}
                for f in all_features
            ],
            is_popular=False,
            cta_label="Get Started Free",
            cta_url_type="register",
            order=1,
        )

        # ── Pro Plan ───────────────────────────────────────────────
        Plan.objects.create(
            name="Pro",
            tagline="For active job seekers who need every edge.",
            credits_per_month=25,
            mrp_monthly=599,
            price_monthly=399,
            mrp_annual=7188,    # 599 × 12
            price_annual=3990,  # 399 × 10
            features=[
                {"name": f, "included": True}
                for f in all_features
            ],
            is_popular=True,
            cta_label="Be a Pro",
            cta_url_type="billing",
            order=2,
        )

        self.stdout.write(self.style.SUCCESS("  ✓ Plans seeded"))

    def _seed_testimonials(self):
        if Testimonial.objects.exists():
            self.stdout.write("Testimonials already exist — skipping.")
            return

        testimonials = [
            {
                "name": "Priya Sharma",
                "role": "Software Engineer",
                "company": "Google",
                "quote": "i-Luffy helped me identify critical keyword gaps I'd missed for months. After applying the AI suggestions, I started getting callbacks within a week!",
                "rating": 5,
            },
            {
                "name": "Rahul Menon",
                "role": "Data Analyst",
                "company": "Amazon",
                "quote": "The ATS simulation feature is a game-changer. I could see exactly how Workday was parsing my resume and fix formatting issues before applying.",
                "rating": 5,
            },
            {
                "name": "Ananya Patel",
                "role": "Product Manager",
                "company": "Microsoft",
                "quote": "The impact rewriting engine transformed my bland bullet points into powerful achievement statements. My interview rate jumped from 5% to 30%.",
                "rating": 5,
            },
            {
                "name": "Vikram Joshi",
                "role": "Full Stack Developer",
                "company": "Flipkart",
                "quote": "I used the compare feature to track my resume improvements over 3 iterations. Watching my score go from 52 to 89 was incredibly motivating.",
                "rating": 4,
            },
            {
                "name": "Sneha Reddy",
                "role": "UX Designer",
                "company": "Swiggy",
                "quote": "As a designer, I thought ATS systems wouldn't affect me — I was wrong. i-Luffy showed me formatting issues that were getting my resume auto-rejected.",
                "rating": 5,
            },
            {
                "name": "Arjun Nair",
                "role": "DevOps Engineer",
                "company": "Razorpay",
                "quote": "The keyword analysis found 12 missing technical terms from the job description. After adding them naturally, I landed 3 interviews in one week.",
                "rating": 5,
            },
        ]
        for i, t in enumerate(testimonials, 1):
            Testimonial.objects.create(order=i, **t)

        self.stdout.write(self.style.SUCCESS("  ✓ Testimonials seeded"))

    def _seed_contact_info(self):
        ContactInfo.objects.get_or_create(
            pk=1,
            defaults={
                "support_email": "support@iluffy.com",
                "twitter_url": "https://twitter.com/iluffy_ai",
                "linkedin_url": "https://linkedin.com/company/iluffy",
                "github_url": "https://github.com/iluffy",
                "instagram_url": "https://instagram.com/iluffy_ai",
                "discord_url": "https://discord.gg/iluffy",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ Contact info seeded"))

    def _seed_site_config(self):
        SiteConfig.objects.get_or_create(
            pk=1,
            defaults={
                "app_base_url": "https://app.iluffy.in",
                "register_path": "/register",
                "login_path": "/login",
                "billing_path": "/billing",
                "sample_report_url": "#",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ Site config seeded"))
