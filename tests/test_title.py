def test_page_default(mkdocs):
    mkdocs.docs(
        """
        foo.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )


def test_page_override(mkdocs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | nav:
        |   - Title: foo.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - Title: foo.md
        """
    )


def test_directory_default(mkdocs):
    mkdocs.docs(
        """
        foo-bar/
            foo.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo bar:
            - Foo: foo-bar/foo.md
        """
    )


def test_directory_override_from_inside(mkdocs):
    mkdocs.docs(
        """
        foo/
            bar.md
            .nav.yml
            | title: Title
        """
    )
    mkdocs.build().assert_nav(
        """
        - Title:
            - Bar: foo/bar.md
        """
    )


def test_directory_override_from_outside(mkdocs):
    mkdocs.docs(
        """
        foo/
            bar.md
        .nav.yml
        | nav:
        |   - Title: foo
        """
    )
    mkdocs.build().assert_nav(
        """
        - Title:
            - Bar: foo/bar.md
        """
    )


def test_directory_override_from_inside_and_outside(mkdocs):
    mkdocs.docs(
        """
        foo/
            bar.md
            .nav.yml
            | title: Inside Title
        .nav.yml
        | nav:
        |   - Outside Title: foo
        """
    )
    mkdocs.build().assert_nav(
        """
        - Outside Title:
            - Bar: foo/bar.md
        """
    )


def test_directory_override_root(mkdocs, logs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | title: Title
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )
    assert logs.from_plugin == [logs.warning("awesome-nav: 'title' option has no effect at the top level [.nav.yml]")]


def test_directory_override_root_log_level(mkdocs, logs):
    mkdocs.files(
        """
        docs/
            foo.md
            .nav.yml
            | title: Title
        mkdocs.yml
        | site_name: Test
        | plugins:
        |   - awesome-nav:
        |       logs:
        |         root_title: info
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )
    assert logs.from_plugin == [logs.info("awesome-nav: 'title' option has no effect at the top level [.nav.yml]")]


def test_preserve_directory_names(mkdocs):
    mkdocs.docs(
        """
        foo-bar/
            foo.md
        .nav.yml
        | preserve_directory_names: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - foo-bar:
          - Foo: foo-bar/foo.md
        """
    )


def test_preserve_directory_names_inheritance(mkdocs):
    mkdocs.docs(
        """
        foo-bar/
            foo-bar/
                foo-bar/
                    foo-bar/
                        foo.md
                    .nav.yml
                    | preserve_directory_names: false
        .nav.yml
        | preserve_directory_names: true
        """
    )
    mkdocs.build().assert_nav(
        """
        - foo-bar:
          - foo-bar:
            - Foo bar:
              - Foo bar:
                - Foo: foo-bar/foo-bar/foo-bar/foo-bar/foo.md
        """
    )
