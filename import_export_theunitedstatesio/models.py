# import_export_theunitedstatesio/models.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from django.db import models
from exception.models import handle_exception, handle_record_not_found_exception
import csv
from datetime import datetime
from collections import namedtuple

LEGISLATORS_CURRENT_CSV_FILE = 'import_export_theunitedstatesio/import_data/legislators-current.csv'
# UnitedStates.io CSV Field names
legislators_current_fields = (
    "last_name",              # row[0]
    "first_name",             # row[1]
    "birthday",               # row[2]
    "gender",                 # row[3]
    "type",                   # row[4]
    "state",                  # row[5]
    "district",               # row[6]
    "party",                  # row[7]
    "url",                    # row[8]
    "address",                # row[9]
    "phone",                  # row[10]
    "contact_form",           # row[11]
    "rss_url",                # row[12]
    "twitter",                # row[13]
    "facebook",               # row[14]
    "facebook_id",            # row[15]
    "youtube",                # row[16]
    "youtube_id",             # row[17]
    "bioguide_id",            # row[18]
    "thomas_id",              # row[19]
    "opensecrets_id",         # row[20]
    "lis_id",                 # row[21]
    "cspan_id",               # row[22]
    "govtrack_id",            # row[23]
    "votesmart_id",           # row[24]
    "ballotpedia_id",         # row[25]
    "washington_post_id",     # row[26]
    "icpsr_id",               # row[27]
    "wikipedia_id"            # row[28]
)


class TheUnitedStatesIoLegislatorCurrent(models.Model):
    # We are relying on built-in Python id field
    last_name = models.CharField(verbose_name="last_name",
                                 max_length=254, default=None, null=True, blank=True)
    first_name = models.CharField(verbose_name="first_name",
                                  max_length=254, default=None, null=True, blank=True)
    birthday = models.DateField("birthday", default=None, null=True, blank=True)
    gender = models.CharField("gender", max_length=10)
    type = models.CharField("type", max_length=254)
    state = models.CharField("state", max_length=25)
    district = models.CharField("district", max_length=254)  # is only used for "rep" (House of Rep) and not
        # "sen" (Senators). This is a number related to state district
    party = models.CharField("party", max_length=254)
    url = models.CharField("url", max_length=254)
    address = models.CharField("address", max_length=254)
    phone = models.CharField("phone", max_length=254)
    contact_form = models.CharField("contact_form", max_length=254)
    rss_url = models.CharField("rss_url", max_length=254)
    twitter = models.CharField("twitter", max_length=254)
    facebook = models.CharField("facebook", max_length=254)
    facebook_id = models.CharField("facebook_id", max_length=254)
    youtube = models.CharField("youtube", max_length=254)
    youtube_id = models.CharField(verbose_name="youtube_id",
                                  max_length=500, default=None, null=True, blank=True)
    bioguide_id = models.CharField(verbose_name="bioguide unique identifier",
                                   max_length=200, null=True, unique=True)
    thomas_id = models.CharField(verbose_name="thomas unique identifier",
                                 max_length=200, null=True, unique=True)
    opensecrets_id = models.CharField(verbose_name="opensecrets unique identifier",
                                      max_length=200, null=True, unique=False)
    lis_id = models.CharField(verbose_name="lis unique identifier",
                              max_length=200, null=True, unique=False)
    cspan_id = models.CharField(verbose_name="cspan unique identifier",
                                max_length=200, null=True, unique=False)
    govtrack_id = models.CharField(verbose_name="govtrack unique identifier",
                                   max_length=200, null=True, unique=True)
    votesmart_id = models.CharField(verbose_name="votesmart unique identifier",
                                    max_length=200, null=True, unique=False)
    ballotpedia_id = models.CharField(verbose_name="ballotpedia id",
                                      max_length=500, default=None, null=True, blank=True)
    washington_post_id = models.CharField(verbose_name="washington post unique identifier",
                                          max_length=200, null=True)
    icpsr_id = models.CharField(verbose_name="icpsr unique identifier",
                                max_length=200, null=True, unique=False)
    wikipedia_id = models.CharField(verbose_name="wikipedia id",
                                    max_length=500, default=None, null=True, blank=True)

    # race = enum?
    # official_image_id = ??

    # bioguide_id, thomas_id, lis_id, govtrack_id, opensecrets_id, votesmart_id, fec_id, cspan_id, wikipedia_id,
    # ballotpedia_id, house_history_id, maplight_id, washington_post_id, icpsr_id, first_name, middle_name,
    # last_name, name_official_full, gender, birth_date
    # Has this entry been processed and transferred to the live We Vote tables?
    was_processed = models.BooleanField(verbose_name="is primary election", default=False, null=False, blank=False)


def import_legislators_current_csv():
    """
    This is a very simple method that is hard coded to the UnitedStates.io CSV Field names. We are saving
    the contents of this file locally so we can
    1) share the data on ElectionDataSummary.org dynamically
    2) save it/merge it into the correct We Vote tables later
    :return:
    """
    with open(LEGISLATORS_CURRENT_CSV_FILE, 'rU') as legislators_current_data:
        legislators_current_data.readline()             # Skip the header
        reader = csv.reader(legislators_current_data)   # Create a regular tuple reader
        for index, legislator_row in enumerate(reader):
            # if index > 7:
            #     break
            # print "import_legislators_current_csv: " + legislator_row[0] # For debugging
            legislator_entry_found = False

            # Do we have a record of this legislator based on bioguide_id?
            if legislator_row[18] != "":
                try:
                    query1 = TheUnitedStatesIoLegislatorCurrent.objects.all()
                    query1 = query1.filter(bioguide_id__exact=legislator_row[18])

                    # Was at least one existing entry found based on the above criteria?
                    if len(query1):
                        legislator_entry = query1[0]
                        legislator_entry_found = True
                except Exception as e:
                    handle_record_not_found_exception(e)

            if not legislator_entry_found:
                # TheUnitedStatesIoLegislatorCurrent was not found based on bioguide id
                # ...so check to see if we have a record of this legislator based on govtrack id?
                if legislator_row[23] != "":
                    try:
                        query2 = TheUnitedStatesIoLegislatorCurrent.objects.all()
                        query2 = query2.filter(govtrack_id__exact=legislator_row[23])

                        # Was at least one existing entry found based on the above criteria?
                        if len(query2):
                            legislator_entry = query2[0]
                            legislator_entry_found = True
                    except Exception as e:
                        handle_record_not_found_exception(e)

            if not legislator_entry_found:
                # TheUnitedStatesIoLegislatorCurrent was not found based on govtrack id
                # ...so create a new entry
                legislator_entry = TheUnitedStatesIoLegislatorCurrent(
                    last_name=legislator_row[0],                          # "last_name",               # row[0]
                    first_name=legislator_row[1],                         # "first_name",               # row[1]
                )

            legislator_entry.last_name = legislator_row[0]              # "last_name",              # row[0]
            legislator_entry.first_name = legislator_row[1]             # "first_name",             # row[1]
            legislator_entry.birth_date = legislator_row[2]             # "birthday",               # row[2]
            legislator_entry.gender = legislator_row[3]                 # "gender",                 # row[3]
            # "type",                   # row[4]
            legislator_entry.state = legislator_row[5]                  # "state",                  # row[5]
            # "district",               # row[6]  # Convert this to ocd district
            legislator_entry.party = legislator_row[7]                  # "party",                  # row[7]
            # "url",                    # row[8]
            # "address",                # row[9]
            # "phone",                  # row[10]
            # "contact_form",           # row[11]
            # "rss_url",                # row[12]
            # "twitter",                # row[13]
            # "facebook",               # row[14]
            # "facebook_id",            # row[15]
            # "youtube",                # row[16]
            # "youtube_id",             # row[17]
            legislator_entry.bioguide_id = legislator_row[18]           # "bioguide_id",            # row[18]
            legislator_entry.thomas_id = legislator_row[19]             # "thomas_id",              # row[19]
            legislator_entry.opensecrets_id = legislator_row[20]        # "opensecrets_id",         # row[20]
            legislator_entry.lis_id = legislator_row[21]                # "lis_id",                 # row[21]
            legislator_entry.cspan_id = legislator_row[22]              # "cspan_id",               # row[22]
            legislator_entry.govtrack_id = legislator_row[23]           # "govtrack_id",            # row[23]
            legislator_entry.votesmart_id = legislator_row[24]          # "votesmart_id",           # row[24]
            legislator_entry.ballotpedia_id = legislator_row[25]        # "ballotpedia_id",         # row[25]
            legislator_entry.washington_post_id = legislator_row[26]    # "washington_post_id",     # row[26]
            legislator_entry.icpsr_id = legislator_row[27]              # "icpsr_id",               # row[27]
            legislator_entry.wikipedia_id = legislator_row[28]          # "wikipedia_id"            # row[28]

            # Add "try/exception" so we know when entry isn't saved due to unique requirement
            try:
                legislator_entry.save()
            except Exception as e:
                handle_exception(e)


def delete_all_legislator_data():
    with open(LEGISLATORS_CURRENT_CSV_FILE, 'rU') as legislators_current_data:
        legislators_current_data.readline()             # Skip the header
        reader = csv.reader(legislators_current_data)   # Create a regular tuple reader
        for index, legislator_row in enumerate(reader):
            if index > 3:
                break
            legislator_entry = TheUnitedStatesIoLegislatorCurrent.objects.order_by('last_name')[0]
            legislator_entry.delete()