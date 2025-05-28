# Section Titles

## Custom Section Title

Set a custom section title for a directory:

<div class="awesome-example" markdown>
```yaml title=".nav.yml"
title: API Endpoints
```

```title="File Structure"
docs/
└─ api/
   ├─ .nav.yml
   ├─ apps.md
   └─ users.md
```

- API Endpoints
    - Apps
    - Users
</div>

!!! info "Title from `nav`"
    Adding a title to the [directory in `nav`](nav.md#directories) overrides this custom title.

## Preserve Directory Names

Just like MkDocs, `awesome-nav` automatically transforms directory names into nicely formatted titles.  
Enable `preserve_directory_names` to use the exact directory name as title:

/// tab | `true`
<div class="awesome-example" markdown>
```yaml title=".nav.yml"
preserve_directory_names: true
```

```title="File Structure"
docs/
└─ awesome-nav
   ├─ .nav.yml
   ├─ getting-started.md
   └─ support.md
```

- awesome-nav
    - Getting started
    - Support
</div>
///

/// tab | `false` (default)
<div class="awesome-example" markdown>
```yaml title=".nav.yml"
preserve_directory_names: false
```

```title="File Structure"
docs/
└─ awesome-nav
   ├─ .nav.yml
   ├─ getting-started.md
   └─ support.md
```

- Awesome nav
    - Getting started
    - Support
</div>
///

??? tip "Child directories inherit this setting"
    `preserve_directory_names` applies to all child directories as well, unless it's overridden by a `.nav.yml` there.

## Index.md Title

To use the title from an `index.md` file as the directory navigation title:

``` tab | `true`
<div class="awesome-example" markdown>
```yaml title=".nav.yml"
use_index_title: true
```

```yaml title="user-guide/index.md"
---
title: User Guide Documentation
---
# User Guide

Welcome to the user guide!
```

```title="File Structure"
docs/
└─ user-guide/
   ├─ .nav.yml
   ├─ index.md
   └─ getting-started.md
```

- User Guide Documentation
    - Getting started
</div>
///

/// tab | `false` (default)
<div class="awesome-example" markdown>
```yaml title=".nav.yml"
use_index_title: false
```

```yaml title="user-guide/index.md"
---
title: User Guide Documentation
---
# User Guide

Welcome to the user guide!
```

```title="File Structure"
docs/
└─ user-guide/
   ├─ .nav.yml
   ├─ index.md
   └─ getting-started.md
```

- User guide
    - Getting started
</div>
///

!!! info "Title extraction priority"
    The plugin looks for a `title` field in the frontmatter metadata of `index.md` first, then it falls back to the default directory name formatting.

??? tip "Child directories inherit this setting"
    `use_index_title` applies to all child directories as well, unless it's overridden by a `.nav.yml` there.

??? tip "Interaction with other title settings"
    - **Custom title**: A `title` set in `.nav.yml` always takes precedence over `use_index_title`
    - **External title**: A title specified in the parent directory's `nav` configuration takes precedence
    - **Preserve directory names**: When `preserve_directory_names: true` is set, it takes precedence over `use_index_title`
