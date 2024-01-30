from django.db import models

# Create your models h
def shoes_directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.title, filename)


class Option(models.Model):
    option = models.CharField(max_length=300)
    id_brand = models.AutoField(primary_key=True)



    def __str__(self):
        return str(self.option)


class Shoes(models.Model):
    # CHOICES = ((option, option) for option in Option.objects.all())
    CHOICES = (("Nike", "Nike"), ("Adidas", "Adidas"))

    description = models.TextField()
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    auto_increment_id = models.AutoField(primary_key=True)
    size = models.FloatField(default=40.0)
    quantity = models.IntegerField(default=1)
    id_brand = models.ForeignKey(Option, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.title

    @property
    def price_in_cents(self):
        return self.price * 100

    @property
    def price_cents_tva(self):
        return int(round(self.price_in_cents * 1.074, 0))

    @property
    def price_tva(self):
        return round(self.price * 1.074, 2)

    # def update_choices(self, key: str, value: str):
    #     if key not in self.CHOICES:
    #         self.CHOICES = self.CHOICES + (key, value)


class Images(models.Model):
    images = models.ImageField(upload_to="images/")
    img_id = models.ForeignKey(Shoes, on_delete=models.CASCADE)

class Nike(models.Model):
    name = models.CharField(max_length=300)



