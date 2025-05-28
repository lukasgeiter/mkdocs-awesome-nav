# Reference

## Plugin Options

```yaml
plugins:
  - awesome-nav:
      filename: awesome_nav.yml #(1)!
      logs: #(2)!
        nav_override: warning
        root_title: warning
        root_hide: warning
        no_matches: warning
```

1. Name of your `awesome-nav` config files. [Read more :material-arrow-right:](features/options.md#filename)
   <span class="reference-type">`str`</span>
   <span class="reference-default">`.nav.yml`</span>
2. Override the log level of certain messages. [Read more :material-arrow-right:](features/options.md#log-level)
   <span class="reference-type">`info` | `warning` | `error`</span>

## .nav.yml

```yaml
title: Lorem Ipsum #(1)!

preserve_directory_names: true #(2)!

hide: true #(3)!

flatten_single_child_sections: true #(4)!

ignore: "*.hidden.md" #(5)!

sort:
  direction: asc #(6)!
  type: natural #(7)!
  by: filename #(8)!
  sections: last #(9)!
  ignore_case: true #(10)!

nav: #(11)!
  - getting-started.md
  - guides
  - More Resources:
    - "*"
    - Website: https://lukasgeiter.github.io/mkdocs-awesome-nav

append_unmatched: true #(12)!

use_index_title: true #(13)!
```

1. Custom title for this directory. [Read more :material-arrow-right:](features/titles.md#custom-section-title)
   <span class="reference-type">`str`</span>
2. Disable formatting of generated directory titles. [Read more :material-arrow-right:](features/titles.md#preserve-directory-names)
   <span class="reference-type">`bool`</span>
   <span class="reference-default">`false`</span>
3. Hide this directory in the navigation. [Read more :material-arrow-right:](features/hiding.md)
   <span class="reference-type">`bool`</span>
   <span class="reference-default">`false`</span>
4. For sections with a single child, show the child instead of the section. [Read more :material-arrow-right:](features/flattening.md#single-child)
   <span class="reference-type">`bool`</span>
   <span class="reference-default">`false`</span>
5. Hide everything that matches this glob pattern. [Read more :material-arrow-right:](features/hiding.md#ignore-patterns)
   <span class="reference-type">`str` | `list[str]`</span>
6. Sorting direction (ascending or descending). [Read more :material-arrow-right:](features/sorting.md#sort-direction)
   <span class="reference-type">`asc` | `desc`</span>
   <span class="reference-default">`asc`</span>
7. How numbers are treated when sorting. [Read more :material-arrow-right:](features/sorting.md#sort-type)
   <span class="reference-type">`natural` | `alphabetical`</span>
   <span class="reference-default">`natural`</span>
8. Attribute that is used for sorting. [Read more :material-arrow-right:](features/sorting.md#sort-by)
   <span class="reference-type">`path` | `filename` | `title`</span>
   <span class="reference-default">`path`</span>
9. How sections are treated when sorting. [Read more :material-arrow-right:](features/sorting.md#sort-sections)
   <span class="reference-type">`first` | `last` | `mixed`</span>
   <span class="reference-default">`last`</span>
10. Enable case-insensitive sorting. [Read more :material-arrow-right:](features/sorting.md#sort-ignore-case)
   <span class="reference-type">`bool`</span>
   <span class="reference-default">`false`</span>
11. Custom navigation for this directory. [Read more :material-arrow-right:](features/nav.md)
12. Add unmatched files at the end. [Read more :material-arrow-right:](features/nav.md#unmatched-files)
13. Use the title from `index.md` as the directory navigation title. [Read more :material-arrow-right:](features/titles.md#index-md-title)
   <span class="reference-type">`bool`</span>
   <span class="reference-default">`false`</span>
