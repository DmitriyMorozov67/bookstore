from django.db import models


def icon_category_path(instance: 'Category', filename: str) -> str:
    if instance.parent:
        return 'catalog/icons/{subcategory}/{category}/{filename}'.format(
            subcategory=instance.parent,
            category=instance.title,
            filename=filename
        )
    else:
        return 'catalog/icons/{category}/{filename}'.format(
            category=instance.title,
            filename=filename
        )


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    activate = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='subcategories'
                               )
    image = models.ImageField(upload_to=icon_category_path, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk',]

    def href(self):
        return f'catalog/{self.pk}'

    def __str__(self):
        return self.title
