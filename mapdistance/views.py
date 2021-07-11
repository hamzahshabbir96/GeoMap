from django.shortcuts import render,get_object_or_404
from .models import Data_acquire
from .forms import Dataacquireform
from geopy.geocoders import Nominatim
from .utils import middle_Coord,zoom_scale
import folium
# Create your views here.
def calculate_distance_view(request):
    obj = get_object_or_404(Data_acquire,id=1)
    form=Dataacquireform(request.POST or None)
    geolocator=Nominatim(user_agent='mapdistance')

    city='Munich'
    location=geolocator.geocode(city)
    #location coord

    l_lat=location.latitude

    l_lon=location.longitude
    pointA=(l_lat,l_lon)

    #folium
    m=folium.Map(width=800,height=500,location=(l_lat,l_lon),zoom_start=8)
    #location marker
    folium.Marker([l_lat,l_lon],tooltip='Click',popup=location,
    icon=folium.Icon(color='red')).add_to(m)
    distance=0


    if form.is_valid():
        temp=form.save(commit=False)
        destination1=form.cleaned_data.get('destination')
        destination=geolocator.geocode(destination1)
        #source
        source1=form.cleaned_data.get('source')
        source=geolocator.geocode(source1)
        #source code
        s_lat=source.latitude
        s_lon=source.longitude
        pointA=(s_lat,s_lon)
        #destinationcoord
        d_lat=destination.latitude
        d_lon=destination.longitude
        pointB=(d_lat,d_lon)
        distance=round(geodesic(pointA,pointB).km,2)
        m=folium.Map(width=800,height=500,location=(s_lat,s_lon,d_lat,d_lon),zoom_start=zoom_scale(distance))
        #location marker
        folium.Marker([s_lat,s_lon],tooltip='Click',popup=source,
        icon=folium.Icon(color='red')).add_to(m)
        #destination marker
        folium.Marker([d_lat,d_lon],tooltip='Click',popup=destination,
        icon=folium.Icon(color='blue')).add_to(m)
        #draw the line
        md=str(distance)+' km'
        line=folium.PolyLine(locations=[pointA,pointB],weight=3,color='purple')
        m.add_child(line)
        folium.Marker(location=[(s_lat+d_lat)/2,(d_lon+s_lon)/2],popup=md,
              icon=folium.DivIcon(
                  icon_size=(180, 20),
                  html='''<div style="
                  font-size: 10pt;
                  font-family: serif;
                  color: black;
                  text-align: center;
                  background-color: white;">
                   Click to see Distance
                  </div>''')
             ).add_to(m)
        temp.location=location
        temp.distance=distance
        temp.save()

    m=m._repr_html_()

    context={
    'distance':obj,
    'form':form,
    'map':m,
    'dist':distance
    }
    return render(request, 'mapdistance/main.html',context)
