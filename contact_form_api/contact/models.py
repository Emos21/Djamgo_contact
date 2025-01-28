from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Enter your full name"
    )
    email = models.EmailField(
        max_length=254,  # RFC 5321 standard max email length
        help_text="Enter a valid email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'"
        )],
        help_text="Optional contact phone number"
    )
    message = models.TextField(
        help_text="Enter your message here"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # Better for filtering/sorting
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class HireRequest(models.Model):
    SERVICE_CHOICES = [
        ('graphic', 'Graphic Design'),
        ('web', 'Web Development'),
        ('both', 'Both Services'),
    ]
    
    email = models.EmailField(
        max_length=254,
        help_text="Enter your professional email address"
    )
    service_needed = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES,
        db_index=True,  # Better for filtering
        help_text="Select required service type"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Hire Request"
        verbose_name_plural = "Hire Requests"
        unique_together = ['email', 'service_needed']  # Prevent duplicate requests

    def __str__(self):
        return f"{self.email} - {self.get_service_needed_display()} ({self.created_at.strftime('%Y-%m-%d')})"