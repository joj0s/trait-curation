"""
This module contains utility functions for downloading, parsing and storing trait data fron ClinVar
"""

import csv
import gzip
import itertools
import os
import urllib.request

from ..models import Trait

# Constants to use. URL defines the clinvar data location and NUMBER_OF_RECORDS defines how many traits to parse
# during development.
URL = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz'
NUMBER_OF_RECORDS = 200


def download_clinvar_data():
    """
    This function downloads the latest ClinVar TSV release data and extracts it into a 'variant_summary.txt' file
    """
    print("Downloading ClinVar data...")
    urllib.request.urlretrieve(URL, './variant_summary.txt.gz')


def parse_trait_names_and_source_records():
    """
    This function parses a downloaded 'variant_summary.txt' file, and returns a unique set of trait names
    along with their calculated source record number, in a form of a dictionary where the key is the trait name
    and the value is the source record number.
    """
    print("Parsing ClinVar data...")
    with gzip.open('variant_summary.txt.gz', 'rt') as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab')
        # A dictionary with trait names as keys and sets of source records as values
        traits_dict = dict()
        # The int value here defines how many records should be parsed
        for row in itertools.islice(reader, NUMBER_OF_RECORDS):
            # For every row, get its allele_id and all its rcv_accessions and phenotypes
            row_alleleid = (row['#AlleleID'])
            row_rcv_list = row['RCVaccession'].split(';')
            row_phenotype_list = row['PhenotypeList'].split(';')
            # Get every possible pair tuple of allele_id rcv_accessions and phenotypes for the current row
            tuple_set = {(row_alleleid, rcv, phenotype) for rcv, phenotype in zip(row_rcv_list, row_phenotype_list)}
            # Insert the tuple in the dictionary
            for tuple in tuple_set:
                trait_name = tuple[2]
                traits_dict.setdefault(trait_name, set())
                traits_dict[trait_name].update([tuple])
        # Count the number of source records for each trait name
        for key in traits_dict.keys():
            traits_dict[key] = len(traits_dict[key])
        os.remove("variant_summary.txt.gz")
        return traits_dict


def store_data(traits_dict):
    """
    This function accepts a dictionary in the form of keys=trait names and values=source record numbers
    and stores them in the database using the Django ORM.
    """
    print("Storing ClinVar data...")
    for trait_name in traits_dict.keys():
        if Trait.objects.filter(name=trait_name).exists():
            trait = Trait.objects.filter(name=trait_name).first()
            trait.number_of_source_records = traits_dict[trait_name]
        else:
            trait = Trait(name=trait_name, status="unmapped",
                          number_of_source_records=traits_dict[trait_name])
        trait.save()
