from django.db import models

DEFAULT_PASSWORD = "ganpati123"


class SiteSettings(models.Model):
    """Single-row table holding festival title, UPI info and committee password."""
    festival_name = models.CharField(max_length=200, default="Ganesh Chaturthi")
    street_name = models.CharField(max_length=200, default="Your Street / Colony Name")
    date_range = models.CharField(max_length=200, default="Set festival dates")
    upi_name = models.CharField(max_length=200, blank=True, default="")
    upi_id = models.CharField(max_length=200, blank=True, default="")
    password = models.CharField(max_length=100, default=DEFAULT_PASSWORD)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.festival_name


class ScheduleItem(models.Model):
    day = models.CharField(max_length=100)
    time = models.CharField(max_length=100, blank=True, default="")
    event = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Collection(models.Model):
    """Chanda / contribution entries. Receipt number must be unique."""
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.CharField(max_length=100, unique=True)
    mode = models.CharField(max_length=50, default="Cash")
    date = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Expenditure(models.Model):
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, default="Miscellaneous")
    date = models.CharField(max_length=20, blank=True, default="")
    note = models.CharField(max_length=300, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
