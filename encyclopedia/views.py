from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util

class NewPageForm(forms.Form):
    page = forms.CharField(label="New Page", widget=forms.Textarea)
    pagename = forms.CharField(label="Name")

class EditPageForm(forms.Form):
    page = forms.CharField(label="Edit Page", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    q = request.GET.get('q')#.strip()
    if q in util.list_entries():
        return redirect("entry", q)
    return render(request, "encyclopedia/search.html", {
        "results": util.search(q),
        "query": q
    })

def entry(request, name):
    html = markdown2.markdown_path(f"entries/{name}.md")
    return render(request, "encyclopedia/entry.html", {
        "title": name,
        "body": html
    })

def randompage(request):
    name = random.choice(util.list_entries())
    return redirect("entry", name=name)

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            page = form.cleaned_data["page"]
            name = form.cleaned_data["pagename"]
            util.save_entry(name, page)
            return HttpResponseRedirect(reverse("entry", args=[name])) 
        else:
            return render(request, "encyclopedia/newpage.html",{
                "form": form
            })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def editpage(request, name):
    default_data = {
        "page": util.get_entry(name)
    }
    if request.method == "POST":
        form = EditPageForm(request.POST)

        if form.is_valid():
            page = form.cleaned_data["page"]
            util.save_entry(name, page)
            return HttpResponseRedirect(reverse("entry", args=[name]))
        else:
            return render(request, "encyclopedia/editpage.html",{
                "title": name,
                "form": form
            })
    return render(request, "encyclopedia/editpage.html", {
        "title": name,
        "form": EditPageForm(default_data)
    })