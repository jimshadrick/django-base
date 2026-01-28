# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres
to [Semantic Versioning](https://semver.org/).

## Unreleased

### Added
- 

### Changed
- 

### Fixed

-

## [0.7.0] - 2026-01-28

### Added

- Add account deletion functionality and user profile enhancements with a confirmation modal.

### Changed

- Changed layout to modern sidebar navigation with compact top bar and card-based content.
- Improved styling in the user profile form and related templates.
- Updated alert.html for more robust handling and styling of messages using Bootstrap.

### Fixed

- Duplicate messages/alerts - moved allauth message rendering to base.html.

## [0.6.0] - 2026-01-17

### Added

- Add comprehensive unit tests for `CustomUser` model, authentication, registration, and email functionality.
- Add Unpoly CDN with Bootstrap 5 integration.

### Changed

- Upgrade to Django 6.0.1 and update related dependencies.
- Simplify base.html by removing debug-specific Bootstrap links, adding Unpoly support, and standardizing to CDN
  resources. Removed unused local Bootstrap files.

## [0.5.1] - 2025-11-30

### Added

- Add `CHANGELOG.md` file.
- Add authentication and session settings to `settings.py` for improved security and user experience.
- Implement environment variable validation, parameterized post_deploy.sh script, updated documentati on.
- Add symlink creation for `.env.prod` in deployment script
- Set `DJANGO_ENV` to production in post_deploy.sh script to use `.env.prod` and give `.env.prod` per missions to deploy
  user in setup_configs.sh.
- Switch to `.env.prod` handling and dynamic environment loading.
- Documented Bootstrap usage in new guide.

### Changed

- Update `manage.html` and `base.html` for layout enhancements.
- Refine templates with updated Bootstrap classes and improved accessibility.
- Replace class-based views with function-based views in `core`.
- Refine templates with updated Bootstrap classes and improved accessibility.

### Fixed

- Modified manage.html and base.html templates to correct layout issues (correct alignment with the sidebar + main
  content).
- Fixed repo URL in deployment script.
- Removed 'navbar-light' (deprecated now this is the default).
- Fixed the issue with background color when calling entrance.html and manage.html to use the same bg-light background
  as the main content.

## [0.4.0] - 2025-04-23

### Added

- Add favicon
- Add email templates for account security notifications
- Customized email confirmation template for user registration
- Enhance the email templates with header, footer, and styling updates
- Add password reset email templates and configuration

### Changed

- Update navbar styling and button roles
- Remove Bootstrap Icons and adjust navigation links
- Update Nginx static files path in setup script

## [0.3.0] - 2025-04-28

### Added

- Add Terms and Conditions and Privacy Policy pages
- Add empty footer_cta block to suppress Call to Action
- Add service restarts to the deployment script.
- Add Bootstrap Icons to navigation bar links.
- Refactor the HTML structure for navigation. Updated the index.html text about project template for bett er readability
  and
  consistency.

### Changed

- Refactor footer layout and improve template structure
- Update navbar and add footer content.
- Update templates, styles, and routing for improved layout
- Update templates and styles for improved UI consistency
- Update UI styling, add logo and hero section, and improve nav links

## [0.2.0] - 2025-04-23

### Added

- Configuration setup and deployment scripts for Digital Ocean VPS.

## [0.1.0] - 2025-04-12 (beta)

### Added

- Project configuration, core models, user account, and templates.
- Replaced AppConfig with command for initializing site and updated deployment script.
- Added anymail and site enhancements.

[Unreleased]:

https://github.com/jimshadrick/django-base