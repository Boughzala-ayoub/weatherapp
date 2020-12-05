from django.shortcuts import render
from django.http import HttpResponse
import requests


# Create your views here.
def get_html_content(request):
        import requests
        city = request.GET.get('city')
        city = city.replace(" ", "+")
        USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        LANGUAGE = "en-gb,en;q=0.5"
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
        return html_content


def home(request):
    weather_data = None
    if 'city' in request.GET:
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data= dict()
        weather_data['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        weather_data['daytime'] = soup.find('div', attrs={'id': 'wob_dts'}).text
        weather_data['status'] = soup.find('span', attrs={'id': 'wob_dc'}).text
        weather_data['temp'] = soup.find('span', attrs={'id': 'wob_tm'}).text
    return render(request, 'core/home.html', {'weather': weather_data})
