"""Keep the homepage's shared base isolated from the other live pages.

Edit styles.css/script.js as usual; these copies are generated, not maintained.
Only the homepage links them, allowing a homepage-only deploy without replacing
shared files used by service and case detail pages.
"""
from pathlib import Path
from shutil import copyfile


def sync(root: Path):
    target = root / 'assets/site'
    target.mkdir(parents=True, exist_ok=True)
    copyfile(root / 'styles.css', target / 'home-base.css')
    copyfile(root / 'script.js', target / 'home-interactions.js')
    copyfile(root / 'templates/index.html', root / 'index.html')
    product_assets = root / 'output/homepage-v6/public/assets/site'
    product_assets.mkdir(parents=True, exist_ok=True)
    for name in ['brand-wall.css', 'guru-system.css', 'guru-motion.css', 'guru-motion.js', 'guru-navigation.css', 'guru-navigation.js', 'navigation-content.json']:
        copyfile(target / name, product_assets / name)


if __name__ == '__main__':
    sync(Path(__file__).resolve().parents[1])
