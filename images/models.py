from django.db import models 
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse 



class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE,
                             related_name='images_created',)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL,  # a many-to-many field
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            ]
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    # overiding save() to include slug automatically
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
