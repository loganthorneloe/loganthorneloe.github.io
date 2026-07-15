import unittest

from scripts.sync_public_cv import build_public_cv


SOURCE = """## Personal Information

- **Email:** private@example.com
- **Phone:** 555-555-1234

## Professional Summary

Public summary.

This whole paragraph must be removed even when the sensitive phrase is
wrapped onto a line mentioning disabilities.

## Work Experience

### Google Ads - Machine Learning Infrastructure
**Software Engineer**
Austin, Texas
June 2022 - Present

- Built an internal system serving 100 teams.
- Support researchers by translating client needs into tooling improvements.
- Worked through sensitive-data and privacy constraints.

### Previous Employer
**Software Engineer**
Los Alamos, New Mexico
2020 - 2022

- Built a public project.

## Publications

- A public paper.

## Education

### Example University
**Bachelor of Science**
Provo, Utah
2015 - 2020

#### Awards & Recognition
- Google Lime Scholar - scholarship for students with disabilities
- Public academic award

#### Additional Scholarships
- Need-based scholarship

## Projects

- Public open-source project
- Lime Connect volunteer

## Activities and Service

- Private personal history

## STAR Examples Bank

- Conflict and failure interview notes

# Brand

- Private positioning notes
"""


class PublicCvTests(unittest.TestCase):
    def test_builds_conservative_public_subset(self):
        public_cv = build_public_cv(SOURCE)

        self.assertIn("Public summary.", public_cv)
        self.assertIn("Support researchers", public_cv)
        self.assertIn("Built a public project.", public_cv)
        self.assertIn("Public academic award", public_cv)
        self.assertNotIn("private@example.com", public_cv)
        self.assertNotIn("555-555-1234", public_cv)
        self.assertNotIn("Austin, Texas", public_cv)
        self.assertNotIn("Los Alamos, New Mexico", public_cv)
        self.assertNotIn("100 teams", public_cv)
        self.assertNotIn("sensitive-data", public_cv)
        self.assertNotIn("Lime", public_cv)
        self.assertNotIn("Need-based", public_cv)
        self.assertNotIn("Private personal history", public_cv)
        self.assertNotIn("interview notes", public_cv)
        self.assertNotIn("positioning notes", public_cv)
        self.assertNotIn("This whole paragraph", public_cv)

    def test_requires_expected_source_structure(self):
        with self.assertRaisesRegex(ValueError, "Missing required CV sections"):
            build_public_cv("## Professional Summary\n\nOnly one section.")


if __name__ == "__main__":
    unittest.main()
