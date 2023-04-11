import pytest

import eng_m


def test_positive_asset_disposal() -> None:
    """
    You have a class 6 depreciable asset worth $5,000 with salvage value $500
    at end of year 4. What are your tax credits (debits) on asset disposal at
    30% marginal tax rate?
    """
    depreciable = eng_m.Depreciable(5000, 500, 4, cca=6, depreciation_class=True)
    assert depreciable.disposal_tax_effect(0.3) == pytest.approx(888.82, abs=0.01)


def test_negative_asset_disposal() -> None:
    """
    You have a class 50 depreciable asset worth $5,000 with salvage value $900
    at the end of year 6. What are your tax credits (debits) on asset disposal
    at 70% marginal tax rate?
    """
    depreciable = eng_m.Depreciable(5000, 900, 6, cca=50, depreciation_class=True)
    assert depreciable.disposal_tax_effect(0.7) == pytest.approx(-583.18, abs=0.01)


def test_capital_gain_asset_disposal() -> None:
    """
    You have an asset depreciating at 20% per year, purchased for $5,000 and
    sold for $6,000 2 years later. What are your tax credits (debits) on asset
    disposal at 20% marginal tax rate?
    """
    depreciable = eng_m.Depreciable(5000, 6000, 2, cca=0.2)
    assert depreciable.disposal_tax_effect(0.2) == pytest.approx(-380, abs=0.01)
