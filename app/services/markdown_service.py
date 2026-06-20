import bleach
import markdown


def render_markdown_safe(content: str) -> str:
    raw_html = markdown.markdown(
        content,
        extensions=["fenced_code", "tables"],
    )

    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        {
            "p",
            "pre",
            "code",
            "hr",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "blockquote",
            "span",
        }
    )

    allowed_attrs = {
        **bleach.sanitizer.ALLOWED_ATTRIBUTES,
        "a": ["href", "title", "target", "rel"],
        "code": ["class"],
        "span": ["class"],
    }

    return bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=["http", "https", "mailto"],
        strip=True,
    )