import dataiku
from dataiku.customrecipe import (
    get_input_names_for_role,
    get_output_names_for_role,
    get_recipe_config,
)

from date_range_common import get_date_range, get_output_names


config = get_recipe_config()
start_name, end_name = get_output_names(config, "column")
start_date, end_date = get_date_range(config)
input_names = get_input_names_for_role("input_dataset")
output_names = get_output_names_for_role("output_dataset")
if len(input_names) > 1 or len(output_names) != 1:
    raise ValueError("Select at most one input dataset and exactly one output dataset.")

output_dataset = dataiku.Dataset(output_names[0])
input_dataset = dataiku.Dataset(input_names[0]) if input_names else None
schema = []
if input_dataset is not None:
    if input_dataset.full_name == output_dataset.full_name:
        raise ValueError("Input and output datasets must be different.")
    schema = list(input_dataset.read_schema())
    existing_names = {column["name"] for column in schema}
    collisions = existing_names.intersection((start_name, end_name))
    if collisions:
        raise ValueError(
            "Choose new date column names; input already contains: {}".format(
                ", ".join(sorted(collisions))
            )
        )

schema.extend([
    {"name": start_name, "type": "string"},
    {"name": end_name, "type": "string"},
])
output_dataset.write_schema(schema)
date_values = {start_name: start_date, end_name: end_date}
with output_dataset.get_writer() as writer:
    if input_dataset is None:
        writer.write_row_dict(date_values)
    else:
        for input_row in input_dataset.iter_rows():
            output_row = dict(input_row.items())
            output_row.update(date_values)
            writer.write_row_dict(output_row)
