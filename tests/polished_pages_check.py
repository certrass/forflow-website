import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8765'
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests' / 'polished'
OUT.mkdir(parents=True, exist_ok=True)

async def inspect_page(browser, name, path, viewport):
    context = await browser.new_context(viewport=viewport, device_scale_factor=1)
    page = await context.new_page()
    page.set_default_timeout(8000)
    errors = []
    page.on('console', lambda msg: errors.append(f'{msg.type}: {msg.text}') if msg.type == 'error' else None)
    page.on('pageerror', lambda exc: errors.append(f'pageerror: {exc}'))
    response = await page.goto(BASE + path, wait_until='networkidle')
    await page.wait_for_timeout(400)
    await page.evaluate("document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-revealed'))")
    await page.screenshot(path=str(OUT / f'{name}.png'), full_page=False)
    result = {
        'status': response.status if response else None,
        'title': await page.title(),
        'viewport': viewport,
        'scrollWidth': await page.evaluate('document.documentElement.scrollWidth'),
        'innerWidth': await page.evaluate('window.innerWidth'),
        'missingImages': await page.evaluate("[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.getAttribute('src'))"),
        'consoleErrors': errors,
    }
    await context.close()
    return result

async def main():
    report = {'pages': {}, 'interactions': {}}
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9226')

        report['pages']['index-desktop'] = await inspect_page(browser, 'index-desktop-viewport', '/index.html', {'width': 1440, 'height': 1000})
        report['pages']['index-mobile'] = await inspect_page(browser, 'index-mobile-viewport', '/index.html', {'width': 390, 'height': 844})
        report['pages']['playbook-desktop'] = await inspect_page(browser, 'playbook-desktop-viewport', '/playbook.html', {'width': 1440, 'height': 1000})
        report['pages']['playbook-mobile'] = await inspect_page(browser, 'playbook-mobile-viewport', '/playbook.html', {'width': 390, 'height': 844})

        context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = await context.new_page(); page.set_default_timeout(8000)
        await page.goto(BASE + '/index.html', wait_until='networkidle')
        trigger = page.locator('[data-mega-trigger]').filter(has_text='企业服务')
        await trigger.click(); await page.wait_for_timeout(280)
        opened = await page.locator('.mega-panel--services').is_visible()
        await page.screenshot(path=str(OUT / 'index-mega-menu.png'), full_page=False)
        await page.keyboard.press('Escape'); await page.wait_for_timeout(280)
        closed = not await page.locator('.mega-panel--services').is_visible()
        search = page.get_by_role('button', name='打开全站搜索')
        await search.click(); await page.wait_for_timeout(220)
        search_open = await page.locator('[data-search-modal]').is_visible()
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

        await browser.close()

    (OUT / 'polished-check-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    failures = []
    for name, data in report['pages'].items():
        if data['status'] != 200: failures.append(f'{name}: HTTP {data["status"]}')
        if data['scrollWidth'] > data['innerWidth'] + 1: failures.append(f'{name}: horizontal overflow')
        if data['missingImages']: failures.append(f'{name}: missing images {data["missingImages"]}')
        if data['consoleErrors']: failures.append(f'{name}: console errors {data["consoleErrors"]}')
    if not all(report['interactions']['desktopNavigation'].values()): failures.append('desktop navigation interaction failed')
    if not all(report['interactions']['mobile'].values()): failures.append('mobile navigation interaction failed')
    if '建设为主' not in report['interactions']['playbook']['decisionRecommendation']: failures.append('decision tool failed')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(json.dumps(report, ensure_ascii=False, indent=2))

asyncio.run(main())
