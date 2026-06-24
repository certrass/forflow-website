import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-deps'))

from playwright.async_api import async_playwright

BASE = os.environ.get('BASE_URL', 'http://127.0.0.1:8765').rstrip('/')
CDP_URL = os.environ.get('CDP_URL', f'http://127.0.0.1:{os.environ.get("CDP_PORT", "9226")}')
OUT = ROOT / 'tests' / 'polished'
OUT.mkdir(parents=True, exist_ok=True)

async def inspect_page(browser, name, path, viewport):
    context = await browser.new_context(viewport=viewport, device_scale_factor=1)
    await context.add_init_script("""(() => {
      const original = Element.prototype.scrollIntoView;
      window.__ffScrollIntoViewCalls = [];
      Element.prototype.scrollIntoView = function patchedScrollIntoView(options) {
        window.__ffScrollIntoViewCalls.push({
          tag: this.tagName,
          text: (this.textContent || '').trim().slice(0, 40),
          y: Math.round(window.scrollY),
          options,
        });
        return original.call(this, options);
      };
    })();""")
    page = await context.new_page()
    page.set_default_timeout(8000)
    errors = []
    page.on('console', lambda msg: errors.append(f'{msg.type}: {msg.text}') if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(f'pageerror: {exc}'))
    response = await page.goto(BASE + path, wait_until='networkidle')
    await page.wait_for_timeout(400)
    await page.evaluate("document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-revealed'))")
    await page.evaluate("""async () => {
      document.querySelectorAll('img[loading="lazy"]').forEach((img) => img.setAttribute('loading', 'eager'));
      await Promise.all([...document.images].map((img) => {
        if (img.complete && img.naturalWidth) return true;
        return new Promise((resolve) => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        });
      }));
    }""")
    await page.screenshot(path=str(OUT / f'{name}.png'), full_page=False)
    vertical_scroll = await page.evaluate("""async () => {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      document.documentElement.style.scrollBehavior = 'auto';
      document.body.style.scrollBehavior = 'auto';
      window.scrollTo({ top: 0, behavior: 'instant' });
      await sleep(120);
      window.scrollBy({ top: window.innerHeight * 1.2, behavior: 'instant' });
      await sleep(120);
      window.scrollBy({ top: window.innerHeight * 1.2, behavior: 'instant' });
      await sleep(120);
      let previousBottom = -1;
      for (let i = 0; i < 10; i += 1) {
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' });
        await sleep(300);
        const bottom = Math.round(window.scrollY + window.innerHeight);
        const total = Math.round(document.documentElement.scrollHeight);
        if (Math.abs(bottom - previousBottom) < 2 && bottom >= total - 4) break;
        previousBottom = bottom;
      }
      const bottom = Math.round(window.scrollY + window.innerHeight);
      const scrollHeight = Math.round(document.documentElement.scrollHeight);
      for (let i = 0; i < 8; i += 1) {
        window.scrollTo({ top: 0, behavior: 'instant' });
        await sleep(160);
        if (Math.round(window.scrollY) === 0) break;
      }
      const top = Math.round(window.scrollY);
      return {
        bottom,
        scrollHeight,
        reachedBottom: bottom >= scrollHeight - 4,
        top,
        returnedTop: top === 0,
      };
    }""")
    result = {
        'status': response.status if response else None,
        'title': await page.title(),
        'viewport': viewport,
        'scrollWidth': await page.evaluate('document.documentElement.scrollWidth'),
        'innerWidth': await page.evaluate('window.innerWidth'),
        'caseTocOverflow': await page.evaluate("""() => {
          const toc = document.querySelector('.case-toc');
          if (!toc) return null;
          return {
            clientWidth: toc.clientWidth,
            scrollWidth: toc.scrollWidth,
            overflowX: getComputedStyle(toc).overflowX,
            position: getComputedStyle(toc).position,
          };
        }"""),
        'verticalScroll': vertical_scroll,
        'scrollIntoViewCalls': await page.evaluate("window.__ffScrollIntoViewCalls || []"),
        'missingImages': await page.evaluate("[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.getAttribute('src'))"),
        'consoleErrors': errors,
    }
    await context.close()
    return result

async def main():
    report = {'pages': {}, 'interactions': {}}
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)

        report['pages']['index-desktop'] = await inspect_page(browser, 'index-desktop-viewport', '/index.html', {'width': 1440, 'height': 1000})
        report['pages']['index-mobile'] = await inspect_page(browser, 'index-mobile-viewport', '/index.html', {'width': 390, 'height': 844})
        report['pages']['playbook-desktop'] = await inspect_page(browser, 'playbook-desktop-viewport', '/playbook.html', {'width': 1440, 'height': 1000})
        report['pages']['playbook-mobile'] = await inspect_page(browser, 'playbook-mobile-viewport', '/playbook.html', {'width': 390, 'height': 844})
        report['pages']['cases-desktop'] = await inspect_page(browser, 'cases-desktop-viewport', '/cases.html', {'width': 1440, 'height': 1000})
        report['pages']['cases-mobile'] = await inspect_page(browser, 'cases-mobile-viewport', '/cases.html', {'width': 390, 'height': 844})
        report['pages']['healthcare-case-desktop'] = await inspect_page(browser, 'healthcare-case-desktop-viewport', '/case-healthcare-agent-roi.html', {'width': 1440, 'height': 1000})
        report['pages']['healthcare-case-mobile'] = await inspect_page(browser, 'healthcare-case-mobile-viewport', '/case-healthcare-agent-roi.html', {'width': 390, 'height': 844})
        report['pages']['automotive-case-desktop'] = await inspect_page(browser, 'automotive-case-desktop-viewport', '/case-automotive-dfmea-ontology-agent.html', {'width': 1440, 'height': 1000})
        report['pages']['automotive-case-mobile'] = await inspect_page(browser, 'automotive-case-mobile-viewport', '/case-automotive-dfmea-ontology-agent.html', {'width': 390, 'height': 844})

        context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = await context.new_page(); page.set_default_timeout(8000)
        await page.goto(BASE + '/index.html', wait_until='networkidle')
        trigger = page.locator('[data-mega-trigger]').filter(has_text='企业服务')
        await trigger.click(); await page.wait_for_timeout(280)
        opened = await trigger.evaluate("el => el.getAttribute('aria-expanded') === 'true' && el.closest('.mega-item')?.classList.contains('is-open')")
        await page.screenshot(path=str(OUT / 'index-mega-menu.png'), full_page=False)
        await page.keyboard.press('Escape'); await page.wait_for_timeout(280)
        closed = await trigger.evaluate("el => el.getAttribute('aria-expanded') === 'false' && !el.closest('.mega-item')?.classList.contains('is-open')")
        search = page.get_by_role('button', name='打开全站搜索')
        await search.click(); await page.wait_for_timeout(220)
        search_open = await page.locator('[data-search-modal]').evaluate("el => el.classList.contains('is-open')")
        report['interactions']['desktopNavigation'] = {
            'megaOpened': opened,
            'megaClosedWithEscape': closed,
            'searchModalOpened': search_open,
        }
        await context.close()

        context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = await context.new_page(); page.set_default_timeout(8000)
        await page.goto(BASE + '/playbook.html', wait_until='networkidle')
        tool = page.locator('[data-decision-tool]')
        build_buttons = tool.locator('[data-decision-vote="build"]')
        for i in range(await build_buttons.count()):
            await build_buttons.nth(i).click()
        recommendation = await tool.locator('[data-decision-result]').inner_text()
        await tool.scroll_into_view_if_needed(); await page.wait_for_timeout(200)
        await tool.screenshot(path=str(OUT / 'playbook-decision-tool.png'))
        await page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight * 0.55)')
        await page.wait_for_timeout(220)
        progress = await page.locator('[data-playbook-progress]').evaluate("el => ({style: el.style.width, value: el.parentElement.getAttribute('aria-valuenow')})")
        report['interactions']['playbook'] = {
            'decisionRecommendation': recommendation,
            'progress': progress,
        }
        await context.close()

        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page(); page.set_default_timeout(8000)
        await page.goto(BASE + '/playbook.html', wait_until='networkidle')
        await page.locator('.menu-toggle').click(); await page.wait_for_timeout(180)
        site_menu = await page.locator('.mobile-menu-panel').is_visible()
        await page.locator('.menu-toggle').click(); await page.wait_for_timeout(180)
        await page.locator('[data-toc-open]').click(); await page.wait_for_timeout(200)
        toc_drawer = await page.locator('[data-toc-drawer]').is_visible()
        report['interactions']['mobile'] = {'siteMenuOpened': site_menu, 'playbookTocOpened': toc_drawer}
        await context.close()

        context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = await context.new_page(); page.set_default_timeout(8000)
        await page.goto(BASE + '/cases.html', wait_until='networkidle')
        await page.locator('[data-case-filter="service"]').click(); await page.wait_for_timeout(180)
        healthcare_visible = await page.locator('#healthcare-agent-roi').is_visible()
        pid_present = await page.locator('#pid[href="case-manufacturing-pid-intelligence.html"]').count() == 1
        automotive_present = await page.locator('#automotive-dfmea-ontology-agent[href="case-automotive-dfmea-ontology-agent.html"]').count() == 1
        await page.goto(BASE + '/search.html?search=医疗', wait_until='networkidle')
        case_count = await page.locator('[data-count-case]').inner_text()
        healthcare_search = await page.locator('a[href="case-healthcare-agent-roi.html"]').is_visible()
        await page.goto(BASE + '/search.html?search=DFMEA', wait_until='networkidle')
        automotive_case_count = await page.locator('[data-count-case]').inner_text()
        automotive_search = await page.locator('a[href="case-automotive-dfmea-ontology-agent.html"]').is_visible()
        report['interactions']['cases'] = {
            'healthcareVisibleAfterServiceFilter': healthcare_visible,
            'pidCardPresent': pid_present,
            'automotiveCardPresent': automotive_present,
            'medicalSearchHasCase': int(case_count) >= 1,
            'healthcareSearchResultVisible': healthcare_search,
            'dfmeaSearchHasCase': int(automotive_case_count) >= 1,
            'automotiveSearchResultVisible': automotive_search,
        }
        await context.close()

        await browser.close()

    (OUT / 'polished-check-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    failures = []
    for name, data in report['pages'].items():
        if data['status'] != 200: failures.append(f'{name}: HTTP {data["status"]}')
        if data['scrollWidth'] > data['innerWidth'] + 1: failures.append(f'{name}: horizontal overflow')
        toc = data.get('caseTocOverflow')
        if 'case-' in name and 'mobile' in name and toc and toc['scrollWidth'] > toc['clientWidth'] + 1:
            failures.append(f'{name}: case toc horizontal scroll')
        if 'case-' in name and 'mobile' in name and data.get('scrollIntoViewCalls'):
            failures.append(f'{name}: scrollspy nudged page {data["scrollIntoViewCalls"]}')
        if not data['verticalScroll']['reachedBottom']: failures.append(f'{name}: vertical scroll did not reach bottom')
        if not data['verticalScroll']['returnedTop']: failures.append(f'{name}: vertical scroll did not return to top')
        if data['missingImages']: failures.append(f'{name}: missing images {data["missingImages"]}')
        if data['consoleErrors']: failures.append(f'{name}: console errors {data["consoleErrors"]}')
    if not all(report['interactions']['desktopNavigation'].values()): failures.append('desktop navigation interaction failed')
    if not all(report['interactions']['mobile'].values()): failures.append('mobile navigation interaction failed')
    if not all(report['interactions']['cases'].values()): failures.append('case/search interaction failed')
    if '建设为主' not in report['interactions']['playbook']['decisionRecommendation']: failures.append('decision tool failed')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(json.dumps(report, ensure_ascii=False, indent=2))

asyncio.run(main())
