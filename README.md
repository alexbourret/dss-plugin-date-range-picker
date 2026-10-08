# Date Range

A Dataiku DSS plugin with a **Generate date range** recipe and a **Set date range variables** macro.

## Recipe

Create a recipe from the plugin menu and select an output dataset.

- With no input, the output contains one row with `start_date` and `end_date`.
- With an input dataset, the output contains every input row and column plus the same date range on each row. An empty input produces an empty output with the extended schema.
- Change **Start column name** and **End column name** to customize the column names.
- The input dataset remains unchanged. Choose a separate output dataset. Names that already exist in the input are rejected before writing.

## Macro

In your project's **Macros** menu, run **Set date range variables**. It recalculates the range each time and sets the standard project variables `start_date` and `end_date`. Customize them with **Start variable name** and **End variable name**.

Existing values of the selected variables are replaced; other standard and local variables are preserved. The user running the macro needs permission to write the project configuration. To refresh the variables automatically, add this macro to a scenario.

## Date ranges

The default is **Today**. Relative ranges use the DSS server's local date at execution time.

| Range | Start | End |
| --- | --- | --- |
| Today | Today | Today |
| Yesterday | Yesterday | Yesterday |
| Last 7 / 14 / 30 / 60 days | N days before today | Yesterday |
| Last work week | Previous calendar week's Monday | Previous calendar week's Friday |
| Last week | Previous calendar week's Monday | Previous calendar week's Sunday |
| Last month | Previous calendar month's first day | Previous calendar month's last day |
| Last quarter | Previous calendar quarter's first day | Previous calendar quarter's last day |
| Last year | January 1 of the previous year | December 31 of the previous year |

Relative starts use `00:00:00.000` and ends use `23:59:00.000`. Rolling ranges exclude today. Weeks begin on Monday.

**Custom** uses DSS date pickers. **Custom (manual)** accepts timestamps such as `2026-10-01T00:00:00.000Z`. Custom timestamps preserve their supplied time and are normalized to milliseconds.

## Installation

Import this folder as a development plugin, or run `make package` and upload `dist/dss-plugin-date-range-0.0.1.zip` through DSS's plugin administration.

The plugin uses Python 3 and the DSS-provided `dataiku` package, with no additional dependencies required.

## References

- [DSS plugin recipes](https://doc.dataiku.com/dss/latest/plugins/reference/recipes.html)
- [DSS plugin macros](https://doc.dataiku.com/dss/latest/plugins/reference/macros.html)
