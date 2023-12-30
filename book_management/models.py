from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    # Add additional fields if needed
    address = models.TextField()

    class Meta:
        # Add related_name attributes to resolve clashes
        # Set related_name to avoid clashes with default User model's relationships
        # related_name sets the reverse relation name for the ForeignKey from Group and Permission models
        # Change these related names as needed
        permissions = [
            ("can_view_custom", "Can view custom"),
            # Add more custom permissions here if needed
        ]

    # Add related_name attributes to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"
