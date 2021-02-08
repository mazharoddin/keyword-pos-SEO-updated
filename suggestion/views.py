from django.shortcuts import render
from django.http import HttpResponse
from .froms import SuggestionForm
from .suggestion_service import get_suggestion
from .models import SeoProject, KeywordSuggestion


def process_keyword(pro):
    keyword_str = pro.keywords
    if len(keyword_str.strip()) != 0:
        keyword_list = keyword_str.split(",")
        for keyword in keyword_list:
            suggested_keyword = get_suggestion(keyword)
            print(suggested_keyword)
            suggestion = ",".join(suggested_keyword)
            KeywordSuggestion.objects.create(
                keyword=keyword, project=pro, suggestion=suggestion
            )


def suggestion_service(request, *args, **kwargs):
    if request.POST:
        form = SuggestionForm(request.POST)
        if form.is_valid():
            project_id = request.POST.get("project")
            project = SeoProject.objects.get(id=project_id)
            process_keyword(project)
            return HttpResponse("ok..")
    else:
        form = SuggestionForm()
        return render(request, "suggestion/key-suggestion.html", {"form": form})

