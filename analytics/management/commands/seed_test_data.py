from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from analytics.models import Region
from movies.models import Movie
from cart.models import Order, Item
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create test users with regions and purchase data for testing the map'

    def handle(self, *args, **kwargs):
        # Check if we have regions
        if not Region.objects.exists():
            self.stdout.write(self.style.ERROR('No regions found. Run: python manage.py seed_regions first'))
            return

        # Check if we have movies
        if not Movie.objects.exists():
            self.stdout.write(self.style.ERROR('No movies found. Please add some movies first'))
            return

        regions = list(Region.objects.all())
        movies = list(Movie.objects.all())

        # Create test users in different regions
        test_users_data = [
            ('user_ga', 'GA'),
            ('user_ca', 'CA'),
            ('user_ny', 'NY'),
            ('user_tx', 'TX'),
            ('user_fl', 'FL'),
            ('user_il', 'IL'),
            ('user_wa', 'WA'),
            ('user_ma', 'MA'),
        ]

        created_users = 0
        created_orders = 0

        for username, region_code in test_users_data:
            # Create or get user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'password': 'testpass123'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
                created_users += 1
                self.stdout.write(f'Created user: {username}')

            # Set region
            region = Region.objects.get(code=region_code)
            user.profile.region = region
            user.profile.save()

            # Create 2-5 random orders for each user
            num_orders = random.randint(2, 5)
            for _ in range(num_orders):
                # Create order
                total = 0
                order = Order.objects.create(user=user, total=0)
                
                # Add 1-3 random movies to each order
                num_items = random.randint(1, 3)
                selected_movies = random.sample(movies, min(num_items, len(movies)))
                
                for movie in selected_movies:
                    quantity = random.randint(1, 3)
                    Item.objects.create(
                        order=order,
                        movie=movie,
                        price=movie.price,
                        quantity=quantity
                    )
                    total += movie.price * quantity
                
                # Update order total
                order.total = total
                order.save()
                created_orders += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {created_users} new test users'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_orders} test orders'))
        self.stdout.write(self.style.SUCCESS(f'✓ All test users password: testpass123'))
        self.stdout.write(self.style.WARNING(f'\nTest users created:'))
        for username, region_code in test_users_data:
            region = Region.objects.get(code=region_code)
            self.stdout.write(f'  - {username} (Region: {region.name})')
