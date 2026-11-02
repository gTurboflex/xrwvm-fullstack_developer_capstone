import json
from pathlib import Path

from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel


class Command(BaseCommand):
    help = "Load the provided sample car records into the dealership portal"

    def handle(self, *args, **options):
        data_path = Path(__file__).resolve().parents[3] / "database" / "data" / "car_records.json"
        cars = json.loads(data_path.read_text(encoding="utf-8"))["cars"]
        created = 0
        for item in cars:
            make, _ = CarMake.objects.get_or_create(name=item["make"])
            _, was_created = CarModel.objects.get_or_create(
                car_make=make,
                name=item["model"],
                dealer_id=item["dealer_id"],
                year=item["year"],
                defaults={"type": item["bodyType"]},
            )
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Loaded {created} new cars; {CarModel.objects.count()} total"))
