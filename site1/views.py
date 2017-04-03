import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template, Context

from books.models import Book
from site1.forms import ContactForm


def hello(request):
    return HttpResponse("Hello world")


def current_datetime(request):
    now = datetime.datetime.now()
    html = "Right now is {}".format(now)
    return render(request,
                  'current_datetime.html',
                  {'current_date': now})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError as err:
        raise Http404(err)

    now = datetime.datetime.now()
    then = datetime.timedelta(hours=offset)
    t = Template("<html>"
                 "<body>"
                 "<p> It is now {{ current_date }}. </p>"
                 "It's going to be {{future}} soon"
                 "</body>"
                 "</html>")
    html = t.render(Context({'current_date': now, 'future': then}))
    # html = "In {} hours, it will be {}".format(offset, then)
    return HttpResponse(html)


def search(request):
    error = None
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = "Please add a query"
        elif len(q) > 20:
            error = "query is too long"
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, "search_result.html",
                          {
                              'query': q,
                              'books': books

                          })

    return render(request, 'search_form.html', {'error': error})

    # return render(request, 'search_form.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            return HttpResponseRedirect('/contact/thanks')
    else:
        form = ContactForm(
            initial={'subject': 'I Love your site!'}
        )
    return render(request, 'contact_form.html', {'form': form})


def contact_thanks(request):
    return HttpResponse("Thank you for contacting us")


def get_meta(request):
    items = request.META.items()

    def html_row(k, v):
        return "<tr><td>{}</td><td>{}</td><tr>".format(k, v)

    rows = [html_row(k, v) for k, v in items]
    rows_text = '\n'.join(rows)
    table_text = "<table>{}</table>".format(rows_text)
    return HttpResponse(table_text)
