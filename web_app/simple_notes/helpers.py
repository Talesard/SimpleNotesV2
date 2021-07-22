import re

from jinja2 import evalcontextfilter, Markup

from simple_notes import app


@app.template_filter()
@evalcontextfilter
def linebreaks(_eval_ctx, value):
    # https://gist.github.com/cemk/1324543
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.template_filter()
@evalcontextfilter
def linebreaksbr(_eval_ctx, value):
    # https://gist.github.com/cemk/1324543
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br/>') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)
