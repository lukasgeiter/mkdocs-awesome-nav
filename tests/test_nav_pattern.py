def test_or_pattern(mkdocs):
    mkdocs.docs(
        """
        bar.md
        foo.md
        .nav.yml
        | nav:
        |   - "@(foo|bar).md"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Bar: bar.md
        - Foo: foo.md
        """
    )


def test_only_directories(mkdocs):
    mkdocs.docs(
        """
        bar.md
        foo/
            bar.md
        .nav.yml
        | nav:
        |   - "*/"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo:
            - Bar: foo/bar.md
        """
    )


def test_only_md_files(mkdocs):
    mkdocs.docs(
        """
        bar.md
        foo/
            bar.md
        .nav.yml
        | nav:
        |   - "*.md"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Bar: bar.md
        """
    )


def test_flatten_everything(mkdocs):
    mkdocs.docs(
        """
        foo.md
        bar/
            foo.md
            bar/
                foo.md
        .nav.yml
        | nav:
        |   - "**"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: bar/bar/foo.md
        - Foo: bar/foo.md
        - Foo: foo.md
        """
    )


def test_deep(mkdocs):
    mkdocs.docs(
        """
        foo.md
        bar/
            foo.md
            bar/
                foo.md
        .nav.yml
        | nav:
        |   - "bar/**/foo.md"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: bar/bar/foo.md
        - Foo: bar/foo.md
        """
    )


def test_scoped_to_directory(mkdocs):
    mkdocs.docs(
        """
        foo/
            foo.md
            bar/
                foo.md
            .nav.yml
            | nav:
            |   - "**"
        bar.md
        .nav.yml
        | nav:
        |   - foo
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo:
            - Foo: foo/bar/foo.md
            - Foo: foo/foo.md
        """
    )


def test_overlapping(mkdocs):
    mkdocs.docs(
        """
        foo.md
        foobar.md
        bar.md
        barfoo.md
        .nav.yml
        | nav:
        |   - Foo:
        |       - "*foo*"
        |   - Bar:
        |       - "*bar*"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo:
            - Barfoo: barfoo.md
            - Foo: foo.md
            - Foobar: foobar.md
        - Bar:
            - Bar: bar.md
        """
    )


def test_overlapping_specificity_is_irrelevant(mkdocs):
    mkdocs.docs(
        """
        foo.md
        foobar.md
        bar.md
        barfoo.md
        .nav.yml
        | nav:
        |   - Foo:
        |       - "*"
        |   - Bar:
        |       - "*bar.md"
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo:
            - Bar: bar.md
            - Barfoo: barfoo.md
            - Foo: foo.md
            - Foobar: foobar.md
        - Bar: []
        """
    )


def test_no_matches(mkdocs, logs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | nav:
        |   - foo.md
        |   - bar_*.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )
    assert logs.from_plugin == [
        logs.warning("awesome-nav: The nav item 'bar_*.md' doesn't match any files or directories [.nav.yml]")
    ]


def test_no_matches_override_level(mkdocs, logs):
    mkdocs.files(
        """
        docs/
            foo.md
            .nav.yml
            | nav:
            |   - foo.md
            |   - bar_*.md
        mkdocs.yml
        | site_name: Test
        | plugins:
        |   - awesome-nav:
        |       logs:
        |         no_matches: error
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )
    assert logs.from_plugin == [
        logs.error("awesome-nav: The nav item 'bar_*.md' doesn't match any files or directories [.nav.yml]")
    ]


def test_no_matches_nested(mkdocs, logs):
    mkdocs.docs(
        """
        foo/
            foo.md
            .nav.yml
            | nav:
            |   - foo.md
            |   - bar_*.md
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo:
            - Foo: foo/foo.md
        """
    )
    assert logs.from_plugin == [
        logs.warning("awesome-nav: The nav item 'bar_*.md' doesn't match any files or directories [foo/.nav.yml]")
    ]
