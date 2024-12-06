#!/usr/bin/python3

import csv
import os
import sys
import datetime
from collections import defaultdict
from dataclasses import dataclass

import click
import rich.emoji
from rich.console import Console
from rich.table import Table
from rich.style import Style
from getkey import getkey, keys
from fit import FitEncoderWeight

EUFY_COLUMN_CONVERSIONS = {
  "Time": "Date",
  "Family Members": None,
  "WEIGHT (kg)": "Body Weight",
  "BMI": "BMI",
  "BODY FAT %": "Body Fat",
  "HEART RATE (bpm)": None,
  "MUSCLE MASS (kg)": "Skeletal Muscle Mass",
  "MUSCLE MASS %": None,
  "BMR": None,
  "WATER": "Body Water",
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
  time: datetime.datetime
  weight: float  # weight in kg
  bmi: float
  family_member: str = ""  # name of user
  body_fat: float = 0  # % of body weight due to fat
  heart_rate: float = 0
  muscle_mass: float = 0  # muscle mass in body in kg
  muscle_mass_percent: float = 0  # % of body weight due to muscle
  bmr: float = 0
  water: float = 0  # mass of water in body in kg
  body_fat_mass: float = 0  # fat in body in kg
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


def convert_fieldname(fieldname: str) -> str:
  """
  Convert fieldname to data class field name

  :param fieldname: field name to convert
  :return: str with converted fieldname
  """
  match fieldname:
    case "Time":
      return "time"
    case "Family Members":
      pass
    case "WEIGHT (kg)":
      return "weight"
    case "BMI":
      return "bmi"
    case "BODY FAT %":
      return "body_fat"
    case "HEART RATE (bpm)":
      return "heart_rate"
    case "MUSCLE MASS (kg)":
      return "muscle_mass"
    case "MUSCLE MASS %":
      return "muscle_mass_percent"
    case "BMR":
      return "bmr"
    case "WATER":
      return "water"
    case "BODY FAT MASS (kg)":
      return "body_fat_mass"
    case "LEAN BODY MASS (kg)":
      return "lean_body_mass"
    case "BONE MASS (kg)":
      return "bone_mass"
    case "BONE MASS %":
      return "bone_mass_percent"
    case "VISCERAL FAT":
      return "visceral_fat_mass"
    case "PROTEIN %":
      return "protein_percentage"
    case "SKELETAL MUSCLE MASS (kg)":
      return "skeletal_muscle_mass"
    case "SUBCUTANEOUS FAT %":
      return "subcutaneous_fat_percentage"
    case "BODY AGE":
      return "body_age"
    case "BODY TYPE":
      return "body_type"
    case "HEAD SIZE (cm)":
      return "head_size"
    case _:
      sys.exit(f"Unrecognized field {fieldname}, exiting\n")


def read_eufyfile(filename: str = None) -> list[WeightEntry]:
  """
  Parse an exported eufy file and return a list with entries

  :param filename: string with name of file to read
  :return: list of WeightEntry objects
  """
  if filename is None:
    sys.exit("Filename not specified, exiting\n")
  if not os.path.exists(filename) or not os.path.isfile(filename):
    sys.exit("File does not exist or is invalid, exiting\n")

  entries = []
  with open(filename, "r", encoding='utf-8-sig') as eufy_file:
    reader = csv.DictReader(eufy_file)
    for row in reader:
      entry = WeightEntry(datetime.datetime.now(), 0.0, 0.0)
      for key, val in row.items():
        match key:
          case "Time":
            entry.time = datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
          case "Family Members":
            pass
          case "WEIGHT (kg)":
            entry.weight = float(val)
          case "BMI":
            entry.bmi = float(val)
          case "BODY FAT %":
            entry.body_fat = float(val)
          case "HEART RATE (bpm)":
            entry.heart_rate = float(val)
          case "MUSCLE MASS (kg)":
            entry.muscle_mass = float(val)
          case "MUSCLE MASS %":
            entry.muscle_mass_percent = float(val)
          case "BMR":
            entry.bmr = float(val)
          case "WATER":
            entry.water = float(val)
          case "BODY FAT MASS (kg)":
            entry.body_fat_mass = float(val)
          case "LEAN BODY MASS (kg)":
            entry.lean_body_mass = float(val)
          case "BONE MASS (kg)":
            entry.bone_mass = float(val)
          case "BONE MASS %":
            entry.bone_mass_percent = float(val)
          case "VISCERAL FAT":
            entry.visceral_fat_mass = float(val)
          case "PROTEIN %":
            entry.protein_percentage = float(val)
          case "SKELETAL MUSCLE MASS (kg)":
            entry.skeletal_muscle_mass = float(val)
          case "SUBCUTANEOUS FAT %":
            entry.subcutaneous_fat_percentage = float(val)
          case "BODY AGE":
            entry.body_age = float(val)
          case "BODY TYPE":
            entry.body_type = str(val)
          case "HEAD SIZE (cm)":
            entry.head_size = float(val)
          case _:
            sys.exit(f"Unrecognized field {key}, exiting\n")
      entries.append(entry)
  return entries


def write_garmin_file(filename: str, entries: list[WeightEntry], fields: list[str] = None) -> None:
  """
  Write a csv file for import to garmin

  :param filename: filename to write
  :param entries: list of WeightEntry objects
  :param fields:  list of fields from entries to export
  :return: None
  """
  if os.path.exists(filename):
    sys.exit("File already exists, exiting\n")
  selected_fields = [convert_fieldname(x) for x in fields]
  if fields is None:
    selected_fields = ["time", "weight", "bmi", "body_fat", "muscle_mass", "bmr", "water", "bone_mass"]

  encoder = FitEncoderWeight()
  encoder.write_file_info()
  encoder.write_file_creator()

  with open(filename, "wb") as f:
    for entry in entries:
      fields = defaultdict(float)
      for field in selected_fields:
        match field:
          case "weight":
            fields["weight"] = entry.weight
          case "bmi":
            fields["bmi"] = entry.bmi
          case "body_fat":
            fields["body_fat"] = entry.body_fat
          case "muscle_mass":
            fields["muscle_mass"] = entry.muscle_mass
          case "bmr":
            fields["bmr"] = entry.bmr
          case "water":
            fields["water"] = entry.water
          case "bone_mass":
            fields["bone_mass"] = entry.bone_mass
          case "body_age":
            fields["body_age"] = entry.body_age
          case "visceral_fat_mass":
            fields["visceral_fat_mass"] = entry.visceral_fat_mass
          case ("family_member" |
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
                "head_size"):
            pass
          case _:
            pass
      print(fields)
      encoder.write_weight_scale(timestamp=entry.time,
                                 weight=fields["weight"],
                                 percent_fat=fields["body_fat"],
                                 percent_hydration=fields["water"],
                                 visceral_fat_mass=fields["visceral_fat_mass"],
                                 bone_mass=fields['bone_mass'],
                                 muscle_mass=fields["muscle_mass"],
                                 basal_met=fields["bmr"],
                                 metabolic_age=fields["body_age"])

    encoder.finish()
    f.write(encoder.getvalue())


def generate_column_table(table_data: list[tuple[str, str]],
                          selected_rows: list[str],
                          cur_row=None) -> Table:
  """
  Generate a table of columns for display

  :param selected_rows: list of selected rows
  :param cur_row: current row
  :param table_data: table data to render
  :return: table to be shown
  """
  cur_row_style = Style(color="black", bgcolor="cornsilk1")
  table = Table(show_header=True, header_style="bold magenta")
  table.add_column("Selected", width=2, max_width=2)
  table.add_column("Column Name (Eufy)")
  table.add_column("Column Name (Garmin)")
  row = 0
  for entry in table_data:
    select_col_char = ""
    if row in selected_rows:
      select_col_char = rich.emoji.Emoji("x")
    if row == cur_row:
      table.add_row(select_col_char, entry[0], entry[1], style=cur_row_style)
    else:
      table.add_row(select_col_char, entry[0], entry[1])
    row += 1
  return table


def select_columns() -> list[str]:
  """
  Select columns to convert from Eufy file
  :return: list with column names
  """
  console = Console()
  selected_rows = []
  cur_row = 0
  table_data = []
  for k, v in EUFY_COLUMN_CONVERSIONS.items():
    if v is not None:
      table_data.append((k, v))
  while True:
    console.clear()
    table = generate_column_table(table_data, selected_rows, cur_row)
    console.print(table)
    console.print("Use up/down keys and space bar to select columns, press enter to continue")
    key = getkey()
    match key:
      case keys.UP:
        if cur_row == 0:
          pass
        else:
          cur_row -= 1
      case keys.DOWN:
        if cur_row == (table.row_count - 1):
          pass
        else:
          cur_row += 1
      case keys.SPACE:
        if cur_row in selected_rows:
          selected_rows = [x for x in selected_rows if x != cur_row]
        else:
          selected_rows.append(cur_row)
      case keys.ENTER:
        return [table_data[x][0] for x in selected_rows]
      case _:
        pass


def generate_date_table(table_data: list[datetime.datetime],
                        start_time: datetime.datetime,
                        end_time: datetime.datetime,
                        cur_row=None) -> Table:
  """
  Generate a table of dates for display

  :param table_data: table data to render
  :param start_time: start date of selected range
  :param end_time: end date of selected range
  :param cur_row: current row
  :return: table to be shown
  """
  cur_row_style = Style(color="black", bgcolor="cornsilk1")
  selected_row_style = Style(color="black", bgcolor="gold1")
  table_data.sort()
  table = Table(show_header=True, header_style="bold magenta")
  table.add_column("Selected", width=2, max_width=2)
  table.add_column("Date")
  row = 0
  if cur_row is None:
    cur_row = 0
  for entry in table_data:
    select_col_char = ""
    if row == cur_row:
      table.add_row(select_col_char,
                    entry.strftime("%Y-%m-%d %H:%M:%S"),
                    style=cur_row_style)
    elif start_time <= entry <= end_time:
      select_col_char = rich.emoji.Emoji("x")
      table.add_row(select_col_char,
                    entry.strftime("%Y-%m-%d %H:%M:%S"),
                    style=selected_row_style)
    else:
      table.add_row(select_col_char, entry.strftime("%Y-%m-%d %H:%M:%S"))
    row += 1
  return table


def select_dates(entries: list[WeightEntry]) -> tuple[datetime.date, datetime.date]:
  """
  Prompt users to select a range of dates from entries

  :param entries: list of entries from eufy export
  :return: a start and end date
  """
  dates = [x.time for x in entries]

  start_time = min(dates)
  end_time = max(dates)
  console = Console()
  cur_row = 0
  while True:
    console.clear()
    date_table = generate_date_table(dates, start_time=start_time, end_time=end_time, cur_row=cur_row)
    console.print(date_table)
    console.print("Use up/down keys to navigate")
    console.print("Use s to indicate the start of export range, e to indicate the end")
    console.print("Press enter to continue")
    key = getkey()
    match key:
      case keys.UP:
        if cur_row == 0:
          pass
        else:
          cur_row -= 1
      case keys.DOWN:
        if cur_row == (date_table.row_count - 1):
          pass
        else:
          cur_row += 1
      case "s":
        start_time = dates[cur_row]
      case "e":
        end_time = dates[cur_row]
      case keys.ENTER:
        return start_time, end_time
      case _:
        pass


def export_entries(filename: str, entries: list[WeightEntry], export_fields: list[str]) -> bool:
  """
  Export entries from Eufy export

  :param filename: name of file to write to
  :param entries: entries to write
  :param export_fields: list of fields to export
  :return: True on success, False on failure
  """
  with open(filename, "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(export_fields)
    for entry in entries:
      row = []
      for field in export_fields:
        print(EUFY_COLUMN_CONVERSIONS[field])
        match EUFY_COLUMN_CONVERSIONS[field]:
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
            row.append(entry.bmr)
          case "bone_mass":
            row.append(entry.bone_mass)
          case (
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
      print(row)
      csv_writer.writerow(row)
  return True


@click.command()
@click.option('--filename', help="File with data to import", required=True)
def interactive_export(filename: str = None) -> None:
  """
  Interactively export data to a Garmin compatible csv file

  :param filename: string with name of file to open
  :return: None
  """
  if filename is None:
    sys.exit("Filename not specified, exiting\n")
  if not os.path.exists(filename):
    sys.exit("File does not exist, exiting\n")
  entries = read_eufyfile(filename)
  columns = select_columns()
  start_time, end_time = select_dates(entries)
  filtered_entries = []
  for entry in entries:
    if start_time <= entry.time <= end_time:
      filtered_entries.append(entry)
  filtered_entries.sort(key=lambda x: x.time)
  write_garmin_file("exported.fit", filtered_entries, columns)


@click.command()
@click.option('--filename', help="File with data to import", required=True)
@click.option('--output', help="File with data to import", required=True)
@click.option('--start', help="Start date in YYYY-MM-DD format", required=False)
@click.option('--end', help="End date in YYYY-MM-DD format", required=False)
def batch_export(filename: str, output: str, start, end, export_fields: list[str]) -> None:
  """
  Export data to csv file that Garmin Connect can import

  :param filename: string with name of file to open
  :param output: string with name of file to export to
  :param start: start date in YYYY-MM-DD format
  :param end: end date in YYYY-MM-DD format
  :param export_fields: optional list of fields to export
  :return: None
  """
  if filename is None:
    sys.exit("Filename not specified, exiting\n")
  if not os.path.exists(filename):
    sys.exit("File does not exist, exiting\n")
  entries = read_eufyfile(filename)



def main() -> None:
  if len(sys.argv) == 3:
    interactive_export()
  elif len(sys.argv) > 3:
    batch_export()
  else:
    print("Need to provide more arguments")
    sys.exit(1)


if __name__ == "__main__":
  main()