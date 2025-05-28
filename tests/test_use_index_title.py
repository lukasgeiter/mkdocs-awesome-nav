def test_use_index_title_disabled_by_default(mkdocs):
    """Test that index.md title is not used when the feature is disabled (default)."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            another-page.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - User guide:
            - User Guide Documentation: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )


def test_use_index_title_enabled_via_local_config(mkdocs):
    """Test that index.md title is used when enabled via local .nav.yml configuration."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            another-page.md
            .nav.yml
            | use_index_title: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - User Guide Documentation:
            - User Guide Documentation: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )


def test_use_index_title_explicit_title_override(mkdocs):
    """Test that explicitly set title overrides index.md title."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            another-page.md
            .nav.yml
            | title: Custom Title
            | use_index_title: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - Custom Title:
            - User Guide Documentation: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )


def test_use_index_title_external_override(mkdocs):
    """Test that externally specified title overrides index.md title."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            another-page.md
            .nav.yml
            | use_index_title: true
        .nav.yml
        | nav:
        |   - External Title: user-guide
        """
    )
    mkdocs.build().assert_nav(
        """
        - External Title:
            - User Guide Documentation: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )


def test_use_index_title_no_metadata(mkdocs):
    """Test fallback to directory name when index.md has no title metadata."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | # User Guide
            | 
            | This is content without frontmatter title.
            another-page.md
            .nav.yml
            | use_index_title: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - User guide:
            - User Guide: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )


def test_use_index_title_inheritance(mkdocs):
    """Test that use_index_title setting is inherited from parent configs."""
    mkdocs.docs(
        """
        user-guide/
            basics/
                index.md
                | ---
                | title: Basic Concepts
                | ---
                | # Basics
                getting-started.md
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            .nav.yml
            | use_index_title: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - User Guide Documentation:
            - User Guide Documentation: user-guide/index.md
            - Basic Concepts:
                - Basic Concepts: user-guide/basics/index.md
                - Getting started: user-guide/basics/getting-started.md
        """
    )


def test_use_index_title_local_override_inheritance(mkdocs):
    """Test that local config can override inherited use_index_title setting."""
    mkdocs.docs(
        """
        user-guide/
            basics/
                index.md
                | ---
                | title: Basic Concepts
                | ---
                | # Basics
                getting-started.md
                .nav.yml
                | use_index_title: false
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            .nav.yml
            | use_index_title: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - User Guide Documentation:
            - User Guide Documentation: user-guide/index.md
            - Basics:
                - Basic Concepts: user-guide/basics/index.md
                - Getting started: user-guide/basics/getting-started.md
        """
    )


def test_use_index_title_with_preserve_directory_names(mkdocs):
    """Test interaction with preserve_directory_names setting."""
    mkdocs.docs(
        """
        user-guide/
            index.md
            | ---
            | title: User Guide Documentation
            | ---
            | # User Guide
            another-page.md
            .nav.yml
            | use_index_title: true
            | preserve_directory_names: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - user-guide:
            - User Guide Documentation: user-guide/index.md
            - Another page: user-guide/another-page.md
        """
    )
