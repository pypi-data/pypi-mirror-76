from inforion.logger.logger import get_logger

logger = get_logger("transform_special", True)


special_sheets = ["Artikel-Lagerort"]


def handle_special_pre_transformations(sheet_to_df_map, mainsheet, data):
    """This functions handles all specical transformation scenarios."""
    if (
        mainsheet == "Artikel-Lagerort"
        and "SUWH" in sheet_to_df_map
        and "ITTY" in sheet_to_df_map
    ):
        suwh_df = get_suwh_dataframe(sheet_to_df_map)
        try:
            mergedframe = data.merge(suwh_df, on="ItemType", how="inner")
        except Exception as ex:
            raise Exception(
                "Error doing special transformation for {0}.".format(mainsheet)
            )
        return mergedframe


def get_suwh_dataframe(sheet_to_df_map):

    df_itty = get_dataframe_from_sheet(sheet_to_df_map, "ITTY", 4, 8)
    df_itty = rename_columns(df_itty, ["ItemType", "M3ITTY", "M3SALE", "M3SPUC"])

    df_suwh = get_dataframe_from_sheet(sheet_to_df_map, "SUWH", 5, 8)
    df_suwh = rename_columns(
        df_suwh, ["M3ITTY", "M3WHLO", "M3SUWH", "M3PUIT", "M3ORTY"]
    )

    df_merged = df_itty.merge(df_suwh, on="M3ITTY")

    return df_merged


def get_dataframe_from_sheet(sheet_to_df_map, sheet_name, column_count=-1, row_skip=0):
    df = sheet_to_df_map[sheet_name][row_skip:]
    if column_count > 1:
        df = df.drop(df.columns[column_count:], axis=1)
    return df


def rename_columns(df, column_names):
    cloumns1 = {}
    for index, col in enumerate(column_names):
        cloumns1[df.columns[index]] = col
    df.rename(columns=cloumns1, inplace=True)
    return df
