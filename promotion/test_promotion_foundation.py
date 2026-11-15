import unittest
from decimal import Decimal

from campaign_policy import evaluate_campaign_start
from public_post_link import parse_public_post_link


class PublicPostLinkTests(unittest.TestCase):
    def test_standard_public_link(self):
        parsed = parse_public_post_link("https://t.me/example_channel/123")
        self.assertEqual(parsed.username, "example_channel")
        self.assertEqual(parsed.message_id, 123)
        self.assertEqual(parsed.canonical_url, "https://t.me/example_channel/123")

    def test_preview_link(self):
        parsed = parse_public_post_link("https://t.me/s/example_channel/456?single")
        self.assertEqual(parsed.username, "example_channel")
        self.assertEqual(parsed.message_id, 456)
        self.assertEqual(parsed.canonical_url, "https://t.me/example_channel/456")

    def test_missing_scheme_is_normalized(self):
        parsed = parse_public_post_link("t.me/example_channel/123")
        self.assertEqual(parsed.message_id, 123)

    def test_private_link_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_public_post_link("https://t.me/c/123456/7")

    def test_non_telegram_host_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_public_post_link("https://example.com/example_channel/123")


class CampaignPolicyTests(unittest.TestCase):
    def test_campaign_needs_every_gate(self):
        decision = evaluate_campaign_start(
            channel_consent_verified=True,
            post_link_valid=True,
            approved_partner_placements=2,
            available_budget_usd=Decimal("15.00"),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "eligible")

    def test_campaign_fails_closed_without_partner_inventory(self):
        decision = evaluate_campaign_start(
            channel_consent_verified=True,
            post_link_valid=True,
            approved_partner_placements=0,
            available_budget_usd=Decimal("15.00"),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "no_approved_partner_inventory")

    def test_campaign_fails_closed_when_budget_is_empty(self):
        decision = evaluate_campaign_start(
            channel_consent_verified=True,
            post_link_valid=True,
            approved_partner_placements=1,
            available_budget_usd=Decimal("0"),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "central_budget_exhausted")


if __name__ == "__main__":
    unittest.main()
