from django.shortcuts import render

from peptidefeatures.features import compute_features

def overview(request):
    #features = compute_features()
    text = "This is for testing"
    return render(request, "overview.html", {"text": text})