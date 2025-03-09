from django.shortcuts import render

from contact.forms import ContactForm

def create(request):
    #     print(request.method)
    #     print(request.POST.get('first_name'))
    #     print(request.POST.get('last_name'))
    #     print()
    if request.method == 'POST':
        context = {
            'form': ContactForm(request.POST)
        }
    
        return render(
            request,
            'contact/create.html',
            context,
        )
    context = {
        'form': ContactForm()
    }

    return render(
        request,
        'contact/create.html',
        context,
    )