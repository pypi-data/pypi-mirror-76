# -*- encoding: utf-8 -*-

from django.core.management import BaseCommand
from django.db import transaction

from bpp.models import (
    Autor_Dyscyplina,
    Wydawnictwo_Ciagle_Autor,
    Wydawnictwo_Zwarte_Autor,
)
from bpp.models import cache
import logging

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Przemapowuje charaktery formalne"

    def add_arguments(self, parser):
        parser.add_argument("klasa_zrodlowa")
        parser.add_argument("antyklasa")
        parser.add_argument("typ_kbn_zrodlowy")
        parser.add_argument("charakter_formalny_docelowy")
        parser.add_argument("typ_kbn_docelowy")


XXX tu skonczylem
- sciagnac tabelke typow KBN z BPP
- przemapowac charaktery na inne te takie
- dopisac do skryptu makefile

    @transaction.atomic
    def handle(self, verbosity, *args, **options):
        if verbosity > 1:
            logger.setLevel(logging.DEBUG)

        cache.disable()

        for klass in Wydawnictwo_Zwarte, Wydawnictwo_Ciagle:


            _Autor, Wydawnictwo_Ciagle_Autor:
                for instance in klass.objects.filter(
                    autor=ad.autor, rekord__rok=ad.rok, dyscyplina_naukowa=None
                ):
                    logger.debug(
                        f"{ad.autor.pk}\t{ad.autor}\t{ad.rok}\t"
                        f"{ad.dyscyplina_naukowa}\t{instance.rekord.tytul_oryginalny}"
                        f"\t{instance.rekord.pk}"
                    )
                    instance.dyscyplina_naukowa = ad.dyscyplina_naukowa

                    if ad.subdyscyplina_naukowa_id is not None:
                        logger.info(
                            f"Autor {ad.autor} ma za rok {ad.rok} dwie dyscypliny, "
                            f"przypisuję pierwszą do pracy {instance.rekord.tytul_oryginalny} "
                            f"{instance.rekord.rok}"
                        )

                    instance.save()
