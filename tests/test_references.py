import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("references", ROOT / "scripts/build-references.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class ReferenceTests(unittest.TestCase):
    def fixture(self, root):
        image = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
        image += (390).to_bytes(4, "big") + (844).to_bytes(4, "big")
        (root / "dashboard-390.png").write_bytes(image)
        manifest = {
            "schemaVersion": 1,
            "source": {"mode": "live-public-demo", "authenticated": False, "commitSha": "a" * 40,
                       "origin": "https://example.test"},
            "capturedAt": "2026-10-29T18:00:00Z",
            "verifiedAt": "2026-10-29T18:01:00Z",
            "viewports": [{"width": 390, "height": 844}],
            "screens": [{"id": "dashboard-390", "screen": "dashboard", "title": "Dashboard",
                         "file": "dashboard-390.png", "path": "/demo/app",
                         "width": 390, "height": 844,
                         "sha256": hashlib.sha256(image).hexdigest(),
                         "pageOverflow": False}],
        }
        return manifest

    def test_hash_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest["screens"][0]["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "hash"):
                builder.validate(root, manifest)

    def test_dimensions_must_match_image_header(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest["screens"][0]["width"] = 1440
            with self.assertRaisesRegex(ValueError, "dimensions"):
                builder.validate(root, manifest)

    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest["screens"][0]["file"] = "../private.png"
            with self.assertRaisesRegex(ValueError, "filename"):
                builder.validate(root, manifest)

    def test_authenticated_capture_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest["source"]["authenticated"] = True
            with self.assertRaisesRegex(ValueError, "public demo"):
                builder.validate(root, manifest)

    def test_duplicate_and_missing_viewport_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest["screens"].append(dict(manifest["screens"][0]))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                builder.validate(root, manifest)
            manifest["screens"].pop()
            manifest["viewports"].append({"width": 768, "height": 1024})
            with self.assertRaisesRegex(ValueError, "viewport"):
                builder.validate(root, manifest)

    def test_committed_capture_set_is_consistent(self):
        manifests = list((ROOT / "references/ship-a-skill").glob("*/manifest.json"))
        self.assertTrue(manifests, "Missing completed reference capture")
        for file in manifests:
            builder.validate(file.parent, json.loads(file.read_text()))

    def test_library_font_families_match_observed_application(self):
        source = (ROOT / "DESIGN.md").read_text().split("---", 2)[1]
        tokens = json.loads(source)["tokens"]
        manifests = list((ROOT / "references/ship-a-skill").glob("*/manifest.json"))
        self.assertTrue(manifests)
        for file in manifests:
            for record in json.loads(file.read_text())["screens"]:
                for role in ("display", "sans", "mono"):
                    family = tokens[f"font-{role}"].split(",")[0].strip('" ')
                    self.assertIn(f'"{family}"', record["fonts"][role],
                                  f'{record["id"]}: {role} differs from the live reference')


if __name__ == "__main__":
    unittest.main()
