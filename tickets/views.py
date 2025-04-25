from django.shortcuts import render
from django.http import HttpResponse
from . models import movie,ticket
from datetime import datetime
# Create your views here.
def index (requests):
    movies = movie.objects.all()
    return render(requests,'index.html',{'movies':movies})
def bookt(request):
    if request.method == 'GET':
        movies = movie.objects.all()
        return render(request, 'index.html', {'movies': movies})
    
    elif request.method == 'POST':
        # Handle form submission
        try:
            movie1 = request.POST['movie']
            booking = int(request.POST.get('booking', 0))
            nos = int(request.POST.get('nos', 0))
            username = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            if not all([movie1, username, phone]):
                return render(request, 'error.html', 
                           {'error': 'All fields are required'}, 
                           status=400)
                
            if nos <= 0:
                return render(request, 'error.html',
                           {'error': 'Number of seats must be positive'},
                           status=400)
                
            booking = booking - nos
            if booking < 0:
                return render(request, 'error.html',
                           {'error': 'Not enough available seats'},
                           status=400)
                
            book_time = datetime.now()
            ticket1 = ticket.objects.create(
                movie=movie1, 
                book_time=book_time,
                user=username,
                phone=phone,
                nos=nos
            )
            movie.objects.filter(name=movie1).update(bookings=booking)
            
            return render(request, 'booked.html', {'obj': ticket1})
            
        except (ValueError, KeyError) as e:
            return render(request, 'error.html',
                        {'error': f'Invalid input: {str(e)}'},
                        status=400)
def delt(requests):
    ticketid=requests.GET['id']
    movie2=requests.GET['movienm']
    obj = movie.objects.get(name=movie2)
    booking=int(obj.bookings)
    nos=int(requests.GET['nos'])
    username=requests.GET['username']
    phone=requests.GET['phone']
    book=booking+nos
    objt=ticket.objects.get(id=ticketid,user=username,phone=phone)
    print(objt.nos)
    left=objt.nos-nos
    if(left>0):
        movie.objects.filter(name=movie2).update(bookings=book)
        ticket.objects.filter(id=ticketid,user=username,phone=phone).update(nos=left)
    else :
        ticket.objects.filter(id=ticketid,user=username,phone=phone).delete()
    return render(requests,'deleted.html')

def delete(requests):
    return render(requests,'delete.html')

def updatetime(requests):
    return render(requests,'updateticket.html')

def viewticket(requests):
    return render(requests,'viewticket.html')

def details(requests):
    return render(requests,'userdetails.html')
def updatetimefn(request):
    if request.method == 'GET':
        tid = request.GET.get('tcid')
        if not tid:
            return HttpResponse("Ticket ID is required", status=400)
            
        try:
            tid = int(tid)
            timing_start = request.GET.get('ts')
            timing_end = request.GET.get('te')
            
            if not all([timing_start, timing_end]):
                return HttpResponse("Both start and end times are required", status=400)
                
            movie.objects.filter(id=tid).update(
                time_start=timing_start,
                time_end=timing_end
            )
            return render(request, 'updated.html')
            
        except ValueError:
            return HttpResponse("Invalid ID or time format", status=400)
def viewticketfn(request):
    timing_start = request.GET.get('ts')
    if not timing_start:
        return HttpResponse("Start time is required", status=400)
    
    try:
        obj = movie.objects.get(time_start=timing_start)
        tts = ticket.objects.filter(movie=obj.name)
        return render(request, 'viewticketdisplay.html', {'obj': tts})
    except movie.DoesNotExist:
        return HttpResponse("No movies found at that time", status=404)
    except ValueError:
        return HttpResponse("Invalid time format (use HH:MM)", status=400)
def userdetailsfn(request):
    try:
        tid = request.GET.get('tcid')
        if not tid:
            return HttpResponse("Ticket ID is required", status=400)
        
        tid = int(tid)
        obj = ticket.objects.get(id=tid)
        return render(request, 'userdetailsdisplay.html', {'obj': obj})
        
    except ValueError:
        return HttpResponse("Invalid ticket ID format", status=400)
    except ticket.DoesNotExist:
        return HttpResponse("Ticket not found", status=404)