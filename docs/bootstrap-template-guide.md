### Bootstrap 5 Guide for base.html and core/index.html

This guide explains how Bootstrap 5 is used in the project templates and doubles as a quick onboarding to Bootstrap 5.
Read it alongside these files:

- Template: `templates/base.html`
- Page: `templates/core/index.html`
- Custom CSS: `static/css/main.css`

#### What you’ll learn

- How Bootstrap is included (CSS/JS) in dev vs. production
- The overall layout pattern (sticky footer with flexbox)
- How the navbar is built with `navbar`, `collapse`, and utilities
- How the footer uses the grid and utilities
- How the home page hero uses spacing, typography, and responsive images
- Key Bootstrap utilities and components appearing in the templates

---

### 1) Including Bootstrap and project CSS

Where: `templates/base.html`

- In development (`{% if debug %}`):
    - CSS: `static/vendor/bootstrap/bootstrap.min.css`
    - JS: `static/vendor/bootstrap/bootstrap.bundle.min.js` (includes Popper)
- In production (`{% else %}`):
    - CSS/JS from the official jsDelivr CDN with SRI `integrity` and `crossorigin`.

Custom stylesheet:

- `static/css/main.css` is loaded after Bootstrap so you can override styles (e.g., active pill color).

Theme toggle:

- The `<html>` element has `data-bs-theme="light"`. In Bootstrap 5.3+, this sets the color mode. You could change to
  `dark` or implement a runtime switch.

Favicon:

- A standard shortcut icon is linked using Django’s `{% static %}` tag.

Key takeaway: Always load your own CSS after Bootstrap so your overrides win if selectors match.

---

### 2) Page layout: sticky footer with flex utilities

Where: `<body class="min-vh-100 d-flex flex-column flex-shrink-0 bg-light">`

- `min-vh-100`: make the body at least the full viewport height.
- `d-flex flex-column`: turn the body into a vertical flex container.
- `flex-shrink-0`: prevent the body from shrinking below its content.
- `bg-light`: give the page a light background.

Pattern goal: keep the footer at the bottom even on short pages.

- The main content lives inside template blocks `{% block body %}{% block content %}…`.
- The footer wrapper uses `mt-auto` to push itself to the bottom of the page:
    - `mt-auto`: automatic top margin consumes remaining vertical space in the flex column.

Common extension: wrap page content with a `.container` to constrain width and use Bootstrap’s responsive gutters.

---

### 3) Accessibility helpers

- Skip link: `<a class="visually-hidden-focusable" href="#content">Skip to main content</a>` becomes visible when
  focused via keyboard, enabling quick navigation past the header.
- Use `id="content"` on your main content container to make the skip link target meaningful.

---

### 4) Navbar breakdown (header)

Where: `templates/base.html` → `<nav class="navbar navbar-expand-lg navbar-light shadow-lg border">`

Core navbar classes:

- `navbar`: base navbar component.
- `navbar-expand-lg`: the navbar content is collapsed below the `lg` breakpoint and expands at `lg` and above.
- `navbar-light`: uses light-appropriate brand/text colors. Pair with a light background (e.g., default or `bg-light`).
- `shadow-lg border`: add a large drop shadow and a border to distinguish the header.

Content container:

- `<div class="container">` constrains the navbar’s width and centers its content.

Brand:

- `<a class="navbar-brand" href="/">` standard brand link.
- The logo image uses `d-inline-block align-text-bottom` to align with text baseline.
- The brand text uses a display utility: `fs-4` (font-size scale).

Responsive collapse:

- Toggler button (`.navbar-toggler`) controls the collapsible area via data attributes:
    - `data-bs-toggle="collapse"` enables the JS behavior.
    - `data-bs-target="#navbarText"` references the collapsible container ID.
    - Inside, `.navbar-toggler-icon` renders the icon (requires Bootstrap CSS + appropriate navbar color scheme).
- Collapsible container: `<div class="collapse navbar-collapse" id="navbarText">` wraps the nav content that should hide
  on small screens and show when toggled. `collapse` handles the generic show/hide behavior. `navbar-collapse` provides
  additional styling for the collapsible area.

Nav links layout:

- `<div class="navbar-nav d-flex flex-column flex-sm-row gap-2 text-nowrap ms-auto">`
    - `navbar-nav`: container for nav links.
    - `d-flex`: switch to flex so utilities can apply directly.
    - `flex-column flex-sm-row`: stack links vertically on extra-small screens, horizontally from `sm` and up.
    - `gap-2`: consistent spacing between children.
    - `text-nowrap`: prevent line breaks within links/buttons.
    - `ms-auto`: push the whole group to the right (auto left margin in LTR).

Links and buttons:

- Links: `.nav-link` for standard navbar links.
- Buttons: `.btn` pairs with variants such as `.btn-primary`, `.btn-outline-primary`, `.btn-outline-dark` to create
  emphasized actions (Sign In/Up/Out).

Practical tips:

- Keep your toggler `data-bs-target` in sync with the collapse container `id`.
- Combine `navbar-expand-*` with `flex-*` utilities to control how nav items stack and align at each breakpoint.

---

### 5) Footer: CTA section + informational footer

Where: `templates/base.html` → `{% block footer %}`

CTA section:

- `<section class="py-5 bg-primary bg-opacity-10">`
    - `py-5`: vertical padding to create breathing room.
    - `bg-primary bg-opacity-10`: softly tinted background using the primary hue.
- Inner container: `<div class="container text-center">`
    - `text-center`: center-align headings, text, and buttons.
- Typography and button:
    - `fw-bold mb-3`: bold heading with bottom margin.
    - `lead mb-4`: larger lead paragraph with spacing.
    - `btn btn-primary btn-lg`: prominent call-to-action button.

Main footer block:

- Wrapper: `<div class="bg-light py-3 border-top">` adds separation from content.
- Layout container: `<div class="container">`.
- Top row: `<div class="row py-2">`
    - Left column: `col-12 col-md-3 mb-3 mb-md-0`
        - `col-12`: full width on extra small.
        - `col-md-3`: 3/12 width from `md` and up.
        - `mb-3 mb-md-0`: vertical spacing on small screens only.
        - Brand uses `d-inline-flex align-items-center` to align image and text; image gets `me-2` for spacing.
    - Right area: `col-12 col-md-9` wraps a nested grid.
        - Nested `row justify-content-end` aligns the link groups to the right at larger sizes.
        - Each links column uses `col-md-3 mb-2` and contains unstyled lists:
            - `list-unstyled`: removes default bullets and padding.
            - Links use `text-decoration-none text-body-secondary` for subtle, clean appearance.

Bottom row:

- `<div class="row pt-3 border-top">` separates legal text.
- Left column shows a copyright notice using `text-body-secondary`.

Key takeaway: The footer combines the grid system (`row`/`col-*`) with spacing utilities to produce a clean, responsive
multi-column layout.

---

### 6) Home page hero (index.html)

Where: `templates/core/index.html`

Hero wrapper:

- `<div class="px-7 pt-5 my-5 text-center">`
    - `pt-5 my-5`: generous top margin and vertical spacing.
    - `px-7`: non-standard in Bootstrap 5 by default; this likely relies on a custom spacing scale if provided
      elsewhere. If no custom CSS defines `px-7`, consider replacing with `px-5` or a responsive combination (e.g.,
      `px-3 px-md-5`).
    - `text-center`: center-align all children.

Heading and lead:

- `<h1 class="display-4 fw-bold">`: large display size with bold weight.
- `<p class="lead mb-4">`: a lead paragraph with comfortable bottom margin.

Width constraint and centering:

- `<div class="col-lg-6 mx-auto">` uses grid column width as a utility container:
    - `col-lg-6`: max width equals 6/12 columns on large screens.
    - `mx-auto`: center horizontally.

Image block:

- `<div class="overflow-hidden" style="max-height: 30vh;">` crops any overflow for a ribbon effect.
- Inner container `container px-5` adds horizontal padding.
- Image classes: `img-fluid border rounded-3 shadow-lg mb-4`
    - `img-fluid`: responsive width (max-width: 100%) and auto height.
    - `border`: 1px border.
    - `rounded-3`: medium rounding.
    - `shadow-lg`: pronounced drop shadow.
    - `mb-4`: spacing below.

---

### 7) Custom CSS overrides

Where: `static/css/main.css`

```css
.nav-pills .nav-link.active {
    background-color: var(--bs-secondary) !important;
    color: #fff;
}

.nav-pills .nav-link {
    color: var(--bs-dark);
}
```

- Demonstrates how to adjust Bootstrap component styles using CSS variables (`--bs-secondary`) and selectors.
- Because `main.css` is loaded after Bootstrap, these rules override defaults.

---

### 8) Quick reference: common Bootstrap utilities used

- Layout and flex:
    - `d-flex`, `flex-column`, `flex-sm-row`, `ms-auto`, `mt-auto`
- Spacing:
    - `py-5`, `pt-5`, `my-5`, `mb-4`, `mb-3`, `pt-3`, `px-5`, `gap-2`, `me-2`
- Sizing and typography:
    - `display-4`, `fs-4`, `fw-bold`, `lead`, `text-center`, `text-body-secondary`, `text-decoration-none`,
      `text-nowrap`
- Backgrounds and borders:
    - `bg-light`, `bg-primary`, `bg-opacity-10`, `border`, `border-top`, `shadow-lg`, `rounded-3`
- Grid:
    - `container`, `row`, `col-12`, `col-md-3`, `col-md-9`, `col-lg-6`, `mx-auto`
- Components:
    - Navbar: `navbar`, `navbar-brand`, `navbar-nav`, `nav-link`, `navbar-expand-lg`, `navbar-toggler`,
      `navbar-toggler-icon`, `collapse navbar-collapse`
    - Buttons: `btn`, `btn-primary`, `btn-outline-primary`, `btn-outline-dark`, `btn-lg`
    - Images: `img-fluid`
- Helpers and accessibility:
    - `visually-hidden-focusable`, `overflow-hidden`, `min-vh-100`

Note: `px-7` is not part of default Bootstrap. If you want that extra spacing without custom CSS, consider `px-5` or
responsive utilities like `px-4 px-lg-5`.

---

### 9) How it works together: the navbar as an example

1) Structure and breakpoints

- `navbar navbar-expand-lg`: base navbar that collapses below `lg`.

2) Toggler + Collapse

- The button with `data-bs-toggle="collapse"` and `data-bs-target="#navbarText"` wires to the div with `id="navbarText"`
  and classes `collapse navbar-collapse`. Bootstrap’s JS toggles visibility and adds appropriate ARIA attributes.

3) Alignment and spacing

- `ms-auto` pushes the nav group to the right.
- `flex-column flex-sm-row gap-2` stacks links vertically on small screens, horizontally from `sm` upward, with
  consistent gaps.

4) Visual appearance

- `navbar-light` for color scheme, plus `shadow-lg border` to separate the navbar from the page.
- Action items use `.btn` variants for visual hierarchy.

---

### 10) Extending the templates (examples)

Add a new nav link:

```html
<a class="nav-link" href="{% url 'core:home' %}">Home</a>
```

Add a dropdown to the navbar (requires Bootstrap JS):

```html

<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        Products
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Item 1</a></li>
        <li><a class="dropdown-item" href="#">Item 2</a></li>
    </ul>
</li>
```

Wrap page content in a container:

```html
{% block content %}
<main id="content" class="container py-4">
    <!-- Your content here -->
</main>
{% endblock %}
```

Add a responsive two-column section:

```html

<div class="container py-5">
    <div class="row g-4">
        <div class="col-12 col-md-6">Left</div>
        <div class="col-12 col-md-6">Right</div>
    </div>
</div>
```

---

### 11) Bootstrap JS components used

- Collapse (navbar) via `data-bs-*` attributes, powered by `bootstrap.bundle.min.js`.
- You can safely use other JS components (dropdowns, modals, tooltips) by adding the right markup and data attributes.
  No extra JS is required beyond the bundle already included.

---

### 12) Pitfalls and best practices

- Ensure the toggler `data-bs-target` matches the collapse container `id`.
- Load your custom CSS after Bootstrap to ensure overrides apply.
- Prefer utilities over custom CSS for spacing, colors, and display when possible.
- Use `container`/`row`/`col-*` for structured grids; avoid nesting containers unnecessarily.
- Validate non-standard classes (e.g., `px-7`) and replace with Bootstrap utilities unless you’ve intentionally extended
  the scale.
- Keep accessibility in mind: use `visually-hidden-focusable` skip links and semantic HTML.

---

### 13) Where to look next

- Official docs: https://getbootstrap.com/docs/5.3/getting-started/introduction/
- Utilities overview: https://getbootstrap.com/docs/5.3/utilities/api/
- Components reference: https://getbootstrap.com/docs/5.3/components/navbar/

This project sets up a pragmatic, responsive baseline with Bootstrap 5. Reuse the structure, rely on utilities, and
layer in components as your pages grow.

### Best Practices

#### Container Usage

The base template includes a container wrapper for each major section of the page:

- Navbar: Has a container (`<div class="container">`) ✅
- Footer CTA section: Has a container (`<div class="container text-center">`) ✅
- Main footer: Has a container (`<div class="container">`)  ✅
- Body content: No container wrapper ❌

For proper container management it is recommended to have one container per content block.
This is the most flexible approach:

- Each major section (navbar, main content, footer) manages its own container
- Allows for full-width sections when needed (like hero banners)
- Gives you granular control over each section's layout

You could wrap everything in one container on the `<body>` tag, but this limits your design flexibility.