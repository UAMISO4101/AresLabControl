from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def enviar_correo(asunto, correo_from, correo_to, template_txt, template_html = '', contexto = ''):
    try:
        plaintext = get_template(template_txt)

        d = Context(contexto)
        text_content = plaintext.render(d)

        msg = EmailMultiAlternatives(asunto, text_content, correo_from, correo_to)

        if template_html != '':
            htmly = get_template(template_html)
            html_content = htmly.render(d)
            msg.attach_alternative(html_content, "text/html")

        return msg.send()

    except Exception as e:
        print (e.message)
