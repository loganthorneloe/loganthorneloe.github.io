import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build


class SiteBuildTests(unittest.TestCase):
    def test_feed_filters_invalid_links_and_sorts_unique_posts(self):
        def item(slug, day, title='Article'):
            return (f'<item><title>{title}</title><link>{slug}</link>'
                    f'<pubDate>Mon, {day:02} Oct 2026 12:00:00 GMT</pubDate></item>')
        xml = '<rss><channel>' + ''.join([
            item('https://www.aiforswes.com/p/old', 1),
            item('https://www.aiforswes.com/p/new', 12, 'AI &amp; systems'),
            item('https://www.aiforswes.com/p/new', 12),
            item('javascript:alert(1)', 13),
            item('https://example.com/p/not-newsletter', 13),
        ]) + '</channel></rss>'
        posts = build.parse_posts(xml)
        self.assertEqual([p['title'] for p in posts], ['AI & systems', 'Article'])

    def test_only_first_article_has_image_and_titles_are_escaped(self):
        post = {'title': '<script> & title', 'link': 'https://www.aiforswes.com/p/a',
                'date': '2026-10-12', 'image_url': 'https://example.com/cover.jpg'}
        rendered = build.render_articles([post] * 5)
        self.assertEqual(rendered.count('<img '), 1)
        self.assertEqual(rendered.count('class="article-link lb-tile"'), 5)
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt; &amp; title', rendered)

    def test_unavailable_feed_retains_cached_articles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            cached = [{'title': 'Cached article'}]
            (root / 'data/latest-articles.json').write_text(json.dumps(cached))
            with patch.object(build, 'fetch', side_effect=OSError('offline')):
                self.assertEqual(build.load_posts(root), cached)

    def test_offline_build_preserves_routes_and_project_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ['templates', 'data', 'static']:
                shutil.copytree(build.ROOT / folder, root / folder)
            with patch.object(build, 'fetch', side_effect=AssertionError('Network access')):
                build.build(root, offline=True)
            home = (root / 'index.html').read_text()
            about = (root / 'about/index.html').read_text()
            self.assertNotIn('{{', home + about)
            self.assertIn('https://thorneloe.ai/about', about)
            self.assertIn('href="https://thorneloe.ai/jobs/"', home)
            self.assertIn('href="https://thorneloe.ai/stockboy/"', home)
            self.assertIn('<article class="card lb-tile" data-tool="ml">', home)
            self.assertIn('href="/#projects"', about)
            self.assertEqual(home.count('class="article-image"'), 1)
            self.assertEqual(home.count('class="article-link lb-tile"'), 5)


if __name__ == '__main__':
    unittest.main()
