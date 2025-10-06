from django.core.management.base import BaseCommand
from analytics.models import Region

class Command(BaseCommand):
    help = 'Seed US states data for the regional popularity map'

    def handle(self, *args, **kwargs):
        # Sample of US states with approximate center coordinates
        states_data = [
            {'name': 'Alabama', 'code': 'AL', 'latitude': 32.806671, 'longitude': -86.791130},
            {'name': 'Alaska', 'code': 'AK', 'latitude': 61.370716, 'longitude': -152.404419},
            {'name': 'Arizona', 'code': 'AZ', 'latitude': 33.729759, 'longitude': -111.431221},
            {'name': 'Arkansas', 'code': 'AR', 'latitude': 34.969704, 'longitude': -92.373123},
            {'name': 'California', 'code': 'CA', 'latitude': 36.116203, 'longitude': -119.681564},
            {'name': 'Colorado', 'code': 'CO', 'latitude': 39.059811, 'longitude': -105.311104},
            {'name': 'Connecticut', 'code': 'CT', 'latitude': 41.597782, 'longitude': -72.755371},
            {'name': 'Delaware', 'code': 'DE', 'latitude': 39.318523, 'longitude': -75.507141},
            {'name': 'Florida', 'code': 'FL', 'latitude': 27.766279, 'longitude': -81.686783},
            {'name': 'Georgia', 'code': 'GA', 'latitude': 33.040619, 'longitude': -83.643074},
            {'name': 'Hawaii', 'code': 'HI', 'latitude': 21.094318, 'longitude': -157.498337},
            {'name': 'Idaho', 'code': 'ID', 'latitude': 44.240459, 'longitude': -114.478828},
            {'name': 'Illinois', 'code': 'IL', 'latitude': 40.349457, 'longitude': -88.986137},
            {'name': 'Indiana', 'code': 'IN', 'latitude': 39.849426, 'longitude': -86.258278},
            {'name': 'Iowa', 'code': 'IA', 'latitude': 42.011539, 'longitude': -93.210526},
            {'name': 'Kansas', 'code': 'KS', 'latitude': 38.526600, 'longitude': -96.726486},
            {'name': 'Kentucky', 'code': 'KY', 'latitude': 37.668140, 'longitude': -84.670067},
            {'name': 'Louisiana', 'code': 'LA', 'latitude': 31.169546, 'longitude': -91.867805},
            {'name': 'Maine', 'code': 'ME', 'latitude': 44.693947, 'longitude': -69.381927},
            {'name': 'Maryland', 'code': 'MD', 'latitude': 39.063946, 'longitude': -76.802101},
            {'name': 'Massachusetts', 'code': 'MA', 'latitude': 42.230171, 'longitude': -71.530106},
            {'name': 'Michigan', 'code': 'MI', 'latitude': 43.326618, 'longitude': -84.536095},
            {'name': 'Minnesota', 'code': 'MN', 'latitude': 45.694454, 'longitude': -93.900192},
            {'name': 'Mississippi', 'code': 'MS', 'latitude': 32.741646, 'longitude': -89.678696},
            {'name': 'Missouri', 'code': 'MO', 'latitude': 38.456085, 'longitude': -92.288368},
            {'name': 'Montana', 'code': 'MT', 'latitude': 46.921925, 'longitude': -110.454353},
            {'name': 'Nebraska', 'code': 'NE', 'latitude': 41.125370, 'longitude': -98.268082},
            {'name': 'Nevada', 'code': 'NV', 'latitude': 38.313515, 'longitude': -117.055374},
            {'name': 'New Hampshire', 'code': 'NH', 'latitude': 43.452492, 'longitude': -71.563896},
            {'name': 'New Jersey', 'code': 'NJ', 'latitude': 40.298904, 'longitude': -74.521011},
            {'name': 'New Mexico', 'code': 'NM', 'latitude': 34.840515, 'longitude': -106.248482},
            {'name': 'New York', 'code': 'NY', 'latitude': 42.165726, 'longitude': -74.948051},
            {'name': 'North Carolina', 'code': 'NC', 'latitude': 35.630066, 'longitude': -79.806419},
            {'name': 'North Dakota', 'code': 'ND', 'latitude': 47.528912, 'longitude': -99.784012},
            {'name': 'Ohio', 'code': 'OH', 'latitude': 40.388783, 'longitude': -82.764915},
            {'name': 'Oklahoma', 'code': 'OK', 'latitude': 35.565342, 'longitude': -96.928917},
            {'name': 'Oregon', 'code': 'OR', 'latitude': 44.572021, 'longitude': -122.070938},
            {'name': 'Pennsylvania', 'code': 'PA', 'latitude': 40.590752, 'longitude': -77.209755},
            {'name': 'Rhode Island', 'code': 'RI', 'latitude': 41.680893, 'longitude': -71.511780},
            {'name': 'South Carolina', 'code': 'SC', 'latitude': 33.856892, 'longitude': -80.945007},
            {'name': 'South Dakota', 'code': 'SD', 'latitude': 44.299782, 'longitude': -99.438828},
            {'name': 'Tennessee', 'code': 'TN', 'latitude': 35.747845, 'longitude': -86.692345},
            {'name': 'Texas', 'code': 'TX', 'latitude': 31.054487, 'longitude': -97.563461},
            {'name': 'Utah', 'code': 'UT', 'latitude': 40.150032, 'longitude': -111.862434},
            {'name': 'Vermont', 'code': 'VT', 'latitude': 44.045876, 'longitude': -72.710686},
            {'name': 'Virginia', 'code': 'VA', 'latitude': 37.769337, 'longitude': -78.169968},
            {'name': 'Washington', 'code': 'WA', 'latitude': 47.400902, 'longitude': -121.490494},
            {'name': 'West Virginia', 'code': 'WV', 'latitude': 38.491226, 'longitude': -80.954453},
            {'name': 'Wisconsin', 'code': 'WI', 'latitude': 44.268543, 'longitude': -89.616508},
            {'name': 'Wyoming', 'code': 'WY', 'latitude': 42.755966, 'longitude': -107.302490},
        ]

        created_count = 0
        for state_data in states_data:
            region, created = Region.objects.get_or_create(
                code=state_data['code'],
                defaults=state_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created region: {region.name}'))
            else:
                self.stdout.write(f'Region already exists: {region.name}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Seeded {created_count} new states'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total regions in database: {Region.objects.count()}'))
