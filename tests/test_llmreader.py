"""Tests for LLMReader class and utilities."""

import pytest
from paperplumber.parsing import LLMReader


@pytest.mark.parametrize(
    "target, text, expected",
    [
        (
            "enthalpy of formation",
            """The enthalpy of formation of water is 25.53 kcal/mol"""
        ),
        (
            "folding rate constant",
            """Figure 5A shows the refolding trajectory for Arc-L1-Arc following a jump from 7.0 to 2.4 M urea (3.1 µM protein, 25 °C, pH 7.5, 250 mM KCl, PMT voltage). The data fit well to a single exponential with a refolding rate constant (k f ) of 240 s -1 . Greater than 95% of the expected change in amplitude is observed during the data collection phase (i.e., less than 5% of the expected amplitude change occurs in the dead time). In experiments performed at final urea concentrations of 2.0 and 2.8 M, k f was found to be independent of Arc-L1-Arc protein concentration from 1 to 10 µM (data not shown).""",
            "240 s-1"
        ),
        (
            "folding rate constant",
            """The refolding of FNIII is relatively fast. The re-folding kinetics are biphasic at low temperatures(Plaxco et al., 1996) with intrinsic rate constants of64(2) and 17(2) s ÿ1 at 5  C (Figure 4b). The rela-tive amplitudes of these phases are unaffected byGuHCl and remain at 70(3)% and 30(3)%, re-spectively. At higher temperatures the rates andamplitudes of the two phases become similar andat 25  C only a single folding phase can be distin-guished. The intrinsic refolding rate constant of10 FNIII under these conditions is 155(5) s ÿ(Figure 4b). The folding transition state energeticsof 10 FNIII at 25  C are relatively insensitive to thepresence of denaturant (m { f  0.91(0.03) kcalmol ÿ1 M ÿ1 ). The two refolding phases observed atlower temperatures exhibit effectively identicalGuHCl sensitivities (fast, m { f  0.84(0.02) kcalmol ÿ1 M ÿ1 ; slow, m { f  0.86(0.02) kcal mol ÿ1 M ÿ1 ),suggesting that the changes in solvent-exposed sur-face area upon formation of the transition states ofthe two processes are very similar (Pace, 1986;Chen et al., 1992). For 10 FNIII, y m is also 0.7, whichsuggests that its folding transition state may exhi-bit a similar degree of collapse.""",
            "155 s-1"
        ),
    ])
def test_llmreader(target, text, expected):
    assert LLMReader(target=target).process(text) == expected