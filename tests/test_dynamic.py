def test_dynamic(mkdocs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | nav:
        |   {% if true %}- foo.md{% endif %}
        |   {% if false %}- boo.md{% endif %}
        """
    )
    mkdocs.build().assert_nav(
        """
        - Foo: foo.md
        """
    )

def test_dynamic_title(mkdocs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | nav:
        |   - {{ config.site_name }}: foo.md
        """
    )
    mkdocs.build(site_name="My Title").assert_nav(
        """
        - My Title: foo.md
        """
    )

def test_dynamic_ifelse(mkdocs):
    mkdocs.docs(
        """
        foo.md
        .nav.yml
        | nav:
        | {% if config.extra.doc_type_a %}
        |   - Worked: foo.md
        | {% else %}
        |   - Did not work: foo.md
        | {% endif %}
        """
    )
    mkdocs.build(extra=dict(doc_type_a=True)).assert_nav(
        """
        - Worked: foo.md
        """
    )

def test_dynamic_loop(mkdocs):
    mkdocs.docs(
        """
        {% for k in config.extra.elements.keys() %}
        {{ k }}
        {% endfor %}
        .nav.yml
        | nav:
        | {% for k,v in config.extra.elements.items() %}
        |   - {{ v }}: {{ k }}
        | {% endfor %}
        """
    )
    mkdocs.build(extra=dict(elements={
        "foo.md": "Foo title",
        "boo.md": "Boo title",
    })).assert_nav(
        """
        - Foo title: foo.md
        - Boo title: boo.md
        """
    )
