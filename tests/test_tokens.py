import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_tokens", ROOT / "build-tokens.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class TokenTests(unittest.TestCase):
    def test_committed_css_matches_design_source(self):
        source = (ROOT / "DESIGN.md").read_text()
        self.assertEqual((ROOT / "bauhausian-tokens.css").read_text(), builder.render(source))

    def test_unknown_reference_is_rejected(self):
        source = '---\n{"tokens":{"ink":"var(--missing)"}}\n---\n'
        with self.assertRaisesRegex(ValueError, "missing"):
            builder.render(source)

    def test_cyclic_reference_is_rejected(self):
        source = '---\n{"tokens":{"first":"var(--second)","second":"var(--first)"}}\n---\n'
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            builder.render(source)

    def test_malformed_frontmatter_is_rejected(self):
        with self.assertRaises(ValueError):
            builder.render("# No tokens")

    def test_css_injection_is_rejected(self):
        source = '---\n{"tokens":{"ink":"red; } body { display:none"}}\n---\n'
        with self.assertRaises(ValueError):
            builder.render(source)

    def test_component_references_are_defined(self):
        import re
        tokens = builder.read_tokens((ROOT / "DESIGN.md").read_text())
        for file in ("components.css", "showcase.css"):
            references = set(re.findall(r"var\(--([a-z0-9-]+)\)", (ROOT / file).read_text()))
            self.assertFalse(references - tokens.keys(), f"{file}: undefined variables")

    def test_text_color_pairs_meet_normal_text_contrast(self):
        tokens = builder.read_tokens((ROOT / "DESIGN.md").read_text())

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
            return sum(a * b for a, b in zip(linear, (.2126, .7152, .0722)))

        for foreground, background in [
            ("ink", "surface"), ("ink-muted", "surface"), ("on-blue", "bauhaus-blue"),
            ("on-orange", "bauhaus-orange"), ("on-yellow", "bauhaus-yellow"),
            ("success", "success-soft"), ("warning", "warning-soft"),
            ("destructive", "destructive-soft"),
        ]:
            light, dark = sorted((luminance(tokens[foreground]), luminance(tokens[background])),
                                 reverse=True)
            self.assertGreaterEqual((light + .05) / (dark + .05), 4.5,
                                    f"{foreground} on {background}")


if __name__ == "__main__":
    unittest.main()
