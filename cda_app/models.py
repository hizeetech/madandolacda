from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CDA(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cda = models.ForeignKey(CDA, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Levy(models.Model):
    CDA_CHOICES = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    LEVY_TYPE_CHOICES = [
        ('Development Fees', 'Development Fees'),
        ('Others', 'Others'),
        ('Electricity', 'Electricity'),
        ('Security Fees', 'Security Fees'),
    ]

    cda = models.ForeignKey(CDA, on_delete=models.CASCADE, null=True, blank=True, help_text="Leave blank for joint payments (Electricity, Security Fees)")
    levy_type = models.CharField(max_length=50, choices=LEVY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.levy_type} - {self.amount}"

class UserLevy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    levy = models.ForeignKey(Levy, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.levy.levy_type} - Due: {self.amount_due}"

class Payment(models.Model):
    user_levy = models.ForeignKey(UserLevy, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.user_levy.user.username} for {self.user_levy.levy.levy_type}"


class ExecutiveMember(models.Model):
    cda = models.ForeignKey(CDA, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='executive_members/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

class Defaulter(models.Model):
    image = models.ImageField(upload_to='defaulter_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    cda_choices = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    cda = models.CharField(max_length=100, choices=cda_choices, verbose_name="CDA")
    amount_indebted = models.DecimalField(max_digits=10, decimal_places=2)
    debt_for_choices = [
        ('Security Fees', 'Security Fees'),
        ('Electricity', 'Electricity'),
        ('Development Levy', 'Development Levy'),
        ('Others', 'Others'),
    ]
    title_defaulted = models.CharField(max_length=200, choices=debt_for_choices, verbose_name="Debt For:")
    status_choices = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('In Progress', 'In Progress'),
        ('Indebt', 'Indebt'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Pending')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.title_defaulted}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} on {self.date}"

class CommunityInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Community Info"

    def __str__(self):
        return self.title

class NavbarImage(models.Model):
    POSITION_CHOICES = [
        ('left', 'Left Corner'),
        ('right', 'Right Corner'),
    ]
    image = models.ImageField(upload_to='navbar_images/')
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Navbar Image ({self.position})"

class PaidMember(models.Model):
    image = models.ImageField(upload_to='paid_member_images/', blank=True, null=True)
    name = models.CharField(max_length=100)
    cda_choices = [
        ('Unity CDA', 'Unity CDA'),
        ('Harmony CDA', 'Harmony CDA'),
        ('Valley-View CDA', 'Valley-View CDA'),
    ]
    cda = models.CharField(max_length=100, choices=cda_choices, verbose_name="CDA")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    purpose_choices = [
        ('Security Fees', 'Security Fees'),
        ('Electricity', 'Electricity'),
        ('Development Levy', 'Development Levy'),
        ('Others', 'Others'),
    ]
    purpose_of_payment = models.CharField(max_length=200, choices=purpose_choices, verbose_name="Purpose of Payment")
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount_paid} ({self.purpose_of_payment})"


class Committee(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    roles_responsibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CommitteeMember(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    image = models.ImageField(upload_to='committee_members/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.committee.name}"

class CommitteeToDo(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='todos')
    task = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.task} ({self.committee.name})"

class CommitteeAchievement(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.committee.name})"

class AdvertCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ProjectDonation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    beneficiary = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(ProjectDonation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"

class DonationProof(models.Model):
    project_donation = models.ForeignKey(ProjectDonation, on_delete=models.CASCADE, related_name='donation_proofs')
    donator_name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=20)
    donated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_receipt_image = models.ImageField(upload_to='donation_proofs/')
    donation_reference_number = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proof for {self.project_donation.title} by {self.donator_name}"

class AdvertItem(models.Model):
    CATEGORY_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
        ('For Lease', 'For Lease'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

class AdvertImage(models.Model):
    advert_item = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='advert_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.advert_item.title}"

class Proposal(models.Model):
    advert = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='proposals')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    proposed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal for {self.advert.title} by {self.name}"

class AdvertMessage(models.Model):
    advert = models.ForeignKey(AdvertItem, on_delete=models.CASCADE, related_name='messages')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    willing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.advert.title} from {self.name}"

class Artisan(models.Model):
    image = models.ImageField(upload_to='artisans/', blank=True, null=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class Professional(models.Model):
    image = models.ImageField(upload_to='professionals/', blank=True, null=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
