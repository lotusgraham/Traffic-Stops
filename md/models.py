from django.db import models

from caching.base import CachingManager, CachingMixin

# Columns in CSV:
# get applicable columns from md csv


YN_CHOICES = (
    ("Y", "Yes"),
    ("N", "No")
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("U", "Unknown")
)

ETHNICITY_CHOICES = (
    ('W', 'White'),
    ('B', 'Black'),
    ('H', 'Hispanic'),
    ('A', 'Asian'),
    ('I', 'Native American'),
    ('U', 'Unknown'),  # unknown includes "Other"
)


class Stop(CachingMixin, models.Model):
    """
    "null=True" for some fields is a temporary solution for this import
    error: "null value in column "what_searched" violates not-null constraint"
    """
    stop_id = models.IntegerField(primary_key=True, default=1)
    date = models.DateTimeField(null=True)
    stop_date_text = models.CharField(max_length=20, blank=True, default='')
    stop_time_text = models.CharField(max_length=20, blank=True, default='')
    stop_location = models.CharField(max_length=1024)
    duration_text = models.CharField(max_length=20, blank=True, null=True)
    stop_reason = models.CharField(max_length=64)
    search_conducted = models.CharField(max_length=1, choices=YN_CHOICES, blank=True)
    search_reason = models.CharField(max_length=64, blank=True)
    seized = models.CharField(max_length=1, choices=YN_CHOICES, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth_text = models.CharField(max_length=20, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, choices=ETHNICITY_CHOICES, blank=True)
    officer_id = models.CharField(max_length=15, blank=True, default=None)
    agency_description = models.CharField(max_length=100)
    agency = models.ForeignKey('Agency', null=True, related_name='stops')
    age = models.PositiveSmallIntegerField(default=0)

    objects = CachingManager()

    def __str__(self):
        return 'Stop %d at %s at %s' % (
            self.stop_id, self.date, self.stop_location
        )


class Agency(CachingMixin, models.Model):
    name = models.CharField(max_length=255)

    objects = CachingManager()

    class Meta(object):
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name
