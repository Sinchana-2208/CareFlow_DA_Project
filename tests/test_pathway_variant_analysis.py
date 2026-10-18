import unittest

import pandas as pd

from src.pathway_variant_analysis import (
    reconstruct_case_sequences,
    summarize_pathway_variants,
)


class TestPathwayVariantAnalysis(unittest.TestCase):

    def setUp(self):
        self.events = pd.DataFrame([
            {
                "case_id": "A",
                "activity": "CRP",
                "timestamp": "2026-01-02 10:00:00",
            },
            {
                "case_id": "A",
                "activity": "Admission NC",
                "timestamp": "2026-01-01 08:00:00",
            },
            {
                "case_id": "B",
                "activity": "Admission NC",
                "timestamp": "2026-01-01 09:00:00",
            },
            {
                "case_id": "B",
                "activity": "CRP",
                "timestamp": "2026-01-02 11:00:00",
            },
            {
                "case_id": "C",
                "activity": "Admission NC",
                "timestamp": "2026-01-01 07:00:00",
            },
            {
                "case_id": "C",
                "activity": "Leucocytes",
                "timestamp": "2026-01-03 12:00:00",
            },
        ])

    def test_reconstructs_sequences_in_timestamp_order(self):
        sequences = reconstruct_case_sequences(self.events)

        case_a = sequences.loc[
            sequences["case_id"] == "A",
            "pathway_variant",
        ].iloc[0]

        self.assertEqual(case_a, "Admission NC -> CRP")

    def test_identifies_matching_pathway_variants(self):
        sequences = reconstruct_case_sequences(self.events)
        summary = summarize_pathway_variants(sequences)

        matching_variant = summary.loc[
            summary["pathway_variant"] == "Admission NC -> CRP"
        ].iloc[0]

        self.assertEqual(matching_variant["case_count"], 2)
        self.assertEqual(
            matching_variant["percentage_of_cases"],
            66.67,
        )

    def test_variant_percentages_total_100(self):
        sequences = reconstruct_case_sequences(self.events)
        summary = summarize_pathway_variants(sequences)

        self.assertAlmostEqual(
            summary["percentage_of_cases"].sum(),
            100.0,
            places=2,
        )

    def test_most_common_variant_is_ranked_first(self):
        sequences = reconstruct_case_sequences(self.events)
        summary = summarize_pathway_variants(sequences)

        self.assertEqual(summary.iloc[0]["variant_id"], "PV001")
        self.assertEqual(summary.iloc[0]["case_count"], 2)

    def test_empty_input_returns_empty_summary(self):
        empty_sequences = pd.DataFrame(
            columns=[
                "case_id",
                "pathway_variant",
                "activity_count",
            ]
        )

        summary = summarize_pathway_variants(empty_sequences)

        self.assertTrue(summary.empty)


if __name__ == "__main__":
    unittest.main()