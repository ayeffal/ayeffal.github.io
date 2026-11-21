import copy
import datetime
import os
import tempfile
import unittest

import yaml

import export_schema as es

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "design", "site-export.sample.yaml")


def sample():
    with open(SAMPLE, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def item(uid):
    return next(i for i in sample()["items"] if i["uid"] == uid)


PREPRINT = "r-5pkjdm6o"   # preprint of a paper under review
PAPER = "r-ecq6f4h2"      # published, free copy, date_precision month
TALK = "r-o5icf221"
POSTER = "r-nklswcel"     # date_precision year


class Sample(unittest.TestCase):
    def test_sample_is_valid(self):
        self.assertEqual(es.validate_export(sample()), [])

    def test_load_export_returns_items(self):
        self.assertEqual(len(es.load_export(SAMPLE)), 5)

    def test_empty_export_is_valid(self):
        self.assertEqual(es.validate_export({"schema_version": 1, "items": []}), [])


class Envelope(unittest.TestCase):
    def test_other_schema_versions_fail(self):
        for v in (0, 2, "1", 1.5, True, None):
            d = sample()
            d["schema_version"] = v
            self.assertTrue(es.validate_export(d), v)

    def test_missing_schema_version_fails(self):
        d = sample()
        del d["schema_version"]
        self.assertTrue(es.validate_export(d))

    def test_unknown_top_level_key_fails(self):
        d = sample()
        d["extra"] = 1
        self.assertTrue(es.validate_export(d))

    def test_items_must_be_a_list(self):
        for v in (None, {}, "x"):
            self.assertTrue(es.validate_export({"schema_version": 1, "items": v}))
        self.assertTrue(es.validate_export({"schema_version": 1}))

    def test_not_a_mapping(self):
        self.assertTrue(es.validate_export([]))
        self.assertTrue(es.validate_export(None))

    def test_duplicate_uid_fails(self):
        d = sample()
        d["items"].append(copy.deepcopy(d["items"][0]))
        self.assertTrue(any("duplicate" in e for e in es.validate_export(d)))


class Items(unittest.TestCase):
    def bad(self, uid, mutate):
        d = {"schema_version": 1, "items": [item(uid)]}
        mutate(d["items"][0])
        errors = es.validate_export(d)
        self.assertTrue(errors, "expected an error")
        return errors

    def test_unknown_field_fails(self):
        self.bad(PAPER, lambda i: i.update(evidence="x"))
        self.bad(TALK, lambda i: i.update(site="public"))

    def test_publication_fields_not_allowed_on_communication(self):
        self.bad(TALK, lambda i: i.update(doi="10.1/x"))

    def test_communication_fields_not_allowed_on_publication(self):
        self.bad(PAPER, lambda i: i.update(meeting="m"))

    def test_missing_required_field_fails(self):
        for uid, fields in [
            (PAPER, ["uid", "title", "date", "authors", "pub_type", "pub_status", "venue"]),
            (TALK, ["meeting", "format"]),
            (PREPRINT, ["preprint_url"]),
        ]:
            for f in fields:
                with self.subTest(uid=uid, field=f):
                    self.bad(uid, lambda i, f=f: i.pop(f))

    def test_type_unknown_or_missing(self):
        self.bad(PAPER, lambda i: i.update(type="course"))
        self.bad(PAPER, lambda i: i.pop("type"))

    def test_unknown_enum_values_fail(self):
        for uid, f, v in [
            (PAPER, "pub_type", "thesis"),
            (PAPER, "pub_status", "submitted"),
            (PAPER, "pub_status", "in-preparation"),
            (PAPER, "article_kind", "letter"),
            (PAPER, "open_copy_kind", "pdf"),
            (PAPER, "date_precision", "day"),
            (TALK, "format", "keynote"),
        ]:
            with self.subTest(f=f, v=v):
                self.bad(uid, lambda i, f=f, v=v: i.update({f: v}))

    def test_in_press_is_valid(self):
        d = {"schema_version": 1, "items": [item(PAPER)]}
        d["items"][0]["pub_status"] = "in-press"
        self.assertEqual(es.validate_export(d), [])

    def test_blank_or_null_values_fail(self):
        self.bad(PAPER, lambda i: i.update(doi=""))
        self.bad(PAPER, lambda i: i.update(doi=None))
        self.bad(PAPER, lambda i: i.update(authors=[]))

    def test_non_string_values_fail(self):
        self.bad(PAPER, lambda i: i.update(pages=1234))        # unquoted number
        self.bad(PAPER, lambda i: i.update(date=datetime.date(2024, 5, 31)))  # unquoted date

    def test_bad_uid_fails(self):
        for v in ("r-ABCDEFGH", "r-abc", "x-abcdefgh", "r-abcdefghi"):
            self.bad(PAPER, lambda i, v=v: i.update(uid=v))

    def test_bad_dates_fail(self):
        for v in ("2024-13-01", "2024-5-31", "31/05/2024", "2024-02-30"):
            self.bad(PAPER, lambda i, v=v: i.update(date=v))

    def test_date_precision_needs_last_day(self):
        self.bad(PAPER, lambda i: i.update(date="2024-05-30"))       # month
        self.bad(POSTER, lambda i: i.update(date="2023-12-30"))      # year
        d = {"schema_version": 1, "items": [item(PAPER)]}
        d["items"][0].update(date="2024-02-29")                      # leap year
        self.assertEqual(es.validate_export(d), [])

    def test_urls_must_be_http(self):
        self.bad(PREPRINT, lambda i: i.update(preprint_url="javascript:alert(1)"))
        self.bad(PAPER, lambda i: i.update(open_copy_url="ftp://x/y"))
        self.bad(POSTER, lambda i: i.update(url="example.org/a"))

    def test_doi_must_be_bare(self):
        self.bad(PAPER, lambda i: i.update(doi="https://doi.org/10.0000/fake.1"))
        self.bad(PAPER, lambda i: i.update(doi="doi:10.0000/fake.1"))

    def test_preprint_hides_venue_details(self):
        for f, v in [("venue", "J"), ("doi", "10.1/x"), ("volume", "1"), ("pages", "1-2"),
                     ("open_copy_url", "https://x.org/a"), ("open_copy_kind", "preprint")]:
            with self.subTest(f=f):
                self.bad(PREPRINT, lambda i, f=f, v=v: i.update({f: v}))

    def test_venue_required_unless_preprint(self):
        self.bad(PAPER, lambda i: i.pop("venue"))

    def test_preprint_url_only_on_preprint(self):
        self.bad(PAPER, lambda i: i.update(preprint_url="https://x.org/p"))

    def test_open_copy_fields_go_together(self):
        self.bad(PAPER, lambda i: i.pop("open_copy_kind"))
        self.bad(PAPER, lambda i: i.pop("open_copy_url"))

    def test_article_kind_required_for_articles_only(self):
        self.bad(PAPER, lambda i: i.pop("article_kind"))
        self.bad(PREPRINT, lambda i: i.pop("article_kind"))
        self.bad(PAPER, lambda i: i.update(pub_type="chapter"))   # keeps article_kind
        d = {"schema_version": 1, "items": [item(PAPER)]}
        d["items"][0].update(pub_type="book")
        del d["items"][0]["article_kind"]
        self.assertEqual(es.validate_export(d), [])

    def test_published_preprint_keeps_uid_and_validates(self):
        before = item(PREPRINT)
        after = dict(before, pub_status="published", venue="Fake Journal",
                     doi="10.0000/fake.2", date="2026-03-01")
        del after["preprint_url"]
        d = {"schema_version": 1, "items": [after]}
        self.assertEqual(es.validate_export(d), [])
        self.assertEqual(after["uid"], before["uid"])

    def test_volume_with_issue_and_article_number_pages_are_valid(self):
        d = {"schema_version": 1, "items": [item(PAPER)]}
        d["items"][0].update(volume="24(6)", pages="e3003861")
        self.assertEqual(es.validate_export(d), [])


class Reporting(unittest.TestCase):
    def test_errors_never_contain_values(self):
        d = sample()
        d["items"][3]["pub_type"] = "SECRET-VALUE"
        d["items"][3]["evidence"] = "SECRET-VALUE"
        d["items"][3]["date"] = "SECRET-VALUE"
        text = "\n".join(es.validate_export(d))
        self.assertTrue(text)
        for it in sample()["items"]:
            self.assertNotIn(it["title"], text)
        self.assertNotIn("SECRET-VALUE", text)

    def test_load_export_raises_on_invalid_file(self):
        d = sample()
        d["schema_version"] = 2
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "x.yaml")
            with open(p, "w", encoding="utf-8") as fh:
                yaml.safe_dump(d, fh)
            with self.assertRaises(es.ExportError):
                es.load_export(p)


if __name__ == "__main__":
    unittest.main()
