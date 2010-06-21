#!/usr/bin/env python

from docutils.parsers.rst import Parser, directives
from docutils.utils import new_document


def rstdoc_from_string(rst):
    parser = Parser()
    document = new_document("string")
    document.settings.tab_width = 4
    document.settings.pep_references = 1
    document.settings.rfc_references = 1
    parser.parse(rst, document)
    return document



if __name__ == "__main__":
    import sys
    from docutils.parsers.rst import directives
    from docutils.core import publish_from_doctree
    import text
    import field

    def show_help():
        print "Usage:"
        print "   %s create <definition-file> <html|text>" % sys.argv[0]
        print "   %s validate <definition-file> <input-file>" % sys.argv[0]
        raise SystemExit()

    field.register_directive() # register .. field:: with rst

    if len(sys.argv) != 4:
        show_help()
    action = sys.argv[1]
    definition_file = sys.argv[2]
    rst = open(definition_file, 'rb').read()
    document = rstdoc_from_string(rst)

    if action == 'create':
        fmt = sys.argv[3]
        if fmt == 'html':
            p = publish_from_doctree(document, writer=SchemaHTMLWriter())
            print p
        elif fmt == 'text':
            print text.examiner_format(rst)
        else:
            show_help()

    elif action == 'validate':
        input_file = sys.argv[3]
        input = open(input_file, 'rb').read()
        input = text.strip_messages(input)
        fields = field.extract_fields(document)
        ok, output = text.validate_input(input, fields)
        open(input_file, 'wb').write(output)
        print output
    else:
        show_help()
