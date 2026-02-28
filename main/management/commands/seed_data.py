from django.core.management.base import BaseCommand
from main.models import Plan, PlanFeature, Testimonial, ContactInfo


class Command(BaseCommand):
    help = "Seed default plans, testimonials, and contact info"

    def handle(self, *args, **options):
        self._seed_plans()
        self._seed_testimonials()
        self._seed_contact_info()
        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully."))

    def _seed_plans(self):
        if Plan.objects.exists():
            self.stdout.write("Plans already exist — skipping.")
            return

        # ── Free Plan ──────────────────────────────────────────────
        free = Plan.objects.create(
            name="Free",
            tagline="Get started with AI resume analysis — no credit card needed.",
            monthly_price=0,
            annual_price=0,
            is_popular=False,
            cta_label="Start Free Analysis",
            order=1,
        )
        free_features = [
            ("2 credits per month", "Each analysis costs 1 credit — get 2 free credits every month"),
            ("ATS score breakdown", "Scored against Generic ATS, Workday, and Greenhouse parsers"),
            ("Keyword analysis", "See matched, missing, and recommended keywords from the job description"),
            ("Section feedback", "Per-section scores and detailed improvement suggestions"),
            ("AI sentence rewrites", "AI rewrites generic bullets into quantified achievements"),
            ("PDF report download", "Download a comprehensive PDF report of your analysis"),
            ("Compare analyses", "View up to 5 analyses side-by-side to track improvement"),
        ]
        for i, (text, tooltip) in enumerate(free_features, 1):
            PlanFeature.objects.create(plan=free, text=text, tooltip=tooltip, order=i)

        # ── Pro Plan ───────────────────────────────────────────────
        pro = Plan.objects.create(
            name="Pro",
            tagline="For active job seekers who need every edge.",
            monthly_price=399,
            monthly_original_price=599,
            annual_price=3990,           # ₹399/mo × 10
            annual_original_price=7188,  # ₹599/mo × 12
            is_popular=True,
            cta_label="Upgrade to Pro",
            order=2,
        )
        pro_features = [
            ("25 credits per month", "25 credits auto-replenished monthly — plus top-up packs available"),
            ("Priority AI processing", "Skip the queue with dedicated processing priority"),
            ("Share reports via link", "Generate a public link to share your analysis with mentors or friends"),
            ("Smart Job Alerts", "AI-powered job matching with daily or weekly alerts based on your resume"),
            ("AI Resume Generator", "Generate ATS-optimized resumes from your analysis results"),
        ]
        for i, (text, tooltip) in enumerate(pro_features, 1):
            PlanFeature.objects.create(plan=pro, text=text, tooltip=tooltip, order=i)

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
