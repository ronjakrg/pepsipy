# This logic is based on the implementation from
# PROTzilla (https://github.com/cschlaffner/PROTzilla/tree/dev/backend/protzilla/importing)
# and has been adapted to fit this project.

from pathlib import Path
import re
from enum import Enum

import pandas as pd


def import_peptide_txt(file, intensity_name: str = "Intensity") -> pd.DataFrame:
    """
    Converts a MaxQuant peptide.txt file into a pandas DataFrame.
        file: File object (e.g., uploaded file from Django) or path to the peptide.txt file.
        intensity_name: Name of the intensity column to extract. Default is "Intensity".
    """
    allowed = {item.value for item in IntensityType}
    if intensity_name not in allowed:
        raise ValueError(f"Unknown intensity name: {intensity_name}")

    if intensity_name in [IntensityType.LFQ_INTENSITY.value, IntensityType.IBAQ.value]:
        intensity_name = IntensityType.INTENSITY.value

    id_columns = [
        "Leading razor protein",
        "Sequence",
        "Missed cleavages",
        "PEP",
        "Charges",
    ]

    if hasattr(file, "read"):
        file.seek(0)
        df = pd.read_csv(
            file,
            sep="\t",
            low_memory=False,
            na_values=["", 0],
            keep_default_na=True,
        )

    if "Sample" not in df.columns:
        id_df = df[id_columns]
        disallowed_suffixes = r"(variability|count|type|peptides)"
        if intensity_name in (
            IntensityType.RATIO_HL.value,
            IntensityType.RATIO_LH.value,
        ):
            base_pattern = rf"^{re.escape(intensity_name)}\s(?!normalized\b)(?!.*\b{disallowed_suffixes}\b).*$"
        else:
            base_pattern = (
                rf"^{re.escape(intensity_name)}\s(?!.*\b{disallowed_suffixes}\b).*$"
            )

        intensity_df = df.filter(regex=base_pattern, axis=1)
        intensity_df.columns = [
            c[len(intensity_name) + 1 :] for c in intensity_df.columns
        ]
        molten = pd.melt(
            pd.concat([id_df, intensity_df], axis=1),
            id_vars=id_columns,
            var_name="Sample",
            value_name="Intensity",
        )

    else:
        final_df = df.rename(columns={"Proteins": "Protein ID"})
        ordered = final_df[
            [
                "Sample",
                "Protein ID",
                "Sequence",
                "Intensity",
                "PEP",
                "Charges",
            ]
        ]

    molten = molten.rename(columns={"Leading razor protein": "Protein ID"})
    ordered = molten[
        [
            "Sample",
            "Protein ID",
            "Sequence",
            "Intensity",
            "PEP",
            "Charges",
        ]
    ]
    ordered.dropna(subset=["Protein ID"], inplace=True)
    ordered.sort_values(by=["Sample", "Protein ID"], ignore_index=True, inplace=True)

    new_groups, filtered_proteins = clean_protein_groups(ordered["Protein ID"].tolist())
    cleaned = ordered.assign(**{"Protein ID": new_groups})

    return cleaned


def clean_protein_groups(protein_groups: list):
    regex = {
        "ensembl_peptide_id": re.compile(r"^ENSP\d{11}"),
        "refseq_peptide": re.compile(r"^NP_\d{6,}"),
        "refseq_peptide_predicted": re.compile(r"^XP_\d{9}"),
    }
    uniprot_regex = re.compile(
        r"""^[A-Z]               # start with capital letter
        [A-Z\d]{5}([A-Z\d]{4})?  # match ids of length 6 or 10
        ([-_][-\d]+)?            # match variations like -8 and _9-6
        """,
        re.VERBOSE,
    )

    removed_protein_ids = []

    extracted_ids = {k: set() for k in regex.keys()}
    found_ids_per_group = []
    # go through all groups and find the valid proteins
    # non uniprot ids are put into extracted_ids, so they can be mapped
    for group in protein_groups:
        found_in_group = []
        for protein_id in group.split(";"):
            if not protein_id.startswith("ENSP") and (
                match := uniprot_regex.search(protein_id)
            ):
                found_in_group.append(match.group(0))
                continue
            for identifier, pattern in regex.items():
                if match := pattern.search(protein_id):
                    found_id = match.group(0)
                    extracted_ids[identifier].add(found_id)
                    found_in_group.append(found_id)
                    break  # can only match one regex
            else:
                removed_protein_ids.append(protein_id)
        found_ids_per_group.append(found_in_group)

    new_groups = []
    for group in found_ids_per_group:
        all_ids_of_group = []
        for old_id in group:
            if uniprot_regex.search(old_id):
                all_ids_of_group.append(old_id)
            # elif map_to_uniprot:
            # [ Removed ]
            else:
                all_ids_of_group.append(old_id)
        new_groups.append(all_ids_of_group[0] if all_ids_of_group else "")
    return new_groups, removed_protein_ids


class IntensityType(Enum):
    IBAQ = "iBAQ"
    INTENSITY = "Intensity"
    LFQ_INTENSITY = "LFQ intensity"
    RATIO_HL = "Ratio H/L"
    RATIO_LH = "Ratio L/H"
    RATIO_HL_NORMALIZED = "Ratio H/L normalized"
    RATIO_LH_NORMALIZED = "Ratio L/H normalized"
