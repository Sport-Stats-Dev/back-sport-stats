import argparse
import openpyxl

from apps.model.exercise import SharedExercise
from apps.shared import db


def get_translation_line(is_name, is_fr):
    print("get_translation_line"
        + f" is_name={is_name}"
        + f" is_fr={is_fr}")
    workbook = openpyxl.load_workbook('app/apps/utils/shared_exercises_data.xlsx')
    worksheet = workbook.active
    if is_name:
        result = "    \"exercise_name\": \"{name, select,"
        if is_fr:
            col_number = 1
        else:
            col_number = 3
    else:
        result = "    \"exercise_description\": \"{description, select,"
        if is_fr:
            col_number = 2
        else:
            col_number = 4

    line_number = 0

    for row in worksheet.iter_rows():
        if line_number != 0:
            result += f" {str(row[0].value)}{{{str(row[col_number].value)}}}"
        line_number += 1

    workbook.close()
    result += " other{} }\",\n"

    with open('apps/utils/result.txt', 'w') as file:
        file.write(result)

def fill_database():
    print("fill_database")
    workbook = openpyxl.load_workbook('app/apps/utils/shared_exercises_data.xlsx')
    worksheet = workbook.active
    line_number = 0
    modified = 0
    created = 0
    for row in worksheet.iter_rows():
        print(line_number)
        print(row[0].value)
        print(row[1].value)
        print(row[2].value)
        print(row[3].value)
        print(row[4].value)
        print(row[5].value)
        if line_number != 0:
            exercise = SharedExercise.query.filter_by(name=row[0].value).first()
            if exercise is not None:
                exercise.image = row[5].value
                exercise.video = row[6].value
            else:
                new_exercise = SharedExercise(
                    name=row[0].value,
                    description="",
                    image=row[5].value,
                    video=row[6].value
                )
                db.session.add(new_exercise)
        line_number += 1
    workbook.close()
    db.session.commit()
    print(f"modified={modified} created={created}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exécute une fonction spécifique.")
    parser.add_argument(
        "--fonction",
        choices=["get_translation_line", "fill_database"],
        required=True,
        help="Nom de la fonction à exécuter."
    )
    parser.add_argument(
        "--is_name",
        choices=[True, False],
        default=True,
        required=False,
        help="Nom de la fonction à exécuter."
    )
    parser.add_argument(
        "--is_fr",
        choices=[True, False],
        default=True,
        required=False,
        help="Nom de la fonction à exécuter."
    )

    args = parser.parse_args()

    if args.fonction == "get_translation_line":
        get_translation_line(args.is_name, args.is_fr)
    elif args.fonction == "fill_database":
        fill_database()
