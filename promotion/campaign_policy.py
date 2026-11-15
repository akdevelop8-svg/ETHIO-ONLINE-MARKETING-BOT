"""Safety and budget gates for the promotion dispatcher."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

DEFAULT_TARGET_VIEWS = 15_000
DEFAULT_WINDOW_SECONDS = 3_600
DEFAULT_PILOT_CAP_USD = Decimal("15.00")


@dataclass(frozen=True)
class CampaignDecision:
    allowed: bool
    reason: str


def evaluate_campaign_start(
    *,
    channel_consent_verified: bool,
    post_link_valid: bool,
    approved_partner_placements: int,
    available_budget_usd: Decimal | str | float,
) -> CampaignDecision:
    """Fail closed: no consent, no valid post, no inventory, or no budget = no launch."""
    if not channel_consent_verified:
        return CampaignDecision(False, "channel_consent_not_verified")
    if not post_link_valid:
        return CampaignDecision(False, "public_post_link_invalid")
    if approved_partner_placements < 1:
        return CampaignDecision(False, "no_approved_partner_inventory")
    try:
        available = Decimal(str(available_budget_usd))
    except (InvalidOperation, ValueError):
        return CampaignDecision(False, "budget_value_invalid")
    if available <= Decimal("0"):
        return CampaignDecision(False, "central_budget_exhausted")
    return CampaignDecision(True, "eligible")
