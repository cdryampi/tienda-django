from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cart.models import Cart, CartItem
from accounts.models import User
from common.models import Category, Tag
from core.models import MetadataModel, MetaBase, AuditModel, BurgerType, Allergy
from pricing.models import PriceProduct
from product.models import Product


class Command(BaseCommand):

    help = "Delete all data from the database"

    def handle(self, *args, **options):
        self.stdout.write("Deleting all data from the database")
        # Delete all data
        Cart.objects.all().delete()
        CartItem.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        BurgerType.objects.all().delete()
        Allergy.objects.all().delete()
        PriceProduct.objects.all().delete()
        Product.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()
        ContentType.objects.all().delete()
        BurgerType.objects.all().delete()
        Allergy.objects.all().delete()
        
        self.stdout.write("All data deleted")
