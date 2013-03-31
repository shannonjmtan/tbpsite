from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def poker_tournament(request):
    return render(request, 'poker_tournament.html')

def rube_goldberg(request):
    return render(request, 'rube_goldberg.html')

def requirements(request):
    return render(request, 'requirements.html')

def tutoring(request):
    return render(request, 'tutoring.html')

def awards(request):
    return render(request, 'awards.html')

def officers(request):
    return render(request, 'officers.html')

def faculty(request):
    return render(request, 'faculty.html')

def contact(request):
    return render(request, 'contact.html')

def eligibility_list(request):
    return render(request, 'eligibility_list.html')

#def candidates(request):
    #return render(request, 'candidates.html')

#def distinguishedactive(request):
    #return render(request, 'distinguishedactive.html')

def houses(request):
    return render(request, 'houses.html')
