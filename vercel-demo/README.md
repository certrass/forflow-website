# ForFlow Vercel Demo

This folder is the isolated Next.js pilot for Vercel preview validation. It does not replace the current Netlify production site and does not bind the production domain.

## Scope

- `src/app/page.tsx`: migrated homepage pilot with ForFlow hero, challenge, service, Navigator, case, resource, FAQ, and footer sections.
- `src/app/cases/page.tsx`: case-library migration skeleton.
- `src/app/navigator/page.tsx`: interactive Navigator pilot.
- `src/lib/demo-content.ts`: first TypeScript content source for migrated data.
- `public/forflow/`: copied brand and runtime assets used only by this demo.

The homepage links only to existing demo routes (`/`, `/cases`, `/navigator`) or same-page anchors. It does not depend on the current Netlify static HTML pages for navigation.

## Local Checks

```bash
npm run lint
npm run build
npm run dev
```

Open `http://127.0.0.1:3000` or the port reported by Next.js.

## Vercel Preview

From the repository root, use this folder as the Vercel project root:

```bash
tools/with-veee-proxy.sh npx vercel@54.16.0 login
tools/with-veee-proxy.sh npx vercel@54.16.0 deploy --yes --cwd vercel-demo
```

For Git integration, import the repository in Vercel and set the project root directory to `vercel-demo`. Keep production domains on the existing Netlify project until local checks, Vercel preview checks, and China access checks all pass.
