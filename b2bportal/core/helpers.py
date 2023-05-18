# from cgitb import html
# from inspect import Parameter
# from io import BytesIO
# from re import template
# from urllib import response
# from webbrowser import get
# from django.template.loader import get_template
# import xhtml2pdf.pisa as pisa
# import uuid
# from django.conf import settings


# def save_pdf():
#     template=get_template("b2bportal/success.html")
#     html=template.render(Parameter)
#     response=BytesIO()
#     pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
#     file_name=uuid.uuid4()


#     try:
#         with open(str(settings.BASE_DIR)+f'/public/static/{file_name}.pdf','wb+') as output:
#             pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')),output)

#     except Exception as e:
#         print(e)   
#     if pdf.err:
#         return '',False
#     return file_name,True             


