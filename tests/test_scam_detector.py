# ==============================================================
# tests/test_scam_detector.py
# Unit tests for utils/scam_detector.py
#
# Run with:
#   cd CongressionalAppDistrict6
#   python -m pytest tests/ -v
# ==============================================================

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.scam_detector import analyze_message


# ── Helper ────────────────────────────────────────────────────────────────────
def verdict_label(result):
    """Return just the emoji-free verdict tier for easy assertions."""
    v = result["verdict"]
    if "Looks Safe" in v:
        return "safe"
    if "Slightly Suspicious" in v:
        return "slightly"
    if "Suspicious" in v:
        return "suspicious"
    if "Likely a Scam" in v:
        return "scam"
    if "No message" in v:
        return "empty"
    return "unknown"


# ── Empty / whitespace input ──────────────────────────────────────────────────
class TestEmptyInput:
    def test_empty_string(self):
        r = analyze_message("")
        assert r["error"] == "empty"
        assert r["score"] == 0
        assert verdict_label(r) == "empty"

    def test_whitespace_only(self):
        r = analyze_message("   \n\t  ")
        assert r["error"] == "empty"

    def test_none_like_blank(self):
        r = analyze_message("  ")
        assert r["error"] == "empty"


# ── Legitimate messages — should receive LOW risk scores (safe or slightly) ──
class TestLegitimateMessages:

    def test_normal_greeting(self):
        """Plain greeting with no money or scam language -> safe."""
        r = analyze_message("Hey! How are you doing today?")
        assert verdict_label(r) == "safe", \
            f"Normal greeting flagged: score={r['score']}, verdict={r['verdict']}"

    def test_school_lunch_reminder(self):
        """School reminder mentioning a dollar amount -> safe."""
        r = analyze_message(
            "Reminder: Tomorrow is Taco Tuesday! Lunch costs $3.50. "
            "Please bring exact change or load your cafeteria account online."
        )
        assert verdict_label(r) in ("safe", "slightly"), \
            f"School lunch reminder over-flagged: score={r['score']}, verdict={r['verdict']}, " \
            f"phrases={r['matched_phrases']}"

    def test_school_field_trip_fee(self):
        """School permission slip with a fee amount -> safe or slightly suspicious at most."""
        r = analyze_message(
            "Dear Parent, the 5th grade field trip to the science museum is on Nov 8. "
            "The permission slip and $12 fee are due by Oct 30. "
            "Please return the signed form to your child's teacher."
        )
        assert verdict_label(r) in ("safe", "slightly"), \
            f"Field trip notice over-flagged: score={r['score']}, verdict={r['verdict']}"

    def test_school_fundraiser_reminder(self):
        """School fundraiser mentioning a price -> safe."""
        r = analyze_message(
            "Don't forget: wrapping paper orders are due Friday. "
            "Each roll is $8.00. Checks payable to Lincoln Elementary PTA."
        )
        assert verdict_label(r) in ("safe", "slightly"), \
            f"School fundraiser over-flagged: score={r['score']}, verdict={r['verdict']}"

    def test_birthday_message(self):
        r = analyze_message("Congratulations on your birthday! Wishing you all the best.")
        assert r["score"] < 20, f"Birthday message over-flagged: score={r['score']}"

    def test_sports_win_message(self):
        r = analyze_message("Congratulations, the team won the championship last night!")
        assert r["score"] < 20, f"Sports message over-flagged: score={r['score']}"

    def test_amazon_product_review(self):
        """Mentioning Amazon in a shopping context -> not a scam."""
        r = analyze_message("I bought this on Amazon and it arrived in two days. Great product!")
        assert verdict_label(r) != "scam", \
            f"Amazon mention over-flagged: score={r['score']}"

    def test_microsoft_office_mention(self):
        r = analyze_message("I use Microsoft Office for work every day.")
        assert verdict_label(r) != "scam", \
            f"Microsoft mention over-flagged: score={r['score']}"

    def test_download_software_legitimate(self):
        r = analyze_message("You can download this free software from the official website.")
        assert verdict_label(r) != "scam", \
            f"Legitimate download mention over-flagged: score={r['score']}"

    def test_news_headline_amazon_river(self):
        """'Amazon' as a geographic name -> safe."""
        r = analyze_message(
            "Scientists discover a new species of butterfly in the Amazon rainforest."
        )
        assert verdict_label(r) == "safe", \
            f"Amazon river headline flagged: score={r['score']}, verdict={r['verdict']}"

    def test_normal_bill_reminder(self):
        """A billing statement mention (legitimate commerce) -> safe or slightly."""
        r = analyze_message(
            "Your monthly statement is ready. Your balance due is $45.00. "
            "Payment is due by the 15th. Log in at your bank's official website to pay."
        )
        assert verdict_label(r) in ("safe", "slightly"), \
            f"Normal bill over-flagged: score={r['score']}, verdict={r['verdict']}"

    def test_order_shipped_notification(self):
        """Shipping confirmation with order total -> safe or slightly."""
        r = analyze_message(
            "Your order #12345 has shipped! Tracking number: 9400111899223456789012. "
            "Estimated delivery: Oct 15. Order total: $32.99."
        )
        assert verdict_label(r) in ("safe", "slightly"), \
            f"Order shipped notice over-flagged: score={r['score']}, verdict={r['verdict']}"

    def test_ordinary_message_no_money(self):
        """Everyday message with no money or scam signals -> safe."""
        r = analyze_message(
            "Can you pick up some milk on your way home? Also, don't forget the dentist "
            "appointment on Thursday at 3 pm."
        )
        assert verdict_label(r) == "safe", \
            f"Ordinary message flagged: score={r['score']}, verdict={r['verdict']}"


# ── Suspicious messages — should receive MEDIUM risk scores ──────────────────
class TestSuspiciousMessages:

    def test_delivery_payment_link(self):
        """Delivery fee via suspicious link is suspicious."""
        r = analyze_message(
            "USPS: Your package could not be delivered. A $2.99 redelivery fee is required. "
            "Click here to pay: parcel-redelivery.com/pay"
        )
        assert verdict_label(r) in ("suspicious", "scam"), \
            f"Delivery payment link not flagged: score={r['score']}, verdict={r['verdict']}"

    def test_delivery_link_no_official_carrier(self):
        """Unknown sender + package + pay link -> suspicious."""
        r = analyze_message(
            "Your shipment is on hold. Pay the $3.50 customs fee now at pkg-release.com "
            "or your package will be returned."
        )
        assert verdict_label(r) in ("suspicious", "scam"), \
            f"Unknown delivery link not flagged: score={r['score']}, verdict={r['verdict']}"

    def test_statefarm_loan_100(self):
        """Context rule: impersonation + loan + money -- must flag."""
        r = analyze_message(
            "I am Jake from State Farm calling you regarding a loan for 100 dollars"
        )
        assert r["score"] > 0, f"State Farm loan 100 not flagged: score={r['score']}"
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"State Farm loan 100 verdict wrong: {r['verdict']}"

    def test_statefarm_loan_10(self):
        """Dollar amount should NOT matter -- context makes it suspicious."""
        r = analyze_message(
            "I am Jake from State Farm calling you regarding a loan for 10 dollars"
        )
        assert r["score"] > 0, f"State Farm loan 10 not flagged: score={r['score']}"
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"State Farm loan 10 verdict wrong: {r['verdict']}"

    def test_loan_10_vs_100_same_verdict(self):
        """Changing amount from $100 to $10 must NOT change the verdict tier."""
        r100 = analyze_message(
            "I am Jake from State Farm calling you regarding a loan for 100 dollars"
        )
        r10 = analyze_message(
            "I am Jake from State Farm calling you regarding a loan for 10 dollars"
        )
        assert verdict_label(r100) == verdict_label(r10), \
            f"Amount changed verdict: 100->{r100['verdict']} vs 10->{r10['verdict']}"

    def test_urgent_money_contact_context(self):
        r = analyze_message("You owe a payment, send money immediately by calling us now")
        assert r["score"] > 0, "Urgent money + contact combo not flagged"
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"Urgent money + contact combo not flagged at all: score={r['score']}"

    def test_single_wire_transfer_mention(self):
        """One strong phrase alone: suspicious but not necessarily 'scam'."""
        r = analyze_message("Please send a wire transfer for the invoice.")
        assert verdict_label(r) in ("slightly", "suspicious"), \
            f"Single strong flag: score={r['score']}, verdict={r['verdict']}"


# ── Obvious scams -- should receive HIGH risk scores (scam) ──────────────────
class TestObviousScams:

    def test_irs_scam(self):
        r = analyze_message(
            "URGENT: This is the IRS. Your Social Security Number has been suspended. "
            "Call back immediately or a warrant will be issued for your arrest."
        )
        assert verdict_label(r) == "scam", f"IRS scam not caught: score={r['score']}"

    def test_lottery_scam(self):
        r = analyze_message(
            "Congratulations you have won $1,000,000 in the National Lottery. "
            "Claim your prize by sending a processing fee via Western Union."
        )
        assert verdict_label(r) == "scam", f"Lottery scam not caught: score={r['score']}"

    def test_tech_support_scam(self):
        r = analyze_message(
            "Your computer is infected with a dangerous virus! "
            "Call Apple Support and allow remote access immediately."
        )
        assert verdict_label(r) == "scam", f"Tech support scam not caught: score={r['score']}"

    def test_gift_card_scam(self):
        r = analyze_message(
            "Your Amazon account has been suspended. Buy $200 in gift cards "
            "and reply with the codes. Act now -- expires today!"
        )
        assert verdict_label(r) == "scam", f"Gift card scam not caught: score={r['score']}"

    def test_inheritance_scam(self):
        r = analyze_message(
            "You have been selected to receive an inheritance of unclaimed funds. "
            "Please send a wire transfer to release the money."
        )
        assert verdict_label(r) == "scam", f"Inheritance scam not caught: score={r['score']}"

    def test_romance_scam_money(self):
        r = analyze_message(
            "I love you so much. I am stuck abroad and need you to send money via Western Union."
        )
        assert verdict_label(r) in ("suspicious", "scam"), \
            f"Romance scam not flagged: score={r['score']}"

    def test_fake_prize_claim_fee(self):
        """Fake prize + upfront fee = scam."""
        r = analyze_message(
            "You've been selected as our grand prize winner! "
            "To claim your reward, you must pay a $49.99 processing fee first. "
            "Reply with your credit card details."
        )
        assert verdict_label(r) == "scam", \
            f"Fake prize scam not caught: score={r['score']}, verdict={r['verdict']}"

    def test_urgent_gift_card_demand(self):
        """Urgent gift card payment request = obvious scam."""
        r = analyze_message(
            "This is the IRS. You owe back taxes. Purchase $500 in iTunes gift cards "
            "and call us back immediately with the card numbers to avoid arrest."
        )
        assert verdict_label(r) == "scam", \
            f"Urgent gift card scam not caught: score={r['score']}, verdict={r['verdict']}"

    def test_scammer_self_identification(self):
        r = analyze_message("I am scammer give 100")
        assert r["score"] > 0, "Scammer message scored 0"
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"Scammer message not flagged: score={r['score']}, verdict={r['verdict']}"
        assert any("scammer" in p for p in r["matched_phrases"]), \
            "Word 'scammer' not in matched_phrases"

    def test_give_dollar_amount(self):
        r = analyze_message("give me $500 now")
        assert r["score"] > 0, "Dollar demand not detected"

    def test_give_me_100_dollars(self):
        r = analyze_message("I am a monkey, give me 100 dollars")
        assert r["score"] > 0, f"'give me 100 dollars' not detected: score={r['score']}"
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"Not flagged: score={r['score']}, verdict={r['verdict']}"

    def test_send_me_money(self):
        r = analyze_message("Please send me money via Zelle right away.")
        assert r["score"] > 0
        assert any(p in r["matched_phrases"] for p in ["send me money", "zelle", "send money"])

    def test_cash_app_request(self):
        r = analyze_message("Send $200 to my Cash App account immediately.")
        assert r["score"] > 0

    def test_venmo_request(self):
        r = analyze_message("Can you Venmo me $50? I really need it urgently.")
        assert r["score"] > 0

    def test_ssn_request(self):
        r = analyze_message("Please confirm your identity by providing your Social Security Number.")
        assert r["score"] > 0
        assert any("social security number" in p for p in r["matched_phrases"])

    def test_password_request(self):
        r = analyze_message("Please verify your account by sending us your password.")
        assert r["score"] > 0

    def test_fake_tech_support_context(self):
        r = analyze_message(
            "There is a virus problem on your computer, call our support technician"
        )
        assert verdict_label(r) in ("slightly", "suspicious", "scam"), \
            f"Tech support context not flagged: score={r['score']}"

    def test_romance_money_context(self):
        r = analyze_message(
            "I love you and miss you so much, I need you to send money for emergency"
        )
        assert r["score"] > 0, "Romance + money context not flagged"


# ── Score calibration checks ─────────────────────────────────────────────────
class TestScoreCalibration:

    def test_single_mild_flag_not_scam(self):
        """One mild flag (weight 1) should NOT reach 'Likely a Scam'."""
        r = analyze_message("Click here to learn more about our service.")
        assert verdict_label(r) != "scam", \
            f"Single mild flag incorrectly labelled scam: score={r['score']}"

    def test_single_strong_flag_not_yet_scam(self):
        """One strong flag alone should be suspicious but NOT 'Likely a Scam'."""
        r = analyze_message("Please send a wire transfer for the invoice.")
        assert verdict_label(r) in ("slightly", "suspicious"), \
            f"Single strong flag: score={r['score']}, verdict={r['verdict']}"

    def test_four_strong_flags_is_scam(self):
        """Four strong flags should reach 'Likely a Scam'."""
        r = analyze_message(
            "You have won! Claim your prize. Send gift cards and provide your routing number."
        )
        assert verdict_label(r) == "scam", \
            f"Four strong flags not reaching scam: score={r['score']}"

    def test_score_capped_at_100(self):
        r = analyze_message(
            "You have won million dollars inheritance unclaimed funds wire transfer "
            "gift card bitcoin western union routing number social security number "
            "your account has been suspended remote access your computer is infected "
            "claim your prize advance fee warrant will be issued"
        )
        assert r["score"] <= 100, f"Score exceeded 100: {r['score']}"

    def test_score_is_integer(self):
        r = analyze_message("Send me money via Zelle now.")
        assert isinstance(r["score"], int)

    def test_legitimate_school_reminder_low_score(self):
        """School lunch reminder must score lower than a scam message."""
        school = analyze_message(
            "Reminder: Lunch is $3.50 tomorrow. Please bring change or top up your cafeteria account."
        )
        scam = analyze_message(
            "URGENT: You have won $3.50 million! Claim your prize by sending a processing fee."
        )
        assert school["score"] < scam["score"], \
            f"School reminder scored higher than scam: school={school['score']}, scam={scam['score']}"

    def test_obvious_scam_scores_higher_than_suspicious(self):
        """An obvious scam must score higher than a mildly suspicious message."""
        mild = analyze_message("There may be an issue with your account. Please verify.")
        obvious = analyze_message(
            "URGENT! This is the IRS. Your SSN has been suspended. A warrant will be issued. "
            "Buy $500 in gift cards and call us immediately."
        )
        assert obvious["score"] > mild["score"], \
            f"Obvious scam not higher than mild: obvious={obvious['score']}, mild={mild['score']}"


# ── Return-value shape ────────────────────────────────────────────────────────
class TestReturnShape:

    def test_all_keys_present_normal(self):
        r = analyze_message("Hello there!")
        for key in ("score", "verdict", "color", "reasons", "matched_phrases", "error"):
            assert key in r, f"Missing key: {key}"

    def test_all_keys_present_empty(self):
        r = analyze_message("")
        for key in ("score", "verdict", "color", "reasons", "matched_phrases", "error"):
            assert key in r, f"Missing key: {key}"

    def test_reasons_and_phrases_same_length(self):
        r = analyze_message(
            "Congratulations you have won! Claim your prize via wire transfer."
        )
        assert len(r["reasons"]) == len(r["matched_phrases"]), \
            f"Mismatch: {len(r['reasons'])} reasons vs {len(r['matched_phrases'])} phrases"

    def test_no_duplicate_phrases(self):
        """Each phrase should only be counted once even if it appears twice."""
        r = analyze_message("gift card gift card gift card")
        assert r["matched_phrases"].count("gift card") == 1, \
            "Duplicate phrase counted multiple times"

    def test_error_none_for_valid_message(self):
        r = analyze_message("Hello, how are you?")
        assert r["error"] is None

    def test_color_matches_verdict_safe(self):
        r = analyze_message("Hello there")
        assert r["color"] == "success", \
            f"Expected success color for safe message, got {r['color']}: score={r['score']}"

    def test_color_matches_verdict_scam(self):
        r = analyze_message(
            "You have won million dollars! Claim your prize. Send gift cards and "
            "provide your routing number. Warrant will be issued if you don't act now."
        )
        assert r["color"] == "error", \
            f"Expected error color for scam message, got {r['color']}: score={r['score']}"
