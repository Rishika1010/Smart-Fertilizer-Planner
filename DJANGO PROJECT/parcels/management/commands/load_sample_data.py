from django.core.management.base import BaseCommand
from parcels.models import Crop
from fertilizers.models import FertilizerProduct


class Command(BaseCommand):
    help = 'Load sample crops and fertilizer products'

    def handle(self, *args, **options):
        # Create sample crops
        crops_data = [
            {
                'name': 'Wheat',
                'description': 'Common wheat crop',
                'nitrogen_requirement': 120,
                'phosphorus_requirement': 60,
                'potassium_requirement': 50,
            },
            {
                'name': 'Rice',
                'description': 'Paddy rice crop',
                'nitrogen_requirement': 150,
                'phosphorus_requirement': 40,
                'potassium_requirement': 60,
            },
            {
                'name': 'Corn/Maize',
                'description': 'Maize crop',
                'nitrogen_requirement': 180,
                'phosphorus_requirement': 50,
                'potassium_requirement': 70,
            },
            {
                'name': 'Soybean',
                'description': 'Soybean crop',
                'nitrogen_requirement': 80,
                'phosphorus_requirement': 40,
                'potassium_requirement': 50,
            },
            {
                'name': 'Tomato',
                'description': 'Tomato crop',
                'nitrogen_requirement': 200,
                'phosphorus_requirement': 80,
                'potassium_requirement': 150,
            },
        ]

        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created crop: {crop.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Crop already exists: {crop.name}'))

        # Create sample fertilizer products
        fertilizers_data = [
            {
                'name': 'Urea',
                'brand': 'Generic',
                'nitrogen_percent': 46,
                'phosphorus_percent': 0,
                'potassium_percent': 0,
                'price_per_unit': 0.50,
                'unit': 'kg',
                'description': 'Urea - High nitrogen fertilizer',
                'is_active': True,
            },
            {
                'name': 'DAP (Diammonium Phosphate)',
                'brand': 'Generic',
                'nitrogen_percent': 18,
                'phosphorus_percent': 46,
                'potassium_percent': 0,
                'price_per_unit': 0.80,
                'unit': 'kg',
                'description': 'DAP - Nitrogen and Phosphorus fertilizer',
                'is_active': True,
            },
            {
                'name': 'MOP (Muriate of Potash)',
                'brand': 'Generic',
                'nitrogen_percent': 0,
                'phosphorus_percent': 0,
                'potassium_percent': 60,
                'price_per_unit': 0.60,
                'unit': 'kg',
                'description': 'MOP - High potassium fertilizer',
                'is_active': True,
            },
            {
                'name': 'NPK 15-15-15',
                'brand': 'Generic',
                'nitrogen_percent': 15,
                'phosphorus_percent': 15,
                'potassium_percent': 15,
                'price_per_unit': 1.00,
                'unit': 'kg',
                'description': 'Balanced NPK fertilizer',
                'is_active': True,
            },
            {
                'name': 'NPK 20-20-20',
                'brand': 'Premium',
                'nitrogen_percent': 20,
                'phosphorus_percent': 20,
                'potassium_percent': 20,
                'price_per_unit': 1.20,
                'unit': 'kg',
                'description': 'Premium balanced NPK fertilizer',
                'is_active': True,
            },
            {
                'name': 'Super Phosphate',
                'brand': 'Generic',
                'nitrogen_percent': 0,
                'phosphorus_percent': 20,
                'potassium_percent': 0,
                'price_per_unit': 0.40,
                'unit': 'kg',
                'description': 'Phosphorus fertilizer',
                'is_active': True,
            },
        ]

        for fert_data in fertilizers_data:
            fertilizer, created = FertilizerProduct.objects.get_or_create(
                name=fert_data['name'],
                brand=fert_data.get('brand', ''),
                defaults=fert_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created fertilizer: {fertilizer.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Fertilizer already exists: {fertilizer.name}'))

        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))

