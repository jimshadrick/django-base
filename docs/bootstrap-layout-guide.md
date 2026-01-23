# Bootstrap 5 Sidebar Layout Guide

## Overview

This guide documents the modern sidebar-based layout implementation for Django Base templates. It serves as both
documentation and a quick-start guide for understanding and extending the template system.

**Key Files:**

- Template: `templates/base.html`
- Dashboard: `templates/core/index.html`
- Account Management: `templates/allauth/layouts/manage.html`
- Custom CSS: `static/css/main.css`

---

## Introduction: Modern App Layout Architecture

### Why a Sidebar Layout?

This project moved from a traditional horizontal navbar to a **persistent sidebar navigation** pattern for several
strategic reasons:

1. **App-Focused Experience**: Sidebars are the de facto standard for SaaS applications and dashboards (Stripe, GitHub,
   Linear, Notion, etc.). They signal "application" rather than "website."

2. **Vertical Space Efficiency**: Top navbars consume valuable vertical real estate. Sidebars leverage unused horizontal
   space, especially on modern widescreen displays.

3. **Scalability**: Adding new navigation items doesn't cause overflow issues. Sidebars can scroll independently,
   supporting dozens of nav items without breaking the layout.

4. **Better Hierarchy**: Sidebar layouts naturally support section grouping and nested navigation, making complex app
   structures easier to navigate.

5. **Consistency Across Devices**: The same navigation pattern works on desktop (always visible) and mobile (collapsible
   overlay), providing a consistent mental model.

### Layout Philosophy

This template is designed for **generic Django applications** - not content-heavy blogs or marketing sites. The
priorities are:

- ✅ Clean, distraction-free workspace for forms and data
- ✅ Quick access to frequently-used functions
- ✅ Professional appearance for internal tools and SaaS products
- ✅ Easy customization for future projects

### How the Components Work Together

The layout uses a **three-zone architecture**:

```
┌─────────────┬──────────────────────────────────┐
│             │  Top Bar (page title + actions) │
│   Sidebar   ├──────────────────────────────────┤
│ (navigation)│                                  │
│             │    Main Content Area             │
│             │    (cards, forms, tables)        │
│             │                                  │
│             ├──────────────────────────────────┤
│             │  Minimal Footer                  │
└─────────────┴──────────────────────────────────┘
```

**Zone Responsibilities:**

1. **Sidebar** (260px wide, dark themed)
    - Primary navigation (Home, Account sections)
    - User authentication status and quick access
    - Collapses to overlay on mobile devices
    - Scrollable independently for long nav lists

2. **Top Bar** (flexible height, light themed)
    - Current page title (from `page_title_text` block)
    - Contextual action buttons (from `topbar_actions` block)
    - Mobile sidebar toggle button

3. **Main Content** (grows to fill available space)
    - Template content from `{% block content %}`
    - Uses `container-fluid` for full-width responsiveness
    - Light background to distinguish from cards
    - Scrollable independently

4. **Footer** (minimal, collapsed)
    - Essential links only (Privacy, Terms, Support)
    - No visual competition with main content
    - Designed to stay out of the way

### Key Design Decisions

**Unified Account Navigation**: Instead of the default django-allauth sidebar (which created redundant navigation), all
account management links are integrated into the main sidebar. This provides:

- Single source of truth for navigation
- No competing sidebars
- Maximum content area for forms
- Consistent with modern SaaS UX patterns

**No Breadcrumbs by Default**: While breadcrumbs can be useful for deep hierarchies, they were omitted because:

- The sidebar already shows context (highlighted active item)
- Most pages are 1-2 levels deep
- Cleaner appearance without extra navigation elements
- Can be added per-page if needed (see Section 10)

---

## 1) Dependencies and Asset Loading

**Location:** `templates/base.html` `<head>` section

### Bootstrap 5.3.5

```html

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/js/bootstrap.bundle.min.js" defer></script>
```

- Loaded from jsDelivr CDN with SRI (Subresource Integrity) hashes for security
- `bootstrap.bundle.min.js` includes Popper.js for dropdowns, tooltips, etc.
- `defer` attribute ensures non-blocking script loading

### Unpoly 3.12.1

```html

<script src="https://cdn.jsdelivr.net/npm/unpoly@3.12.1/unpoly.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/unpoly@3.12.1/unpoly.min.css">
<script src="https://cdn.jsdelivr.net/npm/unpoly@3.12.1/unpoly-bootstrap5.min.js"></script>
```

- Progressive enhancement library for smooth page transitions
- Bootstrap 5 integration for modal and drawer support
- Works with standard Django links - no JavaScript required in templates
- The Unpoly-Bootstrap 5 integration file is needed if Bootstrap's **interactive JavaScript components** (modals,
  dropdowns, tooltips, popovers, collapsible elements) are used within Unpoly-managed fragments.

### Bootstrap Icons 1.11.3

```html

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
```

- Icon font for navigation items, buttons, and UI elements
- Usage: `<i class="bi bi-house-door"></i>`
- Full icon list: https://icons.getbootstrap.com/

### Custom CSS

```html

<link rel="stylesheet" href="{% static 'css/main.css' %}">
```

- **CRITICAL**: Loaded *after* Bootstrap so overrides work correctly
- Contains sidebar styling, active states, and custom animations
- See Section 4 for detailed CSS breakdown

### Theme Configuration

```html

<html lang="en" data-bs-theme="light">
```

- Bootstrap 5.3+ color mode system
- Can be changed to `dark` or toggled dynamically with JavaScript
- Affects all Bootstrap components automatically

---

## 2) Base Layout Structure: Horizontal Flexbox

**Location:** `templates/base.html` `<body>` tag

```html

<body class="d-flex min-vh-100">
```

### Why This Pattern?

The layout uses a **horizontal flex container** at the body level to create the sidebar + content split. This is
fundamentally different from traditional top-nav layouts.

**Class Breakdown:**

- `d-flex`: Enables flexbox layout on the body
- `min-vh-100`: Ensures the layout always fills the viewport height, even with minimal content

**Child Elements:**

1. **Sidebar** (`<aside id="sidebar">`)
    - Fixed width (260px)
    - `flex-shrink-0`: Prevents sidebar from shrinking

2. **Main Wrapper** (`<div class="d-flex flex-column flex-grow-1">`)
    - `flex-grow-1`: Expands to fill remaining horizontal space
    - `d-flex flex-column`: Stacks top bar, content, and footer vertically

### Visual Representation:

```
Body: d-flex (horizontal)
├─ Sidebar: width 260px, flex-shrink-0
└─ Main Wrapper: flex-grow-1, d-flex flex-column (vertical)
   ├─ Top Bar: fixed height
   ├─ Content: flex-grow-1 (expands)
   └─ Footer: fixed height
```

This creates a **"holy grail" layout** where:

- Sidebar stays fixed width
- Content area grows/shrinks with window size
- Footer stays at bottom even with minimal content

---

## 3) Sidebar Navigation Breakdown

**Location:** `templates/base.html` → `<aside id="sidebar">`

### Sidebar Container

```html

<aside id="sidebar" class="bg-dark text-white d-flex flex-column flex-shrink-0 collapse collapse-horizontal show"
       style="width: 260px;">
```

**Class Analysis:**

- `bg-dark text-white`: Dark theme with light text (professional, app-like)
- `d-flex flex-column`: Vertical stack (brand → nav → user section)
- `flex-shrink-0`: Prevents sidebar from getting smaller than 260px
- `collapse collapse-horizontal show`: Bootstrap collapse component for mobile
    - `collapse`: Makes element collapsible
    - `collapse-horizontal`: Slides left/right instead of up/down
    - `show`: Visible by default on desktop
- `width: 260px`: Fixed sidebar width (inline style for clarity)

**Why Collapse-Horizontal?**

This pattern allows the sidebar to:

- Show by default on desktop (`lg` breakpoint and up)
- Hide off-screen on mobile (via CSS in `main.css`)
- Slide in as an overlay when toggled on mobile

### Sidebar Structure: Three Sections

#### 1. Brand Header

```html

<div class="p-3 border-bottom border-secondary">
    <a href="/" class="d-flex align-items-center text-white text-decoration-none">
        <img src="{% static 'images/logo.svg' %}" alt="Logo" height="28" class="me-2">
        <span class="fs-5 fw-semibold">Django Base</span>
    </a>
</div>
```

- `p-3`: Padding all sides for breathing room
- `border-bottom border-secondary`: Subtle separator
- `d-flex align-items-center`: Horizontally align logo and text
- `me-2`: Margin-end (right) spacing between logo and text
- `fs-5 fw-semibold`: Font size 5 and semibold weight

#### 2. Navigation Section (Scrollable)

```html

<nav class="flex-grow-1 overflow-auto">
    <ul class="nav nav-pills flex-column px-2 py-3">
        {% block sidebar_nav %}
        <!-- Navigation items -->
        {% endblock sidebar_nav %}
    </ul>
</nav>
```

**Key Classes:**

- `flex-grow-1`: Expands to fill available vertical space between brand and footer
- `overflow-auto`: Scrollable if nav items exceed available height
- `nav nav-pills flex-column`: Bootstrap nav component, pill style, stacked vertically
- `px-2 py-3`: Horizontal padding 0.5rem, vertical padding 1rem

**Navigation Item Pattern:**

```html

<li class="nav-item">
    <a href="{% url 'core:home' %}"
       class="nav-link text-white {% if request.resolver_match.url_name == 'home' %}active{% endif %}">
        <i class="bi bi-house-door me-2"></i>
        {% translate "Home" %}
    </a>
</li>
```

- `nav-link`: Bootstrap nav link styling
- `text-white`: Override default link color for dark sidebar
- **Active State**: Uses Django's `request.resolver_match.url_name` to highlight current page
- `bi-house-door`: Bootstrap Icon with `me-2` spacing

**Section Headers:**

```html

<li class="nav-item mt-3">
    <span class="nav-link text-white-50 small text-uppercase fw-semibold">
        {% translate "Account" %}
    </span>
</li>
```

- `mt-3`: Top margin to separate sections
- `text-white-50`: 50% opacity white for subtle headers
- `small text-uppercase fw-semibold`: Smaller, uppercase, bold styling
- Not clickable - purely organizational

#### 3. Footer Section (User Info or Auth Buttons)

```html

<div class="border-top border-secondary p-3">
    {% if user.is_authenticated %}
    <!-- User dropdown -->
    {% else %}
    <!-- Sign In/Sign Up buttons -->
    {% endif %}
</div>
```

**Authenticated User Dropdown:**

```html

<div class="dropdown">
    <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
       data-bs-toggle="dropdown" aria-expanded="false">
        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
             style="width: 32px; height: 32px;">
            <i class="bi bi-person-fill"></i>
        </div>
        <span class="small">{{ user.email|truncatechars:20 }}</span>
    </a>
    <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
        <!-- Dropdown items -->
    </ul>
</div>
```

- `dropdown`: Bootstrap dropdown component
- `data-bs-toggle="dropdown"`: Activates dropdown JavaScript
- `dropdown-toggle`: Adds caret icon automatically
- `dropdown-menu-dark`: Dark-themed dropdown to match sidebar
- **Avatar Circle**: `rounded-circle` with fixed dimensions, centered icon
- `truncatechars:20`: Django filter to prevent long emails from breaking layout

**Anonymous User Buttons:**

```html

<div class="d-grid gap-2">
    <a href="{% url 'account_login' %}" class="btn btn-outline-light btn-sm">
        {% translate "Sign In" %}
    </a>
    <a href="{{ signup_url_ }}" class="btn btn-light btn-sm">
        {% translate "Sign Up" %}
    </a>
</div>
```

- `d-grid`: CSS Grid layout for stacked buttons
- `gap-2`: Vertical spacing between buttons
- `btn-outline-light`: Outlined button for secondary action
- `btn-light`: Solid button for primary action
- `btn-sm`: Smaller button size

---

## 4) Custom CSS Deep Dive

**Location:** `static/css/main.css`

This file contains critical customizations that make the sidebar layout work. Let's examine each section in detail.

### Section 1: Sidebar Base Styles

```css
#sidebar {
    transition: margin-left 0.3s ease-in-out;
}
```

**Purpose:** Smooth animation when sidebar slides in/out on mobile.

- `transition`: Animates the `margin-left` property
- `0.3s`: Animation duration (300 milliseconds)
- `ease-in-out`: Acceleration curve for smooth motion
- Applied to `margin-left` changes triggered by the mobile collapse

### Section 2: Sidebar Link Styling

```css
#sidebar .nav-link {
    border-radius: 0.375rem;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.25rem;
    transition: all 0.2s ease-in-out;
}
```

**Purpose:** Consistent, modern styling for all sidebar navigation links.

- `border-radius: 0.375rem`: Slightly rounded corners (matches Bootstrap's `rounded` class)
- `padding: 0.5rem 0.75rem`: Vertical 8px, horizontal 12px - comfortable click targets
- `margin-bottom: 0.25rem`: 4px spacing between nav items
- `transition: all 0.2s ease-in-out`: Smooth animation for hover and active states

**Why These Values?**

- **Padding**: Follows WCAG accessibility guidelines for touch targets (minimum 44x44px)
- **Border-radius**: Matches Bootstrap's design language
- **Margin**: Prevents nav items from appearing cramped while maintaining density

### Section 3: Hover States

```css
#sidebar .nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
```

**Purpose:** Subtle visual feedback when hovering over navigation items.

- `rgba(255, 255, 255, 0.1)`: 10% opacity white background
- **Why RGBA?**: Allows semi-transparent backgrounds that work on any underlying color
- Creates a "glass" effect on the dark sidebar
- **UX Principle**: Provides affordance - users know the item is interactive

### Section 4: Active State (Current Page)

```css
#sidebar .nav-link.active {
    background-color: var(--bs-primary);
    color: white !important;
}
```

**Purpose:** Clearly highlight the current page in the navigation.

- `var(--bs-primary)`: Uses Bootstrap's primary color CSS variable
    - Respects theme customization
    - Changes automatically if you modify Bootstrap's `$primary` color
- `color: white !important`: Ensures text is readable on primary background
    - `!important` overrides other color utilities
- **Why This Matters**: Users always know where they are in the application

**Bootstrap CSS Variable System:**

- `--bs-primary`: Primary brand color (default: blue)
- `--bs-secondary`: Secondary color (default: gray)
- `--bs-success`, `--bs-danger`, etc.: Semantic colors
- Defined in Bootstrap's `:root` and can be overridden

### Section 5: Mobile Responsive Behavior

```css
@media (max-width: 991.98px) {
    #sidebar:not(.show) {
        margin-left: -260px;
    }
}
```

**Purpose:** Hide sidebar off-screen on mobile devices.

- `@media (max-width: 991.98px)`: Targets screens smaller than Bootstrap's `lg` breakpoint (992px)
- `#sidebar:not(.show)`: Applies when sidebar doesn't have the `show` class
- `margin-left: -260px`: Slides sidebar completely off-screen to the left
    - Matches sidebar width exactly
    - Combined with `transition` from Section 1 for smooth animation

**How It Works:**

1. **Desktop (≥992px)**: CSS doesn't apply, sidebar is always visible
2. **Mobile (<992px)**:
    - Sidebar hidden by default (`margin-left: -260px`)
    - When toggle button clicked, Bootstrap adds `.show` class
    - CSS transition animates sidebar sliding in
    - Sidebar becomes an overlay (absolute positioning from Bootstrap's collapse)

### Section 6: Nav Pills Active State Override

```css
.nav-pills .nav-link.active {
    background-color: var(--bs-secondary) !important;
    color: #fff;
}

.nav-pills .nav-link {
    color: var(--bs-dark);
}
```

**Purpose:** Global override for nav-pills outside the sidebar (e.g., in content areas).

- **First rule**: Changes active pill background to secondary color instead of Bootstrap's default primary
- **Second rule**: Sets default link color to dark text
- **Sidebar override**: The `#sidebar .nav-link.active` rule (Section 4) takes precedence due to higher specificity

**Specificity Explanation:**

- `#sidebar .nav-link.active` (ID + classes) beats `.nav-pills .nav-link.active` (classes only)
- This allows different active states for sidebar vs. content area navigation

### Section 7: Unpoly Transitions

```css
[up-transition] {
    transition: opacity 0.2s ease-in-out;
}
```

**Purpose:** Smooth fade effect when Unpoly replaces page content.

- `[up-transition]`: Attribute selector for Unpoly-enhanced elements
- `opacity`: Fades content in/out instead of instant replacement
- **User Experience**: Makes partial page updates feel more polished
- **Note**: Unpoly handles the actual opacity changes; this just defines the animation

### Section 8: Card Hover Effects

```css
.card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-2px);
}
```

**Purpose:** Subtle lift effect when hovering over cards (used in `index.html`).

- `transition`: Animates both `transform` and `box-shadow` properties
- `translateY(-2px)`: Moves card up 2 pixels on hover
- **Why It Works**: Creates depth perception - card feels interactive
- **Performance**: `transform` is GPU-accelerated, so animation is smooth

**Note:** The `box-shadow` part of the transition doesn't have a corresponding `:hover` rule in the provided CSS, but
it's included for future use (you could add `box-shadow: ...` to the hover state).

### Section 9: List Group Hover

```css
.list-group-item-action:hover {
    background-color: var(--bs-light);
}
```

**Purpose:** Hover state for actionable list group items (used in Quick Actions section).

- `.list-group-item-action`: Bootstrap class for interactive list items
- `var(--bs-light)`: Bootstrap's light gray color variable
- Provides visual feedback that items are clickable

---

## 5) Top Bar (Header) Structure

**Location:** `templates/base.html` → `<header>`

```html

<header class="bg-white border-bottom shadow-sm">
    <div class="d-flex align-items-center px-3 py-2">
        <!-- Toggle button, page title, action buttons -->
    </div>
</header>
```

### Container Classes:

- `bg-white`: White background (contrasts with light gray content area)
- `border-bottom`: Subtle separator from content
- `shadow-sm`: Small drop shadow for depth
- `d-flex align-items-center`: Horizontal layout, vertically centered
- `px-3 py-2`: Horizontal padding 1rem, vertical padding 0.5rem

### Three Zones:

#### 1. Mobile Toggle Button

```html

<button class="btn btn-link text-dark d-lg-none me-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#sidebar">
    <i class="bi bi-list fs-4"></i>
</button>
```

- `d-lg-none`: Hidden on large screens (≥992px), visible on mobile
- `btn-link`: Unstyled button (no background)
- `data-bs-toggle="collapse"`: Bootstrap collapse JavaScript
- `data-bs-target="#sidebar"`: Targets sidebar by ID
- `bi-list`: Hamburger menu icon

#### 2. Page Title

```html

<div class="flex-grow-1">
    <h1 class="h5 mb-0">
        {% block page_title %}{% block page_title_text %}{% endblock %}{% endblock %}
    </h1>
</div>
```

- `flex-grow-1`: Expands to fill available space
- `h5`: `<h1>` tag styled as h5 for appropriate size
- `mb-0`: Removes default bottom margin
- **Block Hierarchy**: `page_title` contains `page_title_text` for flexibility
    - Override `page_title_text` for simple text
    - Override `page_title` for complex HTML

#### 3. Action Buttons Area

```html

<div class="d-flex align-items-center gap-2">
    {% block topbar_actions %}
    <!-- Add action buttons here in child templates -->
    {% endblock topbar_actions %}
</div>
```

- `gap-2`: Spacing between multiple action buttons
- Empty by default - child templates add buttons as needed
- Example: "New Item", "Export", "Settings" buttons

---

## 6) Main Content Area

**Location:** `templates/base.html` → `<main>`

```html

<main id="content" class="flex-grow-1 bg-light overflow-auto">
    <div class="container-fluid p-4">
        {% block body %}
        {% block content %}
        {% endblock content %}
        {% endblock body %}
        {% block extra_body %}
        {% endblock extra_body %}
    </div>
</main>
```

### Main Element Classes:

- `flex-grow-1`: Expands to fill available vertical space
- `bg-light`: Light gray background (distinguishes from white cards)
- `overflow-auto`: Scrollable if content exceeds viewport height
- `id="content"`: Target for skip link accessibility

### Container:

- `container-fluid`: Full-width container with responsive gutters
- `p-4`: Padding 1.5rem all sides (breathing room around content)

### Block Hierarchy:

1. `{% block body %}`: Outermost block - rarely overridden
2. `{% block content %}`: Primary content block - most templates override this
3. `{% block extra_body %}`: Additional content after main block

**Why This Structure?**

- Flexibility: Most pages just override `content`
- Edge cases: Complex pages can override `body` to remove wrapper
- Consistency: All pages get the same padding by default

---

## 7) Dashboard Content (index.html) Breakdown

**Location:** `templates/core/index.html`

### Welcome Card (Hero Replacement)

```html

<div class="row mb-4">
    <div class="col-12">
        <div class="card border-0 shadow-sm bg-primary bg-gradient text-white">
            <div class="card-body p-4">
                <h2 class="card-title fw-bold mb-2">Django Base Project</h2>
                <p class="card-text mb-0">...</p>
            </div>
        </div>
    </div>
</div>
```

**Key Classes:**

- `row mb-4`: Bootstrap grid row with bottom margin
- `col-12`: Full width column
- `card border-0 shadow-sm`: Card with no border, subtle shadow
- `bg-primary bg-gradient`: Primary color with gradient overlay
- `text-white`: White text for contrast
- `card-body p-4`: Card content with larger padding
- `fw-bold`: Bold font weight for title

**Design Pattern**: Card-based hero is more modern than centered text + image for app dashboards.

### Feature Cards Grid

```html

<div class="row g-4 mb-4">
    <div class="col-12 col-md-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center p-4">
                <div class="bg-primary bg-opacity-10 rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                     style="width: 64px; height: 64px;">
                    <i class="bi bi-shield-check text-primary fs-3"></i>
                </div>
                <h5 class="card-title">Authentication Ready</h5>
                <p class="card-text text-muted small">...</p>
            </div>
        </div>
    </div>
    <!-- 3 more cards -->
</div>
```

**Grid Breakdown:**

- `row g-4`: Grid row with 1.5rem gutters between columns
- `col-12 col-md-6 col-lg-3`: Responsive columns
    - Mobile: 1 column (full width)
    - Tablet: 2 columns (50% each)
    - Desktop: 4 columns (25% each)
- `h-100`: Height 100% - ensures equal card heights in each row

**Icon Circle Pattern:**

- `bg-primary bg-opacity-10`: 10% opacity background (subtle tint)
- `rounded-circle`: Circular shape
- `d-inline-flex align-items-center justify-content-center`: Flexbox centering
- Fixed dimensions (64x64px) for consistency
- `fs-3`: Font size 3 for icon (approximately 1.75rem)

**Why This Works:**

- Icons add visual interest without imagery
- Colored backgrounds reinforce meaning (primary = security, success = performance, etc.)
- `text-muted small`: Subdued description text doesn't compete with titles

### Quick Actions List

```html

<div class="card border-0 shadow-sm">
    <div class="card-header bg-white border-0 pt-4 pb-3">
        <h5 class="mb-0">Quick Start</h5>
    </div>
    <div class="card-body">
        <div class="list-group list-group-flush">
            <a href="..." class="list-group-item list-group-item-action d-flex align-items-center py-3 border-0">
                <i class="bi bi-github fs-4 me-3 text-muted"></i>
                <div>
                    <div class="fw-semibold">View Repository</div>
                    <small class="text-muted">Check out the source code and documentation</small>
                </div>
                <i class="bi bi-chevron-right ms-auto text-muted"></i>
            </a>
        </div>
    </div>
</div>
```

**Card Header:**

- `card-header bg-white border-0`: White background, no bottom border
- `pt-4 pb-3`: Custom padding for spacing

**List Group:**

- `list-group-flush`: Removes borders and rounded corners
- `list-group-item-action`: Makes items interactive (hover state)
- `d-flex align-items-center`: Horizontal layout, vertically centered
- `py-3`: Vertical padding for comfortable click targets

**List Item Structure:**

1. **Icon** (left): `fs-4 me-3` - large icon with right margin
2. **Content** (center): Two lines - title and description
3. **Chevron** (right): `ms-auto` - pushed to far right with auto left margin

**Conditional Content:**

```html
{% if not user.is_authenticated %}
<!-- Show signup link -->
{% else %}
<!-- Show account management link -->
{% endif %}
```

Provides different actions based on authentication status.

---

## 8) Account Management Layout (manage.html)

**Location:** `templates/allauth/layouts/manage.html`

### Simplified Structure

```html
{% extends "allauth/layouts/base.html" %}
{% load allauth %}

{% block body %}
<div id="content">
    {% if messages %}
    <div class="mb-4">
        {% for message in messages %}
        {% element alert level=message.tags dismissible=True %}
        {% slot message %}
        {{ message }}
        {% endslot %}
        {% endelement %}
        {% endfor %}
    </div>
    {% endif %}
    
    <!-- Constrain content width on larger screens -->
    <div class="row">
        <div class="col-12 col-lg-8 col-xl-6">
            {% block content %}{% endblock %}
        </div>
    </div>
</div>
{% endblock %}
```

### What Changed?

**Before**: manage.html had its own sidebar with Email, Password, Social Accounts, etc.

**After**: Sidebar removed - navigation integrated into main sidebar in base.html.

**Why?**

- No redundant navigation
- Maximum width for account forms
- Consistent with modern SaaS UX
- Single source of truth for navigation

### Messages Display

```html
{% element alert level=message.tags dismissible=True %}
```

- Uses allauth's `{% element %}` tag system
- `level=message.tags`: Maps Django message levels to Bootstrap alert variants
    - `success` → `alert-success`
    - `error` → `alert-danger`
    - `info` → `alert-info`
- `dismissible=True`: Adds close button to alerts

### Content Constraint

To prevent `django-allauth` forms for the manage pages (Email, Password, Social Accounts, etc.) from extending across
the full width on large screens (which isn't ideal from a UX/design perspective), this code was added to restrict
content width to a maximum of 800px on larger screens.

Because this code was added directly to the `manage.html` template, it only affects manage pages, not the
`entrance.html`
pages like Login/Signup, which uses a card-centered layout.

```html
<!-- Constrain content width on larger screens -->
<div class="row">
    <div class="col-12 col-lg-8 col-xl-6">
        {% block content %}{% endblock %}
    </div>
</div>
```

---

## 9) Minimal Footer Design

**Location:** `templates/base.html` → `<footer>`

```html

<footer class="bg-white border-top py-2">
    <div class="container-fluid px-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center">
            <small class="text-body-secondary">
                &copy; {% now "Y" %} Django Base. All rights reserved.
            </small>
            <ul class="list-inline mb-0">
                <li class="list-inline-item">
                    <a href="{% url 'core:privacy_policy' %}" class="text-decoration-none text-body-secondary small">
                        {% translate "Privacy" %}
                    </a>
                </li>
                <!-- Terms, Support -->
            </ul>
        </div>
    </div>
</footer>
```

### Design Philosophy

**Minimal by Design**: App-focused layouts don't need large footers. Users are here to work, not browse.

**Key Classes:**

- `bg-white border-top`: White background with top separator
- `py-2`: Minimal vertical padding (0.5rem)
- `d-flex flex-wrap`: Flexbox that wraps on narrow screens
- `justify-content-between`: Space between copyright and links
- `list-inline`: Horizontal list
- `text-body-secondary small`: Subdued, smaller text

**What's Missing (Intentionally):**

- No large CTA section
- No social media icons
- No multi-column layout
- No branding duplication

**Overriding the Footer:**

Child templates can completely replace footer:

```html
{% block footer %}
<footer>
    <!-- Custom footer content -->
</footer>
{% endblock %}
```

Or suppress it entirely:

```html
{% block footer %}{% endblock %}
```

---

## 10) Extending the Templates

### Example 1: Adding a New Sidebar Navigation Item

**Scenario**: You're building a "Projects" feature and want to add it to the sidebar.

**Step 1**: Create a new template that extends base.html and overrides the sidebar:

```html
{% extends "base.html" %}

{% block sidebar_nav %}
{{ block.super }}  {# Include parent content #}

{# Add new Projects section #}
<li class="nav-item mt-3">
        <span class="nav-link text-white-50 small text-uppercase fw-semibold">
            {% translate "Work" %}
        </span>
</li>

<li class="nav-item">
    <a href="{% url 'projects:list' %}"
       class="nav-link text-white {% if 'projects' in request.resolver_match.namespace %}active{% endif %}">
        <i class="bi bi-folder me-2"></i>
        {% translate "Projects" %}
    </a>
</li>

<li class="nav-item">
    <a href="{% url 'tasks:list' %}"
       class="nav-link text-white {% if 'tasks' in request.resolver_match.namespace %}active{% endif %}">
        <i class="bi bi-check2-square me-2"></i>
        {% translate "Tasks" %}
    </a>
</li>
{% endblock sidebar_nav %}
```

**Key Points:**

- `{{ block.super }}`: Includes parent block content (Home, Account sections)
- Active state uses `request.resolver_match.namespace` to highlight all URLs in the "projects" namespace
- Consistent icon pattern: `bi-*` class + `me-2` spacing

**Step 2**: If you want this navigation on ALL pages, modify `base.html` directly instead.

### Example 2: Adding Action Buttons to Top Bar

**Scenario**: Your project detail page needs "Edit" and "Delete" buttons in the top bar.

```html
{% extends "base.html" %}
{% block page_title_text %}{{ project.name }}{% endblock %}

{% block topbar_actions %}
<a href="{% url 'projects:edit' project.pk %}" class="btn btn-sm btn-primary">
    <i class="bi bi-pencil me-1"></i>
    Edit
</a>
<button type="button" class="btn btn-sm btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteModal">
    <i class="bi bi-trash me-1"></i>
    Delete
</button>
{% endblock topbar_actions %}
```

**Result**: Buttons appear in the top-right corner, next to the page title.

### Example 3: Modifying index.html for a New Project

**Scenario**: You're building an inventory management system and want to adapt the dashboard.

**Before (Generic Dashboard):**

- Welcome card with project description
- 4 feature cards
- Quick actions list

**After (Inventory Dashboard):**

```html
{% extends "base.html" %}
{% load static %}
{% block page_title_text %}Inventory Dashboard{% endblock %}

{% block content %}
<!-- Statistics Row -->
<div class="row g-4 mb-4">
    <div class="col-12 col-sm-6 col-lg-3">
        <div class="card border-0 shadow-sm">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <p class="text-muted mb-1 small">Total Items</p>
                        <h3 class="mb-0">{{ total_items }}</h3>
                    </div>
                    <div class="bg-primary bg-opacity-10 rounded-circle p-3">
                        <i class="bi bi-box-seam text-primary fs-4"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-12 col-sm-6 col-lg-3">
        <div class="card border-0 shadow-sm">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <p class="text-muted mb-1 small">Low Stock</p>
                        <h3 class="mb-0 text-danger">{{ low_stock_count }}</h3>
                    </div>
                    <div class="bg-danger bg-opacity-10 rounded-circle p-3">
                        <i class="bi bi-exclamation-triangle text-danger fs-4"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 2 more stat cards -->
</div>

<!-- Recent Activity -->
<div class="row">
    <div class="col-12 col-lg-8">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pt-4 pb-3">
                <h5 class="mb-0">Recent Transactions</h5>
            </div>
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead class="table-light">
                        <tr>
                            <th>Item</th>
                            <th>Type</th>
                            <th>Quantity</th>
                            <th>Date</th>
                        </tr>
                        </thead>
                        <tbody>
                        {% for transaction in recent_transactions %}
                        <tr>
                            <td>{{ transaction.item.name }}</td>
                            <td>
                                        <span class="badge bg-{% if transaction.type == 'in' %}success{% else %}warning{% endif %}">
                                            {{ transaction.get_type_display }}
                                        </span>
                            </td>
                            <td>{{ transaction.quantity }}</td>
                            <td>{{ transaction.created_at|date:"M d, Y" }}</td>
                        </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-12 col-lg-4">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pt-4 pb-3">
                <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body d-grid gap-2">
                <a href="{% url 'inventory:add_item' %}" class="btn btn-primary">
                    <i class="bi bi-plus-circle me-2"></i>
                    Add New Item
                </a>
                <a href="{% url 'inventory:record_transaction' %}" class="btn btn-outline-primary">
                    <i class="bi bi-arrow-left-right me-2"></i>
                    Record Transaction
                </a>
                <a href="{% url 'inventory:generate_report' %}" class="btn btn-outline-secondary">
                    <i class="bi bi-file-earmark-text me-2"></i>
                    Generate Report
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

**What Changed:**

1. **Statistics Cards**: Replaced feature cards with data-driven stat cards
    - Uses same grid system (`row g-4`, responsive columns)
    - Shows real data from database instead of static content
    - Color-coded icons for context (red for warnings, etc.)

2. **Two-Column Layout**:
    - Left: Data table (8 columns on desktop)
    - Right: Action buttons (4 columns on desktop)
    - Stacks vertically on mobile (`col-12`)

3. **Bootstrap Table**:
    - `table-responsive`: Horizontal scroll on narrow screens
    - `table-hover`: Highlight rows on hover
    - `table-light` header: Subtle background for distinction

4. **Action Buttons**:
    - `d-grid gap-2`: Stacked buttons with spacing
    - Icons for visual clarity
    - Primary action (Add) emphasized with `btn-primary`

### Example 4: Adding Collapsible Sidebar Sections

**Scenario**: Your sidebar has grown and you want to collapse the Account section by default.

```html
{% block sidebar_nav %}
<li class="nav-item">
    <a href="{% url 'core:home' %}" class="nav-link text-white">
        <i class="bi bi-house-door me-2"></i>
        {% translate "Home" %}
    </a>
</li>

{% if user.is_authenticated %}
<li class="nav-item mt-3">
    <a class="nav-link text-white d-flex align-items-center justify-content-between"
       data-bs-toggle="collapse"
       href="#accountSubmenu"
       role="button"
       aria-expanded="false"
       aria-controls="accountSubmenu">
                <span>
                    <i class="bi bi-person-circle me-2"></i>
                    {% translate "Account" %}
                </span>
        <i class="bi bi-chevron-down"></i>
    </a>
</li>

<div class="collapse" id="accountSubmenu">
    <ul class="nav nav-pills flex-column ms-3">
        <li class="nav-item">
            <a href="{{ email_url_ }}" class="nav-link text-white-50">
                <i class="bi bi-envelope me-2"></i>
                {% translate "Email" %}
            </a>
        </li>
        <li class="nav-item">
            <a href="{{ change_password_url_ }}" class="nav-link text-white-50">
                <i class="bi bi-key me-2"></i>
                {% translate "Password" %}
            </a>
        </li>
        <!-- Other account links -->
    </ul>
</div>
{% endif %}
{% endblock sidebar_nav %}
```

**Add to main.css:**

```css
/* Rotate chevron when section is expanded */
a[aria-expanded="true"] .bi-chevron-down {
    transform: rotate(180deg);
    transition: transform 0.2s ease-in-out;
}

/* Indent collapsed submenu items */
#accountSubmenu .nav-link {
    font-size: 0.9rem;
    padding: 0.4rem 0.75rem;
}
```

**How It Works:**

- Clicking "Account" toggles the collapse
- Bootstrap adds/removes `.show` class and updates `aria-expanded`
- CSS rotates the chevron icon when expanded
- Submenu items are indented (`ms-3`) and slightly smaller

### Example 5: Adding Breadcrumbs (Optional)

**Scenario**: You want breadcrumbs on specific deep pages (not globally).

```html
{% extends "base.html" %}
{% block page_title_text %}Edit Project Settings{% endblock %}

{% block content %}
<!-- Breadcrumb -->
<nav aria-label="breadcrumb" class="mb-3">
    <ol class="breadcrumb bg-transparent px-0 mb-2">
        <li class="breadcrumb-item"><a href="{% url 'core:home' %}">Home</a></li>
        <li class="breadcrumb-item"><a href="{% url 'projects:list' %}">Projects</a></li>
        <li class="breadcrumb-item"><a href="{% url 'projects:detail' project.pk %}">{{ project.name }}</a></li>
        <li class="breadcrumb-item active" aria-current="page">Settings</li>
    </ol>
</nav>

<!-- Page content -->
<div class="card border-0 shadow-sm">
    <div class="card-body">
        <!-- Settings form -->
    </div>
</div>
{% endblock content %}
```

**Styling:**

- `bg-transparent`: No background (blends with page)
- `px-0`: Removes default horizontal padding
- `mb-2`: Minimal bottom margin

**When to Use Breadcrumbs:**

- ✅ Deep hierarchies (3+ levels)
- ✅ Complex workflows
- ❌ Single-level pages (redundant with sidebar)
- ❌ Every page (adds clutter)

---

## 11) Bootstrap Components Reference

### Components Used in This Layout

#### Collapse (Sidebar Toggle)

```html

<button data-bs-toggle="collapse" data-bs-target="#sidebar">Toggle</button>
<aside id="sidebar" class="collapse collapse-horizontal show">...</aside>
```

- **Docs**: https://getbootstrap.com/docs/5.3/components/collapse/
- **Behavior**: Shows/hides content with animation
- `collapse-horizontal`: Slides left/right instead of up/down
- `show`: Visible by default

#### Dropdown (User Menu)

```html

<div class="dropdown">
    <a data-bs-toggle="dropdown">User</a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item">Profile</a></li>
    </ul>
</div>
```

- **Docs**: https://getbootstrap.com/docs/5.3/components/dropdowns/
- **Options**: `dropdown-menu-dark`, `dropdown-menu-end` (align right)

#### Nav Pills (Sidebar Navigation)

```html

<ul class="nav nav-pills flex-column">
    <li class="nav-item">
        <a class="nav-link active">Link</a>
    </li>
</ul>
```

- **Docs**: https://getbootstrap.com/docs/5.3/components/navs-tabs/
- **Variants**: `nav-tabs`, `nav-underline`

#### Cards

```html

<div class="card border-0 shadow-sm">
    <div class="card-header">Title</div>
    <div class="card-body">Content</div>
    <div class="card-footer">Footer</div>
</div>
```

- **Docs**: https://getbootstrap.com/docs/5.3/components/card/
- **Utilities**: `border-0` (no border), `shadow-sm` (subtle shadow)

#### List Group

```html

<div class="list-group list-group-flush">
    <a class="list-group-item list-group-item-action">Item</a>
</div>
```

- **Docs**: https://getbootstrap.com/docs/5.3/components/list-group/
- `list-group-flush`: Removes borders for card integration

### Utility Classes Quick Reference

**Spacing:**

- `p-{n}`: Padding all sides (0-5, or custom)
- `m-{n}`: Margin all sides
- `px-{n}`, `py-{n}`: Horizontal/vertical padding
- `mt-auto`: Auto top margin (pushes element down in flex container)
- `gap-{n}`: Gap between flex/grid items

**Flexbox:**

- `d-flex`: Enable flexbox
- `flex-column`, `flex-row`: Direction
- `align-items-center`: Vertical centering
- `justify-content-between`: Space between items
- `flex-grow-1`: Expand to fill space
- `flex-shrink-0`: Don't shrink

**Typography:**

- `fs-{1-6}`: Font size (1 = largest)
- `fw-bold`, `fw-semibold`: Font weight
- `small`: Smaller text
- `text-uppercase`: Uppercase text
- `text-muted`: Subdued color
- `text-decoration-none`: Remove underlines

**Colors:**

- `bg-{color}`: Background color
- `text-{color}`: Text color
- `bg-opacity-{n}`: Background opacity (10, 25, 50, 75, 100)
- CSS variables: `var(--bs-primary)`, `var(--bs-light)`, etc.

**Borders:**

- `border`: Add border
- `border-{side}`: Specific side (top, bottom, left, right)
- `border-0`: No border
- `rounded`: Rounded corners
- `rounded-circle`: Circular shape

**Shadows:**

- `shadow-sm`: Small shadow
- `shadow`: Default shadow
- `shadow-lg`: Large shadow

**Display:**

- `d-none`: Hide element
- `d-{breakpoint}-{value}`: Responsive display (e.g., `d-lg-none`)
- `overflow-auto`: Scrollable if content overflows

**Grid:**

- `container-fluid`: Full-width container
- `row`: Grid row
- `col-{n}`: Column (1-12)
- `col-{breakpoint}-{n}`: Responsive column (e.g., `col-md-6`)
- `g-{n}`: Gutter size (spacing between columns)

**Responsive Breakpoints:**

- `sm`: ≥576px (phones, landscape)
- `md`: ≥768px (tablets)
- `lg`: ≥992px (desktops)
- `xl`: ≥1200px (large desktops)
- `xxl`: ≥1400px (extra large)

---

## 12) Accessibility Features

### Keyboard Navigation

- **Skip Link**: `<a class="visually-hidden-focusable" href="#content">` allows keyboard users to jump to main content
- **Tab Order**: Logical flow (sidebar → top bar → content → footer)
- **Focus Indicators**: Browser defaults respected (no `outline: none`)

### ARIA Attributes

- `aria-expanded`: Tracks collapse state for screen readers
- `aria-controls`: Associates toggle buttons with their targets
- `aria-label`: Provides context for icon-only buttons
- `aria-current="page"`: Identifies current page in navigation

### Screen Reader Support

- Semantic HTML: `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`
- Proper heading hierarchy: `<h1>` for page title, `<h2>`-`<h5>` for sections
- Alt text on images: `<img alt="Description">`

---

## 13) Performance Considerations

### CSS

- Bootstrap loaded from CDN (browser caching, parallel downloads)
- Custom CSS is minimal (~50 lines)
- No unused CSS purging needed - Bootstrap is gzipped ~20KB

### JavaScript

- Bootstrap bundle includes only used components
- `defer` attribute on scripts (non-blocking)
- Unpoly adds ~30KB but eliminates full page reloads

### Images

- SVG logo (scalable, small file size)
- Bootstrap Icons (font, cached across pages)
- Lazy loading: `loading="lazy"` on images

### Layout Performance

- Flexbox-based layout (GPU-accelerated)
- CSS transitions on `transform` and `opacity` (hardware-accelerated)
- Minimal reflows (fixed sidebar width, flex-grow content)

---

## 14) Common Customizations

### Change Sidebar Width

**base.html:**

```html

<aside id="sidebar" ... style="width: 280px;">
```

**main.css:**

```css
@media (max-width: 991.98px) {
    #sidebar:not(.show) {
        margin-left: -280px; /* Match new width */
    }
}
```

### Change Color Theme

**Option 1: Bootstrap Variables (Recommended)**

Create `static/css/custom-bootstrap.scss`:

```scss
// Override Bootstrap variables
$primary: #6f42c1; // Purple
$secondary: #6c757d; // Gray
$dark: #1a1a1a; // Darker sidebar

// Import Bootstrap
@import "~bootstrap/scss/bootstrap";
```

Compile with Sass, replace Bootstrap CDN link.

**Option 2: CSS Variables (Quick)**

```css
:root {
    --bs-primary: #6f42c1;
    --bs-primary-rgb: 111, 66, 193;
}
```

### Dark Mode Support

**Add toggle button to top bar:**

```html
{% block topbar_actions %}
<button class="btn btn-sm btn-outline-secondary" id="themeToggle">
    <i class="bi bi-moon-stars"></i>
</button>
{% endblock topbar_actions %}
```

**Add JavaScript:**

```javascript
<script>
    const toggle = document.getElementById('themeToggle');
    const html = document.documentElement;

    toggle.addEventListener('click', () => {
    const current = html.getAttribute('data-bs-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', next);
    localStorage.setItem('theme', next);
});

    // Restore saved theme
    const saved = localStorage.getItem('theme');
    if (saved) html.setAttribute('data-bs-theme', saved);
</script>
```

### Right-Aligned Sidebar

**base.html:**

```html

<body class="d-flex flex-row-reverse">  <!-- Add flex-row-reverse -->
<aside id="sidebar" ...>
```

**main.css:**

```css
@media (max-width: 991.98px) {
    #sidebar:not(.show) {
        margin-right: -260px; /* Changed from margin-left */
    }
}
```

---

## 15) Troubleshooting

### Sidebar Not Hiding on Mobile

**Check:**

1. Is `main.css` loaded after Bootstrap?
2. Does `#sidebar` have `collapse collapse-horizontal show` classes?
3. Is the `@media` query correct in CSS?

**Debug:**

```javascript
// In browser console
console.log(window.innerWidth);  // Check actual breakpoint
```

### Active Nav State Not Working

**Common Issues:**

- URL name doesn't match condition: `{% if request.resolver_match.url_name == 'home' %}`
- Missing `request` context processor in settings.py
- Namespace not included: Use `request.resolver_match.namespace`

**Fix:**

```python
# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',  # Required
        ],
    },
}]
```

### Cards Not Equal Height

**Solution:**
Add `h-100` to cards inside grid columns:

```html

<div class="col-lg-3">
    <div class="card h-100">...</div>
</div>
```

### Dropdown Not Working

**Check:**

1. Is Bootstrap JS loaded?
2. Does button have `data-bs-toggle="dropdown"`?
3. Is dropdown menu a direct sibling of the toggle?

---

## 16) Where to Look Next

### Official Documentation

- **Bootstrap 5.3**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/
- **Unpoly**: https://unpoly.com/
- **Django Templates**: https://docs.djangoproject.com/en/stable/ref/templates/

### Useful Resources

- **Bootstrap Examples**: https://getbootstrap.com/docs/5.3/examples/
- **Flexbox Guide**: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
- **CSS Variables**: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties

---

## Conclusion

This sidebar layout provides a modern, scalable foundation for Django applications. Key takeaways:

- **App-focused**: Designed for productivity, not marketing
- **Extensible**: Easy to add navigation items, action buttons, and custom content
- **Responsive**: Works seamlessly from mobile to desktop
- **Minimal footprint**: Leverages Bootstrap - no heavy frameworks
- **Accessible**: Follows WCAG guidelines for keyboard and screen reader support

Use this template as a starting point and customize freely for your specific use case!

```
```

`