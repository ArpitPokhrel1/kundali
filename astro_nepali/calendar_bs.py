"""Bikram Sambat (BS) <-> Gregorian (AD) date conversion.

Backed by the well-tested `nepali-datetime` package, which uses the official
panchanga data published by the Government of Nepal.
"""
from datetime import date
import nepali_datetime


def bs_to_ad(bs_year: int, bs_month: int, bs_day: int) -> date:
    """Convert Bikram Sambat date to Gregorian (AD) date."""
    return nepali_datetime.date(bs_year, bs_month, bs_day).to_datetime_date()


def ad_to_bs(ad_date: date) -> tuple[int, int, int]:
    """Convert Gregorian (AD) date to Bikram Sambat (year, month, day)."""
    bs = nepali_datetime.date.from_datetime_date(ad_date)
    return bs.year, bs.month, bs.day
