# Wagtail Draftail Anchors

Adds the ability to add and edit anchors in the Draftail rich text editor, as well as automatically adding
(slug-form) anchor ids to all headings.

## Installation

Add `'wagtail_draftail_anchors'` to `INSTALLED_APPS` below `wagtail.admin`.

Add `'anchor-identifier'` to the features of any rich text field where you have overridden the default feature list.