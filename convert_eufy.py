#!/usr/bin/python3

import csv
import sys
import click
from dataclasses import dataclass

import click
import rich
from rich.console import Console
import datetime

EUFY_COLUMN_CONVERSIONS = {
  "Time": "Date",
  "Family Members" : None,
  "WEIGHT (kg)": 	"Body Weight",
  "BMI" : "BMI",
  "BODY FAT %": "Body Fat",
  "HEART RATE (bpm)": None,
  "MUSCLE MASS (kg)": "Skeletal Muscle Mass",
  "MUSCLE MASS %": None,
  "BMR	WATER	": "Body Water",
  "BODY FAT MASS (kg)": None,
  "LEAN BODY MASS (kg)": None,
  "BONE MASS (kg)": "Bone Mass",
  "BONE MASS %": None,
  "VISCERAL FAT	": None,
  "PROTEIN %": None,
  "SKELETAL MUSCLE MASS (kg)": None,
  "SUBCUTANEOUS FAT %": None,
  "BODY AGE": None,
  "BODY TYPE": None,
  "HEAD SIZE (cm)": None
}

@dataclass
class WeightEntry:
  time: datetime.date
  weight: float  # weight in kg
  bmi: float
  family_member: str = ""  # name of user
  body_fat: float = 0  # % of body weight due to fat
  heart_rate: float = 0
  muscle_mass: float = 0  # muscle mass in body in kg
  muscle_mass_percent: float = 0  # % of body weight due to muscle
  bmr_water: float = 0
  body_fat_mass: float = 0    # fat in body in kg
  lean_body_mass: float = 0  # lean body mass in kg
  bone_mass: float = 0  # mass of bones in kg
  bone_mass_percentage: float = 0  # % of body weight due to bones
  visceral_fat_mass: float = 0  #
  protein_percentage: float = 0  # % of protein in body
  skeletal_muscle_mass: float = 0  # mass of skeletal muscle in kg
  subcutaneous_fat_percentage: float = 0  # % of subcutaneous fat
  body_age: float = 0  # estimated body age
  body_type: str = ""  # body type categorization
  head_size: float = 0  # size of head in cm

@click.command()
@click.option('--start', help="Start date in YYYY-MM-DD format", required=False)
@click.option('--end', help="End date in YYYY-MM-DD format", required=False)
@click.option('--since', help="Start date in YYYY-MM", required=False)
def interactive_export(filename: str, entries: list[WeightEntry], export_fields: list[str]) -> None:
  pass

@click.command()
@click.option('--start', help="Start date in YYYY-MM-DD format", required=False)
@click.option('--end', help="End date in YYYY-MM-DD format", required=False)
@click.option('--since', help="Start date in YYYY-MM", required=False)
def batch_export(filename: str, entries: list[WeightEntry], export_fields: list[str]) -> None:
  """
  Export data to csv file that Garmin Copnnect can import
  :param filename: string with name of file to open
  :param entries: data to export to file
  :parma export_fields: list of fields to export
  :return: None
  """
  with open(filename, "w") as f:
    csv_writer = csv.writer(f, fieldnames=export_fields)

    for entry in entries:
      row = []
      for field in export_fields:
        match field:
          case "time":
            row.append(entry.time)
          case "weight":
            row.append(entry.weight)
          case "bmi":
            row.append(entry.bmi)
          case "body_fat":
            row.append(entry.body_fat)
          case "muscle_mass":
            row.append(entry.muscle_mass)
          case "bmr_water":
            row.append(entry.bmr_water)
          case "bone_mass":
            row.append(entry.bone_mass)
          case (\
            "family_member" |
            "heart_rate" |
            "muscle_mass_percent" |
            "body_fat_mass" |
            "lean_body_mass" |
            "bone_mass_percentage" |
            "visceral_fat_mass" |
            "protein_percentage" |
            "skeletal_muscle_mass" |
            "subcutaneous_fat_percentage" |
            "body_age" |
            "body_type" |
            "head_size"
          ):
            pass
          case _:
            pass
      csv_writer.writerow(row)


def main() -> None:
  if __name__ == "__main__":
    sys.exit(0)


