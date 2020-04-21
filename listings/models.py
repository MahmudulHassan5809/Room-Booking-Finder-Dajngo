from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250)
    image = models.ImageField(
        upload_to="category/%Y/%m/%d/", blank=True, null=True)

    class Meta():
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    print(unique_slug)
    return unique_slug


class ActiveListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Listing(models.Model):
    STATUS_CHOICES = (
        ('0', 'Rent'),
        ('1', 'Sale'),
    )

    ROOMS_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
        ('4', 'Four'),
        ('5', 'Five'),
        ('6', 'FIx'),
    )

    WASHROOM_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_listings')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_listings')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    description = models.TextField()

    price = models.FloatField()

    area = models.CharField(max_length=200)

    rooms = models.CharField(max_length=10, choices=ROOMS_CHOICES)
    wash_rooms = models.CharField(max_length=10, choices=WASHROOM_CHOICES)

    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)

    active = models.BooleanField(default=True)
    booked = models.BooleanField(default=False)

    start_time = models.DateField()
    end_time = models.DateField(null=True, blank=True)

    tags = TaggableManager()

    objects = models.Manager()
    active_objects = ActiveListingManager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Listing, self.title)
        else:
            self.slug = generate_unique_slug(Listing, self.title)
        super(Listing, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listings:update_listings', args=[str(self.slug)])

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='listing_images')
    image = models.ImageField(upload_to="product/%Y/%m/%d/")

    def __str__(self):
        return self.listing.title


class ListingExtra(models.Model):
    STATUS_CHOICES = (
        ('0', 'No'),
        ('1', 'Yes'),
    )

    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='listing_extras')
    facility_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.listing.title